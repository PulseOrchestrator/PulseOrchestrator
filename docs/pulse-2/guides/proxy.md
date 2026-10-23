# Proxy and routing

Pulse runs one Velocity proxy: the group with `software = "velocity"`. Players connect to it, and the `pulse-velocity` plugin sends them on.

```toml
# pulse.toml
[proxy]
port = 25565
lobby = ["lobby"]
fallback = ["lobby", "survival"]
maintenance_message = "We are updating the network. Back in a few minutes!"
maintenance_bypass = "pulse.maintenance.bypass"
```

## Routing

- **Joining:** players go to a running server of the `lobby` groups, the one with the fewest players. If no lobby runs, they are told to come back later.
- **Kicked or crashed server:** players move to a server of the `fallback` groups (without `fallback`: the lobby groups).
- **`/hub`** (also `/lobby`, `/l`) takes a player back to a lobby.

The plugin registers every running Paper, Purpur, Folia and Fabric server in Velocity under its service id, so `/server lobby-1` works as usual. Servers appear when they are ready and disappear when they stop; Velocity never needs a reload.

```bash
pulse proxy status
```

shows which servers the proxy routes to and which count as lobby and fallback.

## Forwarding

Pulse sets up Velocity's modern forwarding with one secret per installation (`forwarding.secret` in the Pulse directory): in `velocity.toml`, in Paper's `config/paper-global.yml`, and for Fabric with the FabricProxy-Lite mod. Velocity checks the player's account; the servers trust Velocity.

Vanilla servers cannot receive forwarded players and are not routed. Without a velocity group there is no forwarding, and because servers listen on `127.0.0.1` only, they cannot be reached from outside.

## Maintenance mode

```bash
pulse proxy maintenance on
pulse proxy maintenance off
```

While maintenance is on, only players with the `maintenance_bypass` permission can join; everyone else sees `maintenance_message`.

## Moving players

```bash
pulse player list
pulse player send Notch bedwars-2
```

`player list` shows players reported by the `pulse-paper` plugin. Plugins can move players with [`PulseApi`](../plugins/pulse-api.md).
