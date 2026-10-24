# HTTP API

The daemon offers an HTTP API on `127.0.0.1:<api_port>` (default 7365) under `/api/v2`. The TUI, the commands and the Pulse plugins all use it. Use it for plugins in other languages, scripts or your own tools.

The complete description is an OpenAPI document: the daemon serves it at `/api/v2/openapi.json`, and a copy is published in [pulse-bridge-api](https://github.com/PulseOrchestrator/pulse-bridge-api/blob/main/openapi/pulse-daemon.json). Generate a client from it in any language.

## Authentication

Every request needs `Authorization: Bearer <token>`.

| Token | Where | May use |
|---|---|---|
| Daemon token | `daemon.json` in the Pulse directory (field `token`), new on every daemon start | Everything |
| Service token | `pulse.json` of the server's Pulse plugin, new on every server start | Read services, groups, players and routing; start, stop and restart services; move players; events; report for its own service |

Service tokens cannot run console commands, read logs, switch maintenance or update or delete groups, and stop working when their server stops.

## Endpoints

| Method and path | Description | Service token |
|---|---|---|
| `GET /daemon` | Version and directory | |
| `POST /daemon/shutdown`, `POST /daemon/restart` | Stop or restart the daemon; servers keep running | |
| `POST /daemon/shutdown?services=true` | Stop every server, then the daemon; the next daemon starts them again | |
| `GET /groups` | Groups with pinned build | ✓ |
| `POST /groups/{name}/update` | Pin the newest build | |
| `DELETE /groups/{name}?delete_data=` | Delete a group; its services stop and are forgotten | |
| `GET /services`, `GET /services/{id}` | Services | ✓ |
| `POST /services/{id}/start` · `stop` · `restart` | Change whether a service runs | ✓ |
| `GET /services/{id}/logs?offset=&lines=` | Console; pass the returned `offset` to follow | |
| `POST /services/{id}/exec` | Console command through RCON | |
| `PUT /services/{id}/report` | A server's own state, players and metrics | own service |
| `GET /players` | Players on all servers | ✓ |
| `POST /players/{uuid}/send` | Move a player through the proxy | ✓ |
| `GET /proxy/routing` | Routed servers, lobby and fallback, maintenance | ✓ |
| `POST /proxy/maintenance` | Switch maintenance mode | |
| `GET /events` | WebSocket event stream | ✓ |
| `GET /openapi.json` | The OpenAPI description (no token needed) | |

Errors have a status code and a body `{"error": {"kind": "...", "message": "..."}}`.

## Events

`GET /api/v2/events` upgrades to a WebSocket. Each text frame is one JSON event:

```json
{"type": "service", "service": {"id": "lobby-1", "status": "running", "...": "..."}}
{"type": "player_send", "player": "069a79f4-44e9-4726-a5be-fca90e38aaf5", "service": "bedwars-2"}
```

`service` arrives whenever a service changes its status, desired state, process, port or reported state. Reconnect after a daemon restart and read `GET /services` again for anything you missed.

## Versions

The major version is part of the path (`/api/v2`). Minor versions only add endpoints and fields; clients should ignore fields they do not know.
