# PulseApi for plugins

Plugins on Paper, Purpur and Folia talk to Pulse through `PulseApi`. The `pulse-paper` plugin, which Pulse installs into every such server, provides it.

With it a plugin can:

- list services and see their status, state and player counts,
- start and stop services,
- move players to another server,
- set the state of its own server, e.g. `LOBBY` or `INGAME`, for matchmaking,
- react to changes of any service.

## Setup

Add the API as `compileOnly`; the Pulse plugin provides it at runtime.

```kotlin
repositories {
    maven("https://jitpack.io")
}

dependencies {
    compileOnly("com.github.PulseOrchestrator:pulse-bridge-api:<version>")
}
```

```yaml
# plugin.yml
depend: [PulseOrchestrator]
```

The API is versioned as major.minor (`2.0`, `2.1`, …); `PulseApi.API_VERSION` holds the version your plugin was built against.

## Usage

```java
PulseApi pulse = Bukkit.getServicesManager().load(PulseApi.class);

// The state other plugins see for this server
pulse.setState("INGAME");

// Send a player to a BedWars server that is waiting for players
pulse.services().thenAccept(services -> services.stream()
        .filter(service -> service.group().equals("bedwars"))
        .filter(service -> "LOBBY".equals(service.state()))
        .filter(Service::hasRoom)
        .findFirst()
        .ifPresent(target -> pulse.sendPlayer(player.getUniqueId(), target.id())));

// React to changes
pulse.addListener(service -> getLogger().info(service.id() + " is " + service.status()));
```

| Method | Description |
|---|---|
| `serviceId()` | Id of this server, e.g. `bedwars-2` |
| `services()`, `service(id)` | All services, or one (`Optional.empty()` if unknown) |
| `startService(id)`, `stopService(id)` | Change whether a service runs. Completes when Pulse accepted the request; listen for `RUNNING` to know when players can join |
| `sendPlayer(uuid, serviceId)` | Move an online player through the proxy. The target must be running and routable |
| `setState(state)`, `state()` | This server's state; reaches Pulse within 5 seconds. `null` clears it |
| `addListener(listener)`, `removeListener(listener)` | Called when a service changes status, desired state or state |

`Service` has `id()`, `group()`, `status()`, `running()` (whether it should run), `state()`, `players()`, `maxPlayers()`, and the helpers `isReady()` and `hasRoom()`. `ServiceStatus` is `STOPPED`, `PREPARING`, `STARTING`, `RUNNING`, `STOPPING` or `BACKOFF`.

## Threads

Every call that talks to Pulse returns a `CompletableFuture` and never blocks. Futures and listeners run on a background thread: switch to the server thread (or the region thread on Folia) before touching players or the world. A failed call completes with a `PulseApiException`; its `kind()` says why, e.g. `not_found`, `not_running` or `unavailable` when the daemon cannot be reached.

## Metrics

Independent of your plugin, `pulse-paper` reports players, TPS and memory every 5 seconds. They show up in the TUI, in `pulse service show` and in `Service.players()`.
