# Migrating from Pulse 1

`pulse import` takes over a Pulse 1 installation into a new, empty Pulse 2 directory. Pulse 1 is only read, never changed, so you can go back.

## Steps

1. Stop Pulse 1 completely (`system shutdown`). Import refuses while Pulse 1 still runs servers; `--force` overrides this, for example when a stale PID is reported.
2. Preview:

    ```bash
    pulse --root /srv/pulse2 import /srv/pulse1 --dry-run
    ```

3. Import:

    ```bash
    pulse --root /srv/pulse2 import /srv/pulse1
    ```

4. Start the daemon. Services that were running in Pulse 1 start again:

    ```bash
    pulse --root /srv/pulse2 daemon start
    ```

## What is taken over

| Pulse 1 | Pulse 2 |
|---|---|
| Tasks in `tasks.json` | Groups in `groups/`; names become lowercase (`Lobby` → `lobby`) |
| `PERSISTENT` / `RESET_ON_START` | `mode = "static"` / `"dynamic"` |
| Number of services per task | `instances` |
| Services, e.g. `Lobby-1` | `lobby-1`; data of static services is copied |
| Running services (desired state) | Started again by the daemon |
| Proxy in `proxy/` | Group `proxy` (Velocity), directory copied |
| `config.json` proxy port, default entry task, fallback tasks, maintenance | `[proxy]` in `pulse.toml`, maintenance mode |
| Port range | `ports` in `pulse.toml` |
| `templates/` | Copied |
| Forwarding secret | Kept, so existing server configs stay valid |

The Pulse 1 plugins are left out of every copy; Pulse 2 installs its own. Pulse 1 accepted the Minecraft EULA for your servers, so the import sets `eula = true`.

Settings without an equivalent, such as `jvmArgs`, `serverArgs`, `environment`, `startPriority` or `preferredPort`, are listed as notes in the output. The target directory must not contain a `pulse.toml` or group files yet.
