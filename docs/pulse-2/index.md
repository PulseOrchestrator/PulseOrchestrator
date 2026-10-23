# Pulse 2

Pulse runs a Minecraft network on one machine: groups of servers behind one Velocity proxy, started, restarted and routed by a background daemon. You control it with a terminal UI or with plain commands that scripts and agents can use just as well.

!!! info "Release status"
    Pulse 2 is in development and has no public release yet. These pages describe it as it is built today. For production networks use [Pulse 1](../pulse-1/index.md).

## How it fits together

```text
pulse daemon      background process: keeps every server in the state you asked for
pulse             terminal UI
pulse <command>   the same actions as commands, with --json output

Minecraft servers and Velocity run independently of the daemon.
pulse-velocity    plugin in Velocity: registers servers, routes players
pulse-paper       plugin in Paper, Purpur and Folia: reports players and metrics, offers PulseApi
```

- **One binary.** Daemon, TUI and commands are the same program. The plugins are built in.
- **Servers outlive the daemon.** Stopping, restarting or updating the daemon does not stop a single server; the next daemon takes them over.
- **No approval lists.** Every version the upstream project offers can be used, and Pulse downloads the matching Java itself.
- **Configuration is files.** `pulse.toml` and one file per group, readable and easy to keep in Git.

## Concepts

| Term | Meaning |
|---|---|
| **Group** | A blueprint in `groups/<name>.toml`: software, version, memory, mode, number of instances, templates |
| **Service** | One instance of a group, e.g. `lobby-1`, with its own directory under `services/` |
| **Template** | A directory copied into a service before it starts: plugins, configs, worlds |
| **Proxy** | The Velocity group. Players connect to it and are routed to the other servers |
| **Desired state** | Whether a service should run. Pulse starts, restarts and stops servers to match it |

## Where to go next

- [Install Pulse](getting-started/install.md) and [set up a first network](getting-started/first-network.md).
- [Groups and server software](guides/groups.md) explains what you can run.
- [Commands and automation](guides/commands.md) covers `--json`, exit codes and scripting.
- [Plugin development](plugins/pulse-api.md) shows how your own plugins talk to Pulse.
