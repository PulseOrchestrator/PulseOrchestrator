# Configuration Reference

PulseOrchestrator stores its settings in two files inside your orchestrator folder:

| File | Purpose |
|---|---|
| `config.json` | All orchestrator settings - API, memory defaults, proxy, health monitoring, backups, and logs |
| `tasks.json` | Your server blueprints - one entry per server type you want to run |

Both files are plain JSON. You can edit them in any text editor. **Restart the orchestrator after making changes** - it reads these files on startup.

---

## config.json

Below is a fully annotated example showing every available setting with its default value.

```json
{
  "host": "127.0.0.1",
  "apiPort": 8080,
  "apiSecret": "auto-generated-on-first-run",

  "java": {
    "path": "java",
    "defaultMaxMemoryMB": 1024,
    "defaultMinMemoryMB": 512
  },

  "portRange": {
    "min": 25700,
    "max": 25800
  },

  "proxy": {
    "type": "VELOCITY",
    "bindPort": 25565,
    "minMemoryMB": 256,
    "maxMemoryMB": 512,
    "defaultEntryTask": "lobby",
    "fallbackTasks": ["fallback"],
    "maintenanceMode": false,
    "maintenanceMessage": "§cThe network is currently in maintenance mode. Please try again later.",
    "maintenanceBypassPermission": "pulseorchestrator.maintenance.bypass",
    "bedrock": {
      "enabled": false,
      "port": 19132
    }
  },

  "health": {
    "enabled": true,
    "checkIntervalSeconds": 30,
    "maxRestartAttempts": 3,
    "restartCooldownSeconds": 60,
    "crashWindowSeconds": 300
  },

  "logs": {
    "rotationEnabled": true,
    "maxLogFiles": 10,
    "maxLogSizeMB": 50,
    "cleanupIntervalHours": 24,
    "retentionDays": 7
  },

  "backups": {
    "maxSlots": 3,
    "excludedDirs": ["logs", "cache", "bundler", ".paper-remapped"]
  },

  "updates": {
    "enabled": false,
    "checkOnStartup": true,
    "includePrereleases": false,
    "checkIntervalHours": 12,
    "runtimeWarningIntervalHours": 8
  }
}
```

---

### API settings

These control the web server that plugins and external tools use to talk to the orchestrator.

| Setting | Default | Description |
|---|---|---|
| `host` | `"127.0.0.1"` | Network address the API listens on. `127.0.0.1` restricts access to the local machine. Set to `0.0.0.0` to accept connections from other hosts - ensure your firewall limits access to trusted IPs. |
| `apiPort` | `8080` | TCP port the API server binds to. Change if the port is already in use. |
| `apiSecret` | *(generated)* | Bearer token required on every API request. Generated automatically on first run. **Never expose this value publicly** - copy it into plugin configs as needed. |

---

### Java settings

These tell the orchestrator where Java is and set the default memory for game servers.

| Setting | Default | Description |
|---|---|---|
| `java.path` | `"java"` | Path to the Java executable. The default `"java"` works when Java is on the system `PATH`. If the orchestrator cannot locate Java, provide the absolute path: `"C:\\Program Files\\Java\\jdk-21\\bin\\java.exe"` (Windows) or `"/usr/bin/java"` (Linux). |
| `java.defaultMaxMemoryMB` | `1024` | Default maximum heap size for game servers, in MB. Can be overridden per task. |
| `java.defaultMinMemoryMB` | `512` | Initial heap allocation for game servers, in MB. Setting min and max to the same value avoids GC pressure from heap resizing on servers with sufficient RAM. |

!!! tip
    Typical requirements: lobby/minigame servers - 512 MB to 1 GB; survival servers - 1–2 GB; large modpacks - 4–8 GB. Start conservative and increase based on observed memory pressure.

---

### Port range

PulseOrchestrator assigns a unique port to each game server it creates, picked from this range.

| Setting | Default | Description |
|---|---|---|
| `portRange.min` | `25700` | Lower bound of the port range assigned to game servers. |
| `portRange.max` | `25800` | Upper bound of the port range. The default range allows up to 100 concurrent servers. |

!!! note
    Game server ports are internal - players connect exclusively through the proxy. These ports only need to be reachable from the proxy process, which runs on the same host.

---

### Proxy settings

The built-in proxy is what players connect to. It routes them to the right game server automatically.

