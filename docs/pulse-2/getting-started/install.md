# Install

Pulse is a single static binary for Linux x86_64. It needs no Java installation of its own: it downloads the Java version each server needs.

## Download

Download `pulse-<version>-x86_64-linux` from the [releases](https://github.com/PulseOrchestrator/PulseOrchestrator/releases), make it executable and put it on your `PATH`:

```bash
install -m 755 pulse-2.0.0-x86_64-linux /usr/local/bin/pulse
pulse --version
```

Every release also contains `SHA256SUMS` and its signature `SHA256SUMS.sig`. `pulse self-update` checks both automatically; see [Updates](../guides/updates.md).

## Choose a directory

Pulse keeps everything in one directory: configuration, server files, downloads. Pass it with `--root`, set `PULSE_HOME`, or run commands from inside it.

```bash
mkdir -p /srv/pulse && cd /srv/pulse
export PULSE_HOME=/srv/pulse
```

## Accept the Minecraft EULA

Minecraft servers only start after you accept the [Minecraft EULA](https://aka.ms/MinecraftEULA) in `pulse.toml`:

```toml
# /srv/pulse/pulse.toml
eula = true
```

## Start the daemon

For a first try, start it in the background:

```bash
pulse daemon start
pulse daemon status
```

Its output goes to `daemon.log` in the Pulse directory. `pulse daemon stop` ends it; your servers keep running.

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
ExecStart=/usr/local/bin/pulse --root /srv/pulse daemon run
Restart=on-failure
# Stop only the daemon. With the default (control-group) systemd would also
# stop every Minecraft server when the daemon stops or restarts.
KillMode=process

[Install]
WantedBy=multi-user.target
```

```bash
systemctl enable --now pulse
```

`KillMode=process` is required: servers run in their own sessions but in the unit's control group, and Pulse relies on them surviving a daemon restart.

## Open the TUI

```bash
pulse
```

Without a running daemon the TUI offers to start one. Continue with [your first network](first-network.md).
