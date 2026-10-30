# Groups and server software

A group is one file in `groups/`. Its name is the file name: `groups/bedwars.toml` is the group `bedwars`, and its services are `bedwars-1`, `bedwars-2`, ...

```toml
software = "paper"
version = "latest"
memory = "1G"
mode = "dynamic"
instances = 2
templates = ["bedwars"]
```

Create, change and delete groups with `pulse group create`, `edit` and `delete` ([commands](commands.md)), in the [TUI](tui.md) with `n`, `e` and `D`, or by writing the file yourself.

Group names use lowercase letters, digits and `-`, start with a letter and have at most 32 characters. All fields are listed in the [configuration reference](../reference/configuration.md#group-files).

## Server software

| `software` | Source | Notes |
|---|---|---|
| `paper` | PaperMC | Ships with the `pulse-paper` plugin |
| `purpur` | PurpurMC | As Paper |
| `folia` | PaperMC | As Paper |
| `velocity` | PaperMC | The proxy; exactly one instance |
| `fabric` | Fabric Meta | Pulse installs FabricProxy-Lite and Fabric API for the proxy |
| `vanilla` | Mojang | Not reachable through the proxy (no forwarding support) |
| `custom` | your own command | Any program; see [custom servers](#custom-servers) |

## Versions

| `version` | Meaning |
|---|---|
| `latest` (default) | The newest stable version |
| `1.21.4` | The newest build of this version |
| `1.21.4#232` | Exactly this build. For Fabric the part after `#` is the loader version |

There is no approval list: any version the upstream project offers works. The Pulse plugin for Paper, Purpur and Folia needs version 26 or newer; on older versions such as 1.21 it does not load, so those servers have no metrics and no `PulseApi`.

### Pinned builds

The first start resolves `version` to a concrete build and remembers it. Later starts use the same build, so `latest` does not change under a running network. To move to the newest build:

```bash
pulse group update lobby
```

Running services keep their build until they restart; `pulse service restart lobby-1` applies it. Changing `version` in the file resolves again on the next start.

## Java

Pulse reads which Java version a server needs and downloads a matching Eclipse Temurin runtime into `runtimes/`. To use your own Java instead:

```toml
java = "/usr/lib/jvm/java-25/bin/java"
```

## Static and dynamic

| `mode` | Behaviour |
|---|---|
| `static` (default) | The service directory is created from the templates once and keeps its data: worlds, plugin data, configs. |
| `dynamic` | Every start begins with a fresh copy of the templates, e.g. for minigame rounds. |

## Instances

`instances` is the number of services of the group. Lowering it stops the services above the new count; their directories stay in `services/`. Deleting a group stops its services and keeps their directories, unless you delete the data with it. Each service is started and stopped on its own; the TUI acts on all services of a group at once.

## Start-up and crashes

A service counts as ready when its console prints the server's ready line (`Done (…)! For help, type "help"`, for Velocity `Done (…)!`). Until then it is `starting`. If it is not ready within `startup_timeout` seconds (default 300), Pulse stops it and treats it as a failed start.

A server that crashes or fails to start is restarted after 5 seconds, then after twice as long each time, up to 5 minutes. After 5 minutes of stable running the delay starts over. A manual `pulse service start` starts at once.

## Custom servers

`custom` runs any command in the service directory. Relative paths like `./start.sh` refer to that directory, so a template can bring the script along.

```toml
software = "custom"
command = ["./start.sh"]
ready_pattern = "^Server started"   # optional; without it the service is ready at once
```

The process gets these environment variables:

| Variable | Value |
|---|---|
| `PULSE_SERVICE` | Service id, e.g. `event-1` |
| `PULSE_GROUP` | Group name |
| `PULSE_PORT` | Port assigned to the service |
| `PULSE_MEMORY_MB` | `memory` in MB |
| `PULSE_FORWARDING_SECRET` | Velocity forwarding secret, if a proxy group exists |

Pulse stops custom servers with `SIGTERM`.