| Setting | Default | Description |
|---|---|---|
| `proxy.type` | `"VELOCITY"` | Proxy software. Currently always `VELOCITY`. |
| `proxy.bindPort` | `25565` | TCP port Java players connect to. `25565` is the Minecraft default, so no port suffix is needed in the server address. |
| `proxy.minMemoryMB` | `256` | Minimum heap allocation for the proxy process, in MB. |
| `proxy.maxMemoryMB` | `512` | Maximum heap allocation for the proxy process, in MB. 512 MB is sufficient for most networks; increase for very high player counts. |
| `proxy.defaultEntryTask` | *(none)* | Task whose running services receive newly connected players. Configure via `proxy route set-default <task>` in the console. |
| `proxy.fallbackTasks` | `[]` | Ordered list of tasks to attempt if no service is available for the entry task. Manage via `proxy route add-fallback` / `remove-fallback` in the console. |
| `proxy.maintenanceMode` | `false` | When `true`, all player connections are blocked at the proxy level. Toggle via `proxy maintenance enable` / `disable` in the console. |
| `proxy.maintenanceMessage` | *(see below)* | Kick/disconnect message shown to blocked players. Supports legacy `§` colour codes. |
| `proxy.maintenanceBypassPermission` | `pulseorchestrator.maintenance.bypass` | Velocity permission node that allows a player to bypass maintenance mode and connect normally. Requires a permission plugin (e.g. LuckPerms for Velocity). |

!!! note "Per-service maintenance"
  Individual services can also be put into maintenance mode independently - this blocks transfers to that specific server while the rest of the network stays open. Use `service maintenance enable <id>` in the console. Per-service maintenance uses the same `maintenanceMessage` and `maintenanceBypassPermission` as proxy-level maintenance.

---

### Bedrock compatibility { #bedrock }

