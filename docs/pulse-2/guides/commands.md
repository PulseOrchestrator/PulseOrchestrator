# Commands and automation

Every action of the TUI is also a command. Commands never ask questions, can print JSON and report the outcome in their exit code, so scripts and AI agents can operate Pulse like a person. The one exception is `pulse init` in a terminal: it asks for the settings you did not give as options, and never asks with `--json` or without a terminal.

## Global options

| Option | Meaning |
|---|---|
| `--root <dir>` | Pulse directory. Defaults to `$PULSE_HOME`, then the directory of the `pulse` binary if a `pulse.toml` is beside it, then the current directory |
| `--json` | Print JSON instead of text, on success and on errors |

## Commands

| Command | Action |
|---|---|
| `pulse` | Open the [TUI](tui.md) |
| `pulse init [--accept-eula] [--port 25565] [--lobby paper] [--memory 2G] [--start\|--no-start] [--timeout 600]` | [Set up a first network](../getting-started/install.md#set-up-a-first-network) in an empty directory: `pulse.toml`, groups `proxy` and `lobby`. `--start` also starts the daemon and both servers and waits up to `--timeout` seconds for each |
| `pulse daemon run` | Run the daemon in the foreground (systemd) |
| `pulse daemon start` | Start the daemon in the background; output in `daemon.log` |
| `pulse daemon status` | Show whether a daemon runs |
| `pulse daemon stop` | Stop the daemon; servers keep running |
| `pulse daemon stop --services [--timeout 120]` | Stop every server, then the daemon. The next `pulse daemon start` starts the same servers again |
| `pulse daemon restart` | Restart the daemon in place; servers keep running |
| `pulse group list` / `show <name>` | Groups with their pinned build |
| `pulse group update <name>` | Use the newest build of the group's version from the next start |
| `pulse group create <name> --software <software> [options]` | Create a group; its services start out stopped. Needs no daemon |
| `pulse group edit <name> [options]` | Change a group; comments in the file stay. Needs no daemon |
| `pulse group delete <name> [--delete-data]` | Stop and forget the group's services; `--delete-data` also deletes their directories |
| `pulse service list` / `show <id>` | Services with status, port, build and metrics |
| `pulse service start <id>` | Start and keep running |
| `pulse service stop <id>` | Stop and keep stopped |
| `pulse service restart <id>` | Stop and start again |
| `pulse service logs <id> [--lines 50]` | End of the console |
| `pulse service exec <id> <command…>` | Console command through RCON (Minecraft servers) |
| `pulse proxy status` | Routed servers, lobby and fallback, maintenance |
| `pulse proxy maintenance on\|off` | Switch maintenance mode |
| `pulse player list` | Players on all servers |
| `pulse player send <name\|uuid> <service>` | Move a player |
| `pulse import <pulse1-dir> [--dry-run] [--force]` | [Import Pulse 1](import.md) |
| `pulse self-update [--check] [--pre]` | [Update Pulse](updates.md) |

`start`, `stop` and `restart` accept `--wait` to return only when the service is running or stopped, with `--timeout <seconds>` (default 60). A start that ends in a crash fails instead of waiting.

`group create` and `group edit` take the fields of the [group file](../reference/configuration.md#group-files) as options: `--software`, `--version`, `--memory`, `--mode`, `--instances`, `--templates` (comma-separated), `--java`, `--ready-pattern`, `--startup-timeout`. `""` clears `--templates`, `--java` and `--ready-pattern`. The command of a custom group follows `--`:

```bash
pulse group create event --software custom --ready-pattern '^Server started' -- ./start.sh --port 25570
pulse group edit bedwars --instances 4 --memory 2G
```

`pulse <command> --help` describes every option.

## Exit codes

| Code | Meaning |
|---|---|
| `0` | Success |
| `1` | Failed, e.g. a start that crashed |
| `2` | Invalid input or configuration, e.g. the EULA is not accepted |
| `3` | Not found |
| `4` | No daemon reachable |
| `5` | `--wait` ran out of time |

## JSON

Successful commands print one JSON object:

```bash
pulse --json service start app-1 --wait
```

```json
{
  "service": {
    "id": "app-1",
    "group": "app",
    "desired": "running",
    "status": "running",
    "pid": 63299,
    "port": 30000,
    "build": null,
    "failures": 0,
    "retry_in_seconds": null,
    "last_error": null,
    "state": null,
    "metrics": null
  }
}
```

Errors print `error.kind` and `error.message` and set the exit code:

```bash
pulse --json service show nope-1   # exit code 3
```

```json
{ "error": { "kind": "not_found", "message": "service \"nope-1\" not found" } }
```

Service `status` is one of `stopped`, `preparing`, `starting`, `running`, `stopping`, `backoff`; `desired` is `running` or `stopped`.

## Groups as files

`group create` and `group edit` write `groups/<name>.toml` (see [Groups](groups.md)). You can also write the file yourself; the daemon picks up changes within a second. `pulse group show <name>` reports errors in a file with exit code `2`. `group create` fails with exit code `2` if the group exists, `group edit` and `group delete` with `3` if it does not.
