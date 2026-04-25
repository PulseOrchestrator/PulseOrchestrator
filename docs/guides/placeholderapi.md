# PlaceholderAPI Integration

PulseOrchestrator's Paper plugin includes an optional [PlaceholderAPI](https://github.com/PlaceholderAPI/PlaceholderAPI) expansion that exposes live orchestrator data as placeholders usable in scoreboards, chat formats, GUIs, holograms, and any other plugin that supports PAPI.

---

## Requirements

| Requirement | Details |
|---|---|
| Plugin | `plugin-paper` installed on the Paper server |
| PlaceholderAPI | 2.11+ installed on the same server (optional — the plugin starts without it) |

PlaceholderAPI is a **soft dependency**. The plugin starts and functions normally whether or not PAPI is present; the expansion is registered only when PAPI is detected at startup.

---

## How it works

### Service data cache

The expansion maintains a local cache of all services, refreshed from the orchestrator every **30 seconds** in the background. Non-metric placeholders (status, port, uptime, task name) are served from this cache.

### Live metrics push

Metric placeholders (`tps`, `mspt`, `ram`, `cpu`, `players`, `chunks`, `entities`) are populated by the **metrics push** mechanism: each Paper server running the plugin reports its own metrics to the orchestrator every **5 seconds**. The orchestrator stores these metrics alongside the service record, and they are included in the cache refresh.

This means:

- Metric placeholders are available for **Paper servers only** — they return `unknown` for any server that does not push metrics (e.g. non-Paper servers managed by the orchestrator).
- After a server first starts, metric placeholders show `unknown` until the first push cycle completes (≤ 5 seconds).
- If a server goes offline, its last reported metrics remain visible until the service record is updated.

### Service ID matching

Placeholders that accept a `<id>` parameter match against the service's ID with flexible normalisation — hyphens (`-`) and underscores (`_`) are treated as equivalent, and matching is case-insensitive. For example, `%pulse_service_status_lobby-1%` and `%pulse_service_status_lobby_1%` resolve to the same service.

---

## Placeholder reference

All placeholders use the `pulse` identifier and follow the format `%pulse_<placeholder>%`.

### Local server

These reflect the Paper server the placeholder is being evaluated on, without any orchestrator lookup.

| Placeholder | Returns | Example |
|---|---|---|
| `%pulse_local_online%` | Number of players currently online on this server | `12` |
| `%pulse_local_max%` | Max player slots configured for this server | `100` |

### Network overview

| Placeholder | Returns | Example |
|---|---|---|
| `%pulse_service_count_total%` | Total number of services (all states) | `5` |
| `%pulse_service_count_running%` | Number of services in the `RUNNING` state | `3` |
| `%pulse_task_running_<taskName>%` | Number of `RUNNING` services for a given task | `%pulse_task_running_lobby%` → `2` |

### Per-service — status

Replace `<id>` with the service ID (e.g. `lobby-1`).

| Placeholder | Returns | Fallback |
|---|---|---|
| `%pulse_service_status_<id>%` | Service state: `RUNNING`, `STOPPED`, `STARTING`, `FAILED`, etc. | `unknown` |
| `%pulse_service_port_<id>%` | Port the service is bound to | `-1` |
| `%pulse_service_task_<id>%` | Task name the service was created from | `unknown` |
| `%pulse_service_uptime_<id>%` | Time elapsed since the service last started, formatted as `1d2h3m4s` | `unknown` |

### Per-service — live metrics

These are populated by the metrics push mechanism described above. They return `unknown` if the server has not reported metrics yet or is not a Paper server.

| Placeholder | Returns | Example |
|---|---|---|
| `%pulse_service_online_players_<id>%` | Online player count | `7` |
| `%pulse_service_max_players_<id>%` | Max player slots | `100` |
| `%pulse_service_tps_<id>%` | Ticks per second (1-minute average), 2 decimal places | `19.98` |
| `%pulse_service_mspt_<id>%` | Milliseconds per tick, 2 decimal places | `1.23` |
| `%pulse_service_cpu_<id>%` | JVM process CPU usage, 2 decimal places | `4.72%` |
| `%pulse_service_ram_<id>%` | JVM heap usage in megabytes | `512` |
| `%pulse_service_chunks_<id>%` | Total loaded chunks across all worlds | `846` |
| `%pulse_service_entities_<id>%` | Total loaded entities across all worlds | `1204` |

---

## Examples

Show how full a lobby server is in a scoreboard:

```
%pulse_service_online_players_lobby-1% / %pulse_service_max_players_lobby-1%
```

Show TPS next to a service's status:

```
lobby-1: %pulse_service_status_lobby-1% | TPS: %pulse_service_tps_lobby-1%
```

Count running lobby servers network-wide:

```
Lobbies online: %pulse_task_running_lobby%
```

---

## Troubleshooting

**Placeholders all return blank / do not resolve**

: Confirm PlaceholderAPI is installed and enabled (`/plugins`). The plugin logs `Registered PlaceholderAPI expansion 'pulse'` on enable if registration succeeded.

**Metric placeholders return `unknown`**

: The service may not be running the Paper plugin, or fewer than 5 seconds have passed since startup. Check that `ServiceMetricsReporter` is not logging a warning about port resolution — this indicates the plugin could not identify its own orchestrator service ID.

**Service ID not found**

: Check the service ID as shown by `service list` in the orchestrator console. Remember that hyphens and underscores are normalised, but spelling must match.