When Bedrock support is enabled, PulseOrchestrator automatically downloads and deploys [Geyser-Velocity](https://geysermc.org) and [Floodgate-Velocity](https://wiki.geysermc.org/floodgate/) as proxy plugins. Bedrock players connect on the standard Bedrock port (19132) without needing to type a port number - the same as Java players on port 25565.

!!! note "How it works"
    Geyser translates the Bedrock protocol to Java at the proxy level. Floodgate handles Bedrock player authentication and assigns stable UUIDs, making Bedrock players indistinguishable from Java players to your game servers.

| Setting | Default | Description |
|---|---|---|
| `proxy.bedrock.enabled` | `false` | Enables Bedrock support. When `true`, Geyser and Floodgate JARs are downloaded and deployed on the next proxy start. |
| `proxy.bedrock.port` | `19132` | UDP port Bedrock clients connect to. `19132` is the Bedrock default, so no port suffix is required. Change only if the port is unavailable. |

!!! tip "Firewall"
    UDP port 19132 must be permitted inbound for Bedrock clients. Java clients use TCP 25565, which is typically already open.

After enabling Bedrock for the first time, an initial Geyser config is written to `proxy/plugins/Geyser-Velocity/config.yml`. You can edit it freely - PulseOrchestrator will not overwrite it on subsequent starts.

---

### Health monitor { #health-monitor }

The health monitor watches your game servers and can restart them automatically if they crash.

| Setting | Default | Description |
|---|---|---|
| `health.enabled` | `true` | Turn automatic health checking on or off. Leave this `true` in almost all cases. |
| `health.checkIntervalSeconds` | `30` | How often (in seconds) the monitor checks each server's status. |
| `health.maxRestartAttempts` | `3` | How many times the monitor will try to restart a crashed server before giving up and marking it `FAILED`. |
| `health.restartCooldownSeconds` | `60` | How many seconds to wait between restart attempts. This prevents rapid restart loops. |
| `health.crashWindowSeconds` | `300` | The time window (in seconds) used to count crashes. If a server crashes `maxRestartAttempts` times within this window, it is marked `FAILED`. Set it higher to be more tolerant of occasional crashes. |

**Example:** With default settings, a server that crashes 3 times within 5 minutes is marked `FAILED` and left stopped. Investigate the logs and restart it manually.

---

### Log settings

These control how the orchestrator manages its own log files in the `logs/` folder.

| Setting | Default | Description |
|---|---|---|
| `logs.rotationEnabled` | `true` | Whether old log files are automatically cleaned up. |
| `logs.maxLogFiles` | `10` | The maximum number of log files to keep per service. Older files are deleted when this limit is reached. |
| `logs.maxLogSizeMB` | `50` | The maximum size of a single log file in megabytes before it is rotated. |
| `logs.cleanupIntervalHours` | `24` | How often (in hours) the cleanup job runs to remove old log files. |
| `logs.retentionDays` | `7` | Log files older than this many days are deleted. |

---

### Backup settings

PulseOrchestrator has a built-in backup system that saves snapshots of your service files.

| Setting | Default | Description |
|---|---|---|
| `backups.maxSlots` | `3` | How many backup snapshots to keep per service. When you take a 4th backup, the oldest one is deleted automatically. |
| `backups.excludedDirs` | `["logs", "cache", "bundler", ".paper-remapped"]` | Folders inside a service directory that are skipped during backup. These are usually large temporary files that do not need to be saved. The `server.jar` file is always excluded regardless of this list. |

---

### Update settings

These control whether the orchestrator checks for newer versions of itself.

!!! note
    Update checking is disabled by default on pre-release builds. You can leave these settings as-is unless you want to opt in.

| Setting | Default | Description |
|---|---|---|
| `updates.enabled` | `false` | Turn update checking on or off. |
| `updates.checkOnStartup` | `true` | Run a check when the orchestrator starts. |
| `updates.includePrereleases` | `false` | Whether pre-release versions count as "newer". Leave `false` for stable deployments. |
| `updates.checkIntervalHours` | `12` | How often (in hours) to re-check in the background. |
| `updates.runtimeWarningIntervalHours` | `8` | If you are running an unsafe version, how often (in hours) to show the warning again. |

---

## tasks.json

Tasks are the blueprints for your servers. Each entry in the `tasks` array defines one server type.

```json
{
  "tasks": [
    {
      "name": "lobby",
      "description": "Main lobby server",
      "serverSoftware": "PAPER",
      "serverVersion": "1.21.4",
      "preferredPort": 25700,
      "maxMemoryMB": 1024,
      "minMemoryMB": 512,
      "storageMode": "PERSISTENT",
      "restartPolicy": "ON_FAILURE",
      "tags": ["lobby"],
      "templates": [],
      "jvmArgs": [],
      "serverArgs": ["--nogui"],
      "environment": {}
    }
  ]
}
```

### Task fields

| Field | Required | Description |
|---|---|---|
| `name` | Yes | A short unique identifier for this task. Used in commands like `service create lobby`. Lowercase letters and hyphens recommended. |
| `description` | No | A human-readable note about what this task is for. Only shown in `task list`. |
| `serverSoftware` | Yes | The server software to use. One of: `PAPER`, `PURPUR`, `FABRIC`. |
| `serverVersion` | Yes | The Minecraft version to run, for example `"1.21.4"`. PulseOrchestrator downloads the matching JAR automatically. |
| `preferredPort` | Yes | The port PulseOrchestrator tries to assign first when creating a service from this task. If that port is already taken, it picks the next free one in the configured range. |
| `maxMemoryMB` | Yes | Maximum RAM for servers of this type, in MB. Overrides the global default from `config.json`. |
| `minMemoryMB` | Yes | Minimum RAM for servers of this type, in MB. |
| `storageMode` | Yes | `PERSISTENT` - keep files between restarts. `RESET_ON_START` - wipe and re-provision on every start. See the [Feature Guide](feature-guide.md#storage-modes) for details. |
| `restartPolicy` | Yes | `NEVER`, `ON_FAILURE`, or `ALWAYS`. See the [Feature Guide](feature-guide.md#restart-policies) for details. |
| `tags` | No | A list of text labels for your own organisation, for example `["lobby", "hub"]`. |
| `templates` | No | Names of template folders to apply when creating services from this task. Leave empty to use only the global template. |
| `jvmArgs` | No | Extra arguments passed to the Java process before the `-jar` flag, for example `["-XX:+UseG1GC"]`. Most servers do not need custom JVM args. |
| `serverArgs` | No | Arguments passed to the server after the `-jar` flag. `["--nogui"]` is always included by default and disables the graphical window. |
| `environment` | No | Extra environment variables set for the server process, as key-value pairs. Most servers do not need this. |

### Server software options

| Value | Description |
|---|---|
| `PAPER` | Paper is the most popular high-performance Minecraft server software. Recommended for most setups. |
| `PURPUR` | Purpur is based on Paper and adds extra configuration options and gameplay tweaks. |
| `FABRIC` | Fabric is a lightweight mod loader, useful for server-side mods. |

!!! tip "Which software should I use?"
    If you are not sure, use `PAPER`. It has the best plugin ecosystem, the most community support, and runs well out of the box.

---

## Editing config safely

1. Stop the orchestrator, or be prepared to restart it after saving.
2. Edit the file in any text editor. JSON requires a comma after every value except the last one in a block.
3. Start the orchestrator. If the JSON is malformed, it will print a parse error with the location of the problem.

!!! warning "Common JSON mistakes"
    - Trailing comma on the last item in a block: `"value": 123,` ← remove the trailing comma
    - Unquoted string: `path: java` should be `"path": "java"`
    - Wrong bracket type: use `{}` for objects and `[]` for arrays

If the config is unrecoverable, delete `config.json` and run the setup wizard again. **Do not delete `pulse.db`** - it holds all service records.
