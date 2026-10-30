# Install

Pulse is a single binary for Linux x86_64 and Windows x86_64. It needs no Java installation of its own: it downloads the Java version each server needs.

## Download into the Pulse directory

Pulse keeps everything in one directory: configuration, server files, downloads. Put the binary there too:

```bash
mkdir -p /srv/pulse && cd /srv/pulse
curl -Lo pulse https://github.com/PulseOrchestrator/PulseOrchestrator/releases/download/v2.0.0/pulse-2.0.0-x86_64-linux
chmod +x pulse
./pulse --version
```

On Windows, in PowerShell:

```powershell
New-Item -ItemType Directory -Force C:\pulse; cd C:\pulse
Invoke-WebRequest -OutFile pulse.exe https://github.com/PulseOrchestrator/PulseOrchestrator/releases/download/v2.0.0/pulse-2.0.0-x86_64-windows.exe
.\pulse --version
```

The commands in this guide are the same on Windows with `.\pulse` instead of `./pulse`; the systemd section is Linux only.

Every release also contains `SHA256SUMS` and its signature `SHA256SUMS.sig`. `pulse self-update` checks both automatically; see [Updates](../guides/updates.md).

## Set up a first network

```bash
./pulse init
```

`init` asks you to accept the [Minecraft EULA](https://aka.ms/MinecraftEULA), the port players connect to (25565), the lobby software (Paper) and its memory (2G). Then it writes `pulse.toml`, a Velocity group `proxy` and a group `lobby`, and offers to start everything right away. The first start downloads Velocity, the lobby server and Java, which can take a minute. After that, connect Minecraft to your machine.

Opening the TUI with `./pulse` in an empty directory shows the same setup.

For scripts and agents, pass everything as options; without a terminal `init` asks nothing:

```bash
./pulse init --accept-eula --port 25565 --lobby paper --memory 2G --start --json
```

`init` only writes into a directory without `pulse.toml` and without group files. [Your first network](first-network.md) explains the files it writes.

## Which directory Pulse uses

A binary with a `pulse.toml` beside it manages its own directory, wherever you call it from: `/srv/pulse/pulse service list` works from any directory, and so does `./pulse` inside it. Otherwise Pulse uses the current directory.

`--root <dir>` and the environment variable `PULSE_HOME` override both, e.g. for one binary on the `PATH` that manages several directories:

```bash
install -m 755 pulse-2.0.0-x86_64-linux /usr/local/bin/pulse
pulse --root /srv/pulse service list
```

## Start the daemon

If you did not let `init` start the network:

```bash
./pulse daemon start
./pulse daemon status
```

Its output goes to `daemon.log` in the Pulse directory. `pulse daemon stop` ends it; your servers keep running. `pulse daemon stop --services` stops the servers too, e.g. before you shut the machine down; the next `pulse daemon start` starts the same servers again.

### As a systemd service

For a permanent setup, let systemd run the daemon in the foreground:

```ini
# /etc/systemd/system/pulse.service
[Unit]
Description=Pulse
After=network-online.target
Wants=network-online.target

[Service]
User=minecraft
ExecStart=/srv/pulse/pulse daemon run
Restart=on-failure
# Stop only the daemon. With the default (control-group) systemd would also
# stop every Minecraft server when the daemon stops or restarts.
KillMode=process

[Install]
WantedBy=multi-user.target
```

If the daemon runs already, stop it first with `./pulse daemon stop`, then:

```bash
systemctl enable --now pulse
```

`KillMode=process` is required: servers run in their own sessions but in the unit's control group, and Pulse relies on them surviving a daemon restart.

## Open the TUI

```bash
./pulse
```

Without a running daemon the TUI offers to start one. Continue with [your first network](first-network.md).
