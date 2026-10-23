# Templates

Templates are directories in `templates/` that Pulse copies into a service directory before the start. Use them for plugins, configuration files and worlds.

## Layers

For each start Pulse copies, in this order:

1. `templates/global/`
2. `templates/software/<software>/`, e.g. `templates/software/paper/`
3. every template listed in the group's `templates`, in order

Later files overwrite earlier ones. `global` and `software/<software>` are optional; a template named in `templates` must exist, otherwise the start fails.

```text
templates/
  global/server.properties           all servers
  software/paper/plugins/spark.jar   all Paper servers
  bedwars/plugins/BedWars.jar        groups with templates = ["bedwars"]
  bedwars/world/                     ...
```

When templates are applied depends on the group's `mode`: once for `static` services, on every start for `dynamic` ones.

## What Pulse writes

After copying, Pulse sets what it needs to run the server. It merges these settings into existing files, so everything else from your templates stays as it is.

| File | Settings |
|---|---|
| `eula.txt` | `eula=true`, when `eula = true` is set in `pulse.toml` |
| `server.properties` | `server-ip=127.0.0.1`, `server-port`, RCON on `127.0.0.1` with a random password; `online-mode=false` behind the proxy |
| `config/paper-global.yml` | Velocity forwarding (Paper, Purpur, Folia) |
| `config/FabricProxy-Lite.toml`, `mods/` | Forwarding mod and Fabric API (Fabric) |
| `velocity.toml`, `forwarding.secret` | Port and forwarding (Velocity) |
| `plugins/pulse-paper.jar`, `plugins/pulse-velocity.jar` | The Pulse plugins and their `pulse.json` |

Servers listen on `127.0.0.1` only; players reach them through the proxy.

Mods that Pulse installs are listed in `mods/.pulse-mods`. Pulse replaces only those; mods from your templates are never touched.
