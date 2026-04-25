# Feature Guide

This guide explains the main concepts and workflows you will use every day with PulseOrchestrator.

---

## Core concepts

### Task

A **task** is a blueprint that defines the properties of a server type - the software, version, memory allocation, and restart behaviour. Tasks are not running processes; they are templates from which services are created.

Tasks are stored in `tasks.json` in your orchestrator folder.

### Service

A **service** is a running server instance provisioned from a task. Multiple services can be created from the same task - for example, two lobby servers from a single `lobby` task.

Services are tracked in the orchestrator's database and stored in the `services/` folder.

### Proxy routing

Players connect to the built-in Velocity proxy, which routes them to the appropriate game server based on task configuration. The proxy uses **task-based routing**: you configure a default entry task (e.g. `lobby`) and an ordered fallback list. On connection, the proxy selects a `RUNNING` service matching the entry task; if none is available, it works through the fallback list in order.

### Bedrock compatibility

When enabled, PulseOrchestrator deploys [Geyser](https://geysermc.org) and [Floodgate](https://wiki.geysermc.org/floodgate/) as Velocity plugins, allowing Bedrock Edition clients to connect alongside Java clients on the same proxy process. Geyser handles protocol translation; Floodgate manages Bedrock player authentication and UUID assignment. Game servers require no changes - Bedrock players are transparent at the server level.

Both platforms use their default ports (Java: TCP 25565, Bedrock: UDP 19132), so neither player group needs to specify a port when connecting.

---

## Storage modes

When creating a task you choose a storage mode. This controls what happens to a service's world and data files.

| Mode | What it does |
|---|---|
| `PERSISTENT` | The server's files are kept between restarts. World data, plugins, configs - everything is saved. Use this for servers that should hold state. |
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

- **Server software** - `PAPER`, `PURPUR`, or `FABRIC`
- **Server version** - for example `1.21.4`
- **Preferred port** - the port PulseOrchestrator tries to assign first; it picks the next free one if taken
- **Storage mode** - `PERSISTENT` or `RESET_ON_START` (see above)
- **Restart policy** - `NEVER`, `ON_FAILURE`, or `ALWAYS` (see above)
- **Description and tags** *(optional)* - for your own organisation
- **Template scaffolding** *(optional)* - files to copy into every service created from this task
- **Advanced settings** *(optional)* - custom JVM arguments, server arguments, environment variables

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

Configure routing before starting the proxy:

```text
proxy route set-default lobby      ← players are sent here on connect
proxy route add-fallback fallback  ← used if no running service exists for the entry task
proxy route show                   ← confirm the active routing configuration
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
    The proxy routes players to a task only if at least one service from that task is in the `RUNNING` state. If no entry task service is available, it falls through the fallback list in order.

### 4. Put the network into maintenance mode *(optional)*

Maintenance mode blocks players from connecting to the network while you work on it. Players with the bypass permission can still join normally.

**Enable network-wide maintenance:**

```text
proxy maintenance enable
proxy maintenance status
proxy maintenance disable
```

**Enable maintenance on a single service** (blocks transfers to that server only, rest of the network stays open):

```text
service maintenance enable lobby-1
service maintenance status lobby-1
service maintenance disable lobby-1
```

The message shown to blocked players and the bypass permission are configurable - see [Proxy settings](configuration.md#proxy) in the Configuration Reference.

!!! tip "Testing maintenance mode"
    Grant yourself the bypass permission before enabling maintenance so you can verify the network is still reachable while players are blocked.

---

### 5. Enable Bedrock compatibility *(optional)*

To allow Bedrock Edition players to connect, enable Bedrock support and restart the proxy:

```text
proxy bedrock enable
proxy restart
```

Geyser and Floodgate are downloaded and deployed automatically on the next proxy start. Ensure **UDP port 19132** is open in your firewall - Java players use TCP 25565 which is typically already open.

See the [Configuration Reference](configuration.md#bedrock) for available Bedrock settings.

---

## Templates

Templates let you pre-fill new services with files - plugin jars, configs, worlds - so every service starts with the right setup.

Files placed in `templates/global/` are copied into **every** service regardless of task. Files in a task-specific template folder are only copied into services from that task.

Typical workflow:

1. Create a task.
2. Add any files you want pre-loaded into the template folder.
3. Create services - they automatically receive the template files.
4. To apply updated template files to an existing service, rebuild it:

```text
service rebuild lobby-1
```

!!! warning "Rebuild on persistent services"
    Rebuilding a persistent service re-provisions its directory. Any files in the service folder that are not part of a template will be lost. Take a backup before rebuilding if the service holds data you need.

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

---

## Plugin behaviour

### Paper plugin

The Paper plugin gives you in-game access to orchestrator features:

- `/pulse` - orchestrator commands from inside the game
- `/hub` - sends the player back through the network routing flow
- A Bukkit `ServicesManager` bridge for other plugins to talk to the orchestrator

### Velocity plugin

The Velocity plugin is bundled inside the orchestrator and deployed automatically to `proxy/plugins/` on every proxy start - no manual installation needed. It enforces maintenance mode at the proxy boundary: when the network or an individual service is in maintenance, the plugin blocks player connections and shows the configured message. Players with the bypass permission are unaffected.

---

## Operational tips

- Start with a single task and service, verify the setup end-to-end, then scale out.
- Use `system status` for a live overview of service states and system health.
- `service logs <id> 100` is the fastest way to diagnose a misbehaving server.
- The console status bar shows live service counts and any pending update notices.
- See the [Configuration Reference](configuration.md) for a full breakdown of every available setting.
- Keep the runtime base path on persistent, reliable storage - `pulse.db` holds all service records.
- Add tags and descriptions to tasks early; they become essential for readability as your setup grows.
- Define one clear default entry task for player connections. Use the fallback list for deliberate overflow routing, not as a catch-all.
- Note which tasks are persistent and which are disposable before scaling - the distinction matters during maintenance and migrations.
- Use `proxy maintenance enable` before taking the network down for updates; players see a clean message rather than a connection failure.
