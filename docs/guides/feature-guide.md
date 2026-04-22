# Feature Guide

PulseOrchestrator separates reusable server definitions from actual running instances.

## Core concepts

### Task

A task is a reusable blueprint stored in `tasks.json`.

It defines the server software, version, preferred port, restart policy, storage mode, templates, and advanced runtime settings.

### Service

A service is a concrete instance created from a task.

Services are persisted in the orchestrator database, provisioned into the `services/` directory, and managed through the orchestrator process manager.

### Proxy routing

Routing is task-based, not service-ID-based.

You choose:

- one default entry task
- zero or more fallback tasks

The proxy then resolves those tasks to whichever matching services are currently running.

## Main workflows

### 1. Create a task blueprint

Use the orchestrator console:

```text
task create lobby
```

The interactive flow asks for:

- server software
- server version
- preferred port
- storage mode
- restart policy
- optional description and tags
- optional template scaffolding
- optional advanced settings

You can inspect defined blueprints with:

```text
task list
```

### 2. Create and start a service

Instantiate a service from a task:

```text
service create lobby
service start lobby-1
```

Useful related commands:

```text
service list
service logs lobby-1 100
service attach lobby-1
service command lobby-1 say hello
service restart lobby-1
service stop lobby-1
```

### 3. Route players through the built-in proxy

Set the default entry task and fallback order:

```text
proxy route set-default lobby
proxy route add-fallback fallback
proxy route show
proxy start
```

Operational commands:

```text
proxy status
proxy logs 100
proxy restart
proxy stop
```

## Templates and provisioning

Templates let you scaffold reusable files into new services.

Typical pattern:

1. Create a task.
2. Scaffold or attach a template.
3. Create services from that task.
4. Rebuild non-persistent services when you want a clean reprovisioned state.

For a full wipe and re-apply of templates on an existing service:

```text
service rebuild lobby-1
```

## Plugin behavior

### Paper plugin

The Paper integration is aimed at in-game control and bridge access:

- `/pulse` for orchestrator-related operations
- `/hub` for routing players back through the network flow
- a Bukkit `ServicesManager` bridge API for plugin integrations

### Velocity plugin

The standalone Velocity integration keeps the proxy registration in sync with orchestrator state by polling the HTTP API.

It is useful when you want an external Velocity instance instead of the built-in proxy-managed workflow.

## Operational advice

- Treat tasks as stable blueprints and services as disposable runtime instances.
- Keep the runtime base path on persistent storage.
- Use tags and descriptions early so task lists stay readable once you have multiple environments.
- Keep one clear entry task for player joins and use fallbacks only for deliberate backup ordering.
- Document which tasks are persistent and which are intentionally disposable before you scale out.
