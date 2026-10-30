# First network

This sets up a Velocity proxy and a Paper lobby. Players connect to the proxy on port 25565 and land in the lobby.

`pulse init` (see [Install](install.md#set-up-a-first-network)) writes exactly these files and starts both servers. This page shows what it does, so you can change the files or write them yourself.

## Configure the proxy

```toml
# pulse.toml
eula = true

[proxy]
port = 25565
lobby = ["lobby"]
```

## Define the groups

```toml
# groups/proxy.toml
software = "velocity"
memory = "512M"
```

```toml
# groups/lobby.toml
software = "paper"
memory = "2G"
```

`version` defaults to `latest`, the newest stable release. The daemon reads the files every second; no restart is needed.

## Start the servers

```bash
pulse service start proxy-1 --wait
pulse service start lobby-1 --wait
pulse service list
```

The first start downloads the server and the right Java version, which can take a minute. `--wait` returns once the server is ready for players.

Connect with Minecraft to your machine's address. Velocity checks the account and forwards you to `lobby-1`.

## Look inside

- `pulse` opens the TUI with all services, their console and metrics.
- `pulse service logs lobby-1` prints the end of the console.
- `pulse service exec lobby-1 say Hello` runs a console command.

Services you started stay started: after a crash Pulse restarts them, and after a reboot the daemon starts them again. `pulse service stop` stops a service until you start it again.

## Next steps

- Add game servers as more groups and list them in `[proxy] fallback` so kicked players have somewhere to go: [Proxy and routing](../guides/proxy.md).
- Put plugins and configs into [templates](../guides/templates.md).
- Pin versions and update builds: [Groups and server software](../guides/groups.md).
