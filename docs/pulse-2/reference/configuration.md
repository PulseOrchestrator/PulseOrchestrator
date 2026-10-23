# Configuration reference

## pulse.toml

All settings are optional. Changes apply within a second, except `api_port`, which applies when the daemon starts.

```toml
eula = true
api_port = 7365
ports = { first = 30000, last = 30999 }

[proxy]
port = 25565
lobby = ["lobby"]
fallback = []
maintenance_message = "The network is in maintenance. Please try again later."
maintenance_bypass = "pulse.maintenance.bypass"
```

| Setting | Default | Meaning |
|---|---|---|
| `eula` | `false` | You accept the [Minecraft EULA](https://aka.ms/MinecraftEULA). Without it, Minecraft servers do not start |
| `api_port` | `7365` | Port of the daemon API on `127.0.0.1`. Plugins connect here |
| `ports.first`, `ports.last` | `30000`, `30999` | Range for server and RCON ports |
| `proxy.port` | `25565` | Port players connect to |
| `proxy.lobby` | `[]` | Groups for joining players, in order of preference |
| `proxy.fallback` | `[]` | Groups for kicked players; empty means `lobby` |
| `proxy.maintenance_message` | see above | Shown to players during maintenance |
| `proxy.maintenance_bypass` | `pulse.maintenance.bypass` | Permission to join during maintenance |

## Group files

`groups/<name>.toml`, one per group. See [Groups and server software](../guides/groups.md).

| Field | Default | Meaning |
|---|---|---|
| `software` | required | `paper`, `purpur`, `folia`, `velocity`, `fabric`, `vanilla` or `custom` |
| `version` | `latest` | `latest`, a version like `1.21.4`, or a build like `1.21.4#232` |
| `memory` | `1G` | Heap size, e.g. `512M` or `2G` |
| `mode` | `static` | `static` keeps data, `dynamic` starts fresh from the templates each time |
| `instances` | `1` | Number of services; `velocity` allows only `1` |
| `templates` | `[]` | Template directories applied after `global` and `software/<software>` |
| `java` | automatic | Path to your own `java` |
| `ready_pattern` | built in | Regular expression for the console line that marks the server ready |
| `startup_timeout` | `300` | Seconds until a server that is not ready counts as a failed start |
| `command` | — | Program and arguments, only for `custom` |

Unknown fields are an error, so typos do not go unnoticed.

## Directory layout

| Path | Content |
|---|---|
| `pulse.toml`, `groups/` | Your configuration |
| `templates/` | Your templates |
| `services/<id>/` | Working directory of a service, with `console.log` |
| `state.json` | Which services should run, pinned builds, maintenance mode |
| `cache/`, `runtimes/` | Downloaded servers, mods and Java runtimes |
| `plugins/` | Optional: `pulse-velocity.jar` or `pulse-paper.jar` to use instead of the built-in plugins |
| `forwarding.secret` | Velocity forwarding secret |
| `daemon.json`, `daemon.lock` | Address and token of the running daemon (readable only by its owner) |
| `daemon.log` | Output of a daemon started with `pulse daemon start` |

To back up a network, copy the whole directory while the servers are stopped. `cache/` and `runtimes/` can be left out; Pulse downloads them again.
