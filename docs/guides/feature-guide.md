# Feature Guide

This guide explains the main concepts and workflows you will use every day with PulseOrchestrator.

---

## Core concepts

### Task

A **task** is a blueprint. It describes the kind of server you want — the software, version, memory limits, and restart behaviour — but it is not a running server by itself.

Think of it like a recipe: the recipe says what ingredients to use and how to cook them, but it is not the actual meal.

Tasks are stored in `tasks.json` in your orchestrator folder.

### Service

A **service** is a real running server created from a task.

Using the same analogy: a service is the meal you actually cooked from that recipe. You can make multiple services from the same task (for example two lobby servers from one `lobby` task).

Services are tracked in the orchestrator's database and live in the `services/` folder.

### Proxy routing

Players do not connect directly to game servers. They connect to the built-in proxy, which then sends them to the right server automatically.

The proxy uses **task-based routing** — you tell it which task is the default entry point (for example `lobby`) and which tasks are fallbacks (for example `fallback`). When a player connects, the proxy finds a running service that matches the entry task and sends the player there.

---

## Storage modes

When creating a task you choose a storage mode. This controls what happens to a service's world and data files.

| Mode | What it does |
|---|---|
| `PERSISTENT` | The server's files are kept between restarts. World data, plugins, configs — everything is saved. Use this for servers that should hold state. |
| `RESET_ON_START` | The server's folder is wiped and re-provisioned from the task template every time it starts. Use this for minigame servers where each round should start fresh. |

!!! tip
    When in doubt, use `PERSISTENT`. It is the safe default and what most servers need.

---

## Restart policies

A restart policy controls what PulseOrchestrator does when a service stops unexpectedly.

| Policy | What it does |
|---|---|
| `NEVER` | Never restart automatically. You restart it yourself. |
| `ON_FAILURE` | Only restart if the server crashed (non-zero exit code). If you stopped it on purpose, it stays stopped. |
| `ALWAYS` | Always restart, no matter how it stopped. |

The health monitor enforces a cooldown between restart attempts and a maximum number of retries to prevent crash loops. See the [Configuration Reference](configuration.md#health-monitor) for those settings.

---

## Main workflows

### 1. Create a task blueprint

Open the orchestrator console and run:

```text
task create lobby
```

The interactive wizard asks for:

- **Server software** — `PAPER`, `PURPUR`, or `FABRIC`
- **Server version** — for example `1.21.4`
- **Preferred port** — the port PulseOrchestrator tries to assign first; it picks the next free one if taken
- **Storage mode** — `PERSISTENT` or `RESET_ON_START` (see above)
- **Restart policy** — `NEVER`, `ON_FAILURE`, or `ALWAYS` (see above)
- **Description and tags** *(optional)* — for your own organisation
- **Template scaffolding** *(optional)* — files to copy into every service created from this task
- **Advanced settings** *(optional)* — custom JVM arguments, server arguments, environment variables

To see all your tasks:

```text
task list
```

### 2. Create and start a service

Once you have a task, create a server from it:

```text
service create lobby
service start lobby-1
```

PulseOrchestrator provisions the server directory, downloads the correct JAR if needed, and starts the process.

Other useful service commands:

```text
service list                      ← see all services and their state
service logs lobby-1 100          ← view the last 100 log lines
service attach lobby-1            ← live-follow the console output
service command lobby-1 say hello ← send a command directly to the server
service restart lobby-1
service stop lobby-1
service rebuild lobby-1           ← wipe and re-provision from the task template
service recreate lobby-1          ← delete and create a fresh service
```

### 3. Route players through the proxy

Set up routing before starting the proxy:

```text
proxy route set-default lobby      ← players land here first
proxy route add-fallback fallback  ← redirect here if lobby has no running server
proxy route show                   ← confirm the current routing config
proxy start
```

Other proxy commands:

```text
proxy status
proxy logs 100
proxy restart
proxy stop
```

!!! note "Routing requires at least one running service"
    The proxy can only send players to a task if there is at least one service from that task currently in the `RUNNING` state. If no services are running for the entry task, the proxy will use the first fallback task it can find.

---

## Templates

Templates let you pre-fill new services with files — plugin jars, configs, worlds — so every service starts with the right setup.

Files placed in `templates/global/` are copied into **every** service regardless of task. Files in a task-specific template folder are only copied into services from that task.

Typical workflow:

1. Create a task.
2. Add any files you want pre-loaded into the template folder.
3. Create services — they automatically receive the template files.
4. To apply updated template files to an existing service, rebuild it:

```text
service rebuild lobby-1
```

!!! warning "Rebuild on persistent services"
    Rebuilding a persistent service re-provisions its directory. Any changes made directly inside the service folder that are not part of a template will be lost. Back up important data first.

---

## JAR management

PulseOrchestrator downloads server JARs automatically when you create a service. It caches them in `server-jars/` so they are not downloaded again.

### Useful jar commands

```text
jar list                      ← list all cached JARs
jar check                     ← check all cached JARs for newer builds
jar check paper               ← check only Paper JARs
jar check paper 1.21.4        ← check a specific version
jar update paper 1.21.4       ← download the latest build for that version
jar update-all                ← update every cached JAR
```

!!! note "Updating JARs does not affect running services"
    Services copy their JAR at creation time. To apply a new build to an existing service, recreate it:

    ```text
    service recreate lobby-1
    ```

### REST API equivalents

All JAR operations are also available over the HTTP API.

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/jars` | List all cached JARs |
| `GET` | `/api/jars/{software}/{version}` | Get info for one cached JAR |
| `GET` | `/api/jars/{software}/{version}/check` | Check for an update without downloading |
| `POST` | `/api/jars/{software}/{version}/update` | Update one JAR to its latest build |
| `POST` | `/api/jars/update-all` | Update every cached JAR |

All routes require the `Authorization: Bearer <secret>` header.

---

## Plugin behaviour

### Paper plugin

The Paper plugin gives you in-game access to orchestrator features:

- `/pulse` — orchestrator commands from inside the game
- `/hub` — sends the player back through the network routing flow
- A Bukkit `ServicesManager` bridge for other plugins to talk to the orchestrator

### Velocity plugin

The standalone Velocity plugin is for setups where you run your own Velocity instance instead of using the built-in proxy. It polls the HTTP API to keep server registrations in sync with the orchestrator's state.

---

## Tips for new operators

- **Start small.** Create one task, one service, get it running, then expand.
- **Use `system status`** in the console to see a health overview at any time.
- **Logs are your friend.** Use `service logs <id> 100` when something is not working.
- **The status bar** at the bottom of the console always shows your running service count and any update notices.
- For a full explanation of every setting you can change, see the [Configuration Reference](configuration.md).
- Keep the runtime base path on persistent storage.
- Use tags and descriptions early so task lists stay readable once you have multiple environments.
- Keep one clear entry task for player joins and use fallbacks only for deliberate backup ordering.
- Document which tasks are persistent and which are intentionally disposable before you scale out.
