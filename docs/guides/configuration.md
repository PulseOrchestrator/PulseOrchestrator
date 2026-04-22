# Configuration Reference

PulseOrchestrator stores its settings in two files inside your orchestrator folder:

| File | Purpose |
|---|---|
| `config.json` | All orchestrator settings — API, memory defaults, proxy, health monitoring, backups, and logs |
| `tasks.json` | Your server blueprints — one entry per server type you want to run |

Both files are plain JSON. You can edit them in any text editor. **Restart the orchestrator after making changes** — it reads these files on startup.

!!! tip "Not sure what JSON is?"
    JSON is a simple text format for storing settings. It uses `{` curly braces `}` for sections and `"key": value` pairs for individual settings. Values in quotes are text, values without quotes are numbers or true/false switches.

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
    "fallbackTasks": ["fallback"]
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
| `host` | `"127.0.0.1"` | The network address the API listens on. `127.0.0.1` means only programs on the same machine can connect. Change to `0.0.0.0` if plugins on other machines need to reach the API — but make sure your firewall only allows trusted IPs. |
| `apiPort` | `8080` | The port number for the API. Change this if something else on your machine already uses port 8080. |
| `apiSecret` | *(generated)* | A long random password that plugins must send with every API request. **Never share this publicly.** It is generated for you and stored here — you just copy it into your plugin configs. |

---

### Java settings

These tell the orchestrator where Java is and set the default memory for game servers.

| Setting | Default | Description |
|---|---|---|
| `java.path` | `"java"` | The path to the Java executable. The default `"java"` works if Java is in your system PATH. If the orchestrator cannot find Java, provide the full path like `"C:\\Program Files\\Java\\jdk-21\\bin\\java.exe"` (Windows) or `"/usr/bin/java"` (Linux). |
| `java.defaultMaxMemoryMB` | `1024` | The maximum RAM a game server can use, in megabytes. 1024 = 1 GB. This is the default — you can override it per task. |
| `java.defaultMinMemoryMB` | `512` | The starting memory allocation for game servers. Minecraft performs best when min and max are set to the same value on servers with enough RAM. |

!!! tip "How much memory should I give?"
    A small survival server needs about 1–2 GB. Minigame or lobby servers can often run on 512 MB. Large modpacks may need 4–8 GB. Start conservative and increase if the server is lagging.

---

### Port range

PulseOrchestrator assigns a unique port to each game server it creates, picked from this range.

| Setting | Default | Description |
|---|---|---|
| `portRange.min` | `25700` | The lowest port number that can be assigned to a game server. |
| `portRange.max` | `25800` | The highest port number. The range `25700–25800` allows up to 100 simultaneous servers. |

!!! note
    Players never connect to these ports directly — they connect to the proxy port instead. The individual server ports only need to be reachable from the proxy, which runs on the same machine.

---

### Proxy settings

The built-in proxy is what players connect to. It routes them to the right game server automatically.

| Setting | Default | Description |
|---|---|---|
| `proxy.type` | `"VELOCITY"` | The proxy software. Currently always `VELOCITY`. |
| `proxy.bindPort` | `25565` | The port players type when connecting to your network. `25565` is the default Minecraft port, so players can connect without typing a port number. |
| `proxy.minMemoryMB` | `256` | Minimum memory for the proxy process. |
| `proxy.maxMemoryMB` | `512` | Maximum memory for the proxy process. 512 MB is plenty for most networks. Increase if you have hundreds of simultaneous players. |
| `proxy.defaultEntryTask` | *(none)* | The task name that new players are sent to first. For example `"lobby"`. Set this via `proxy route set-default lobby` in the console. |
| `proxy.fallbackTasks` | `[]` | An ordered list of task names to try if no server is running for the entry task. For example `["fallback"]`. Add entries with `proxy route add-fallback` in the console. |

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

**Example:** With the defaults, if a server crashes 3 times within 5 minutes, the monitor stops trying and marks it as failed. You would then investigate the logs and restart it manually.

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
| `storageMode` | Yes | `PERSISTENT` — keep files between restarts. `RESET_ON_START` — wipe and re-provision on every start. See the [Feature Guide](feature-guide.md#storage-modes) for details. |
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

1. Stop the orchestrator before editing (or be ready to restart it).
2. Open the file in a text editor. Make sure to use proper JSON — every value except the last one in a block needs a comma after it.
3. Save the file.
4. Start the orchestrator again. If there is a mistake in the JSON, it will print an error telling you what is wrong.

!!! warning "Common JSON mistakes"
    - Trailing commas: `"value": 123,` ← the comma after the last item in a block causes an error
    - Missing quotes: `path: java` should be `"path": "java"`
    - Wrong brackets: use `{}` for objects and `[]` for lists

If you break the config file and cannot get the orchestrator to start, delete `config.json` and run the setup wizard again. **Do not delete `pulse.db`** — that holds your service records.
