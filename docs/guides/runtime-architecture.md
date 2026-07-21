# Runtime Architecture

Pulse separates the operator-facing control plane from the processes that keep Minecraft services online. A normal production installation runs three Java components with different responsibilities.

## Components

| Component | Responsibility | Update frequency |
|---|---|---|
| Launcher | Starts the runtime in the correct order, prevents a second instance, activates downloaded versions, and restarts the orchestrator | Rare |
| Runtime Host | Owns the Velocity and Minecraft process handles, command input, console output, and live runtime state | Infrequent |
| Orchestrator | Provides the CLI and API, reads configuration, stores service metadata, provisions services, applies policy, and requests lifecycle actions | Frequent |

The Minecraft services and built-in Velocity proxy are children of the Runtime Host, not the orchestrator. This is why the orchestrator can restart during a compatible update without restarting the game network.

```text
Launcher
  |-- Runtime Host
  |     |-- Velocity proxy
  |     `-- Minecraft service JVMs
  |
  `-- Orchestrator
        |-- interactive console
        |-- public API
        |-- config, tasks, and database
        `-- local authenticated control connection to Runtime Host
```

The Runtime Host is internal. Operators use the orchestrator console and API; plugins also communicate only with the orchestrator API.

## Supported startup

Start Pulse through the Launcher for production use. The Launcher:

1. acquires an exclusive lock for the Pulse home folder;
2. starts or reconnects to the Runtime Host;
3. starts the orchestrator in the same terminal;
4. keeps running while the orchestrator is active; and
5. processes update requests after the orchestrator exits for an update.

Starting the orchestrator JAR directly is a development and recovery option. It runs in degraded mode and cannot use launcher-managed `system update`. Processes started in that mode cannot be guaranteed to survive an orchestrator restart.

!!! warning "Current platform limit"
    Launcher-managed startup currently requires Windows because child Java processes are resolved through `java.exe`. Linux can run the orchestrator directly in degraded mode, but warm launcher-managed updates are not supported there yet.

## State and folders

User-managed state remains in the Pulse home folder:

```text
config.json
tasks.json
pulse.db
services/
templates/
server-jars/
proxy/
logs/
```

Launcher-managed state is stored separately:

```text
runtime/
  current-release.json
  versions/
  control/
```

- `current-release.json` selects the active orchestrator and Runtime Host JARs.
- `versions/` contains immutable versioned artifacts.
- `control/` contains local session tokens, process metadata, the launcher lock, and pending update requests.

!!! danger "Protect the control folder"
    Run Pulse under a dedicated operating-system account and restrict the complete Pulse home folder to that account. A local user who can read the Runtime Host token can control services; a user who can modify update control files can interfere with updates.

Do not edit files in `runtime/control/` while Pulse is running. Do not use `pulse.db` or a saved PID as proof that a service is live. The Runtime Host is the source of truth for current process state.

## Reattachment after orchestrator restart

During a warm update, the Runtime Host remains alive and retains every process handle. The new orchestrator asks the host for its runtime registry and reattaches to existing service identities. It does not merely look up persisted PIDs.

After reattachment, the orchestrator can again:

- show live status;
- send console commands;
- read console output;
- stop and restart services; and
- update proxy routing.

If the Runtime Host cannot be reached, `system status` reports `HOST_UNAVAILABLE`. Persisted service information may still be shown, but live control is not reliable until the host connection is restored.

## Shutdown behavior

| Action | Orchestrator | Runtime Host | Services and proxy |
|---|---|---|---|
| Compatible warm update | Restarts | Keeps running | Keep running |
| Maintenance update | Restarts | May be replaced | Stop and are restored |
| `system shutdown` | Stops | Stops with Launcher | Stop |
| Direct orchestrator restart | Restarts | Not available | Continuity is not guaranteed |

A warm update protects game-process continuity, not every possible failure. A Runtime Host crash loses the live stdin/stdout ownership that makes reattachment possible. The current architecture detects this condition but does not transparently recover those process handles.

## Operational recommendations

- Keep the Launcher attached to a service supervisor that stops the whole Pulse process tree intentionally.
- Do not configure a supervisor to kill and restart only one of the three components.
- Back up `pulse.db`, `config.json`, `tasks.json`, `services/`, and `proxy/` before maintenance updates.
- Keep the Runtime Host stable. Routine features and policy changes should normally ship in the orchestrator.
- Check `system status` after every update and test a service command plus fresh console output.
- Treat a Runtime Host update as planned maintenance even when the updater automates it.

See [Updating Pulse](updates.md) for update modes and the operator workflow.
