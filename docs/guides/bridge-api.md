# Plugin Bridge API

The **pulse-bridge-api** is a Java library that lets other Paper plugins interact with
PulseOrchestrator at runtime — creating and managing services, reacting to lifecycle
events, routing players, and reading metrics — without making HTTP calls or knowing
anything about the WebSocket API.

The API classes are bundled inside `plugin-paper`, so **no extra jar** needs to be
present on the server. Other plugins depend on the library at compile time only and
receive the implementation through Bukkit's `ServicesManager` at runtime.

---

## Setup

### Maven

```xml
<repository>
    <id>jitpack</id>
    <url>https://jitpack.io</url>
</repository>

<dependency>
    <groupId>de.pulseorchestrator</groupId>
    <artifactId>pulse-bridge-api</artifactId>
    <version>1.0.0-beta.2</version>
    <scope>provided</scope>
</dependency>
```

### Gradle (Kotlin DSL)

```kotlin
repositories {
    maven("https://jitpack.io")
}

dependencies {
    compileOnly("de.pulseorchestrator:pulse-bridge-api:1.0.0-beta.2")
}
```

### `plugin.yml` dependency

Declare a soft-depend so Bukkit loads `plugin-paper` before your plugin:

```yaml
depend:
  - PulseOrchestrator
```

---

## Getting the API instance

```java
import de.pulseorchestrator.api.OrchestratorBridgeApi;
import org.bukkit.plugin.RegisteredServiceProvider;

RegisteredServiceProvider<OrchestratorBridgeApi> rsp =
    getServer().getServicesManager().getRegistration(OrchestratorBridgeApi.class);

if (rsp == null) {
    getLogger().severe("PulseOrchestrator bridge not available");
    return;
}

OrchestratorBridgeApi api = rsp.getProvider();
```

---

## Core concepts

### Services and tasks

A **task** is a blueprint (software, version, memory). A **service** is a live server
instance provisioned from a task. Multiple services can run from the same task.

```java
// List all tasks
List<TaskDto> tasks = api.listTasks();

// Get a specific task
Optional<TaskDto> lobby = api.getTask("lobby");

// List all services
List<ServiceDto> all = api.listServices();

// Filter by status
List<ServiceDto> running = api.listServices(ServiceStatus.RUNNING);

// Services for a specific task
List<ServiceDto> lobbies = api.listServicesForTask("lobby");
```

### ActionResult

Mutating calls return `ActionResult<T>` — a typed result with success/failure status,
an optional data payload, and an error message on failure.

```java
ActionResult<ServiceDto> result = api.createService("lobby");

if (result.success()) {
    ServiceDto service = result.data().get();
    getLogger().info("Created service: " + service.id() + " on port " + service.port());
} else {
    getLogger().warning("Failed: " + result.message());
}
```

---

## Service lifecycle

```java
// Create (starts automatically)
ActionResult<ServiceDto> created = api.createService("lobby");

// Create with a custom name
ActionResult<ServiceDto> named = api.createService("lobby", "lobby-eu-1");

// Start / stop / restart
api.startService(serviceId);
api.stopService(serviceId);
api.restartService(serviceId);

// Recreate from scratch, starting immediately
api.recreateService(serviceId, true);

// Delete
api.deleteService(serviceId);
```

### Async variants

Every lifecycle method has a `*Async` counterpart that returns
`CompletableFuture<ActionResult<...>>`:

```java
api.createServiceAsync("minigame")
   .thenAccept(result -> {
       if (result.success()) {
           // schedule player teleport on the main thread
           Bukkit.getScheduler().runTask(plugin, () -> {
               api.connectPlayerToServer(playerUuid, result.data().get().id());
           });
       }
   });
```

!!! warning
    Futures run on a shared ForkJoinPool thread. Any Bukkit API calls inside
    the callback **must** be dispatched back to the main thread.

---

## Tasks (CRUD)

```java
// Read
List<TaskDto> tasks = api.listTasks();
Optional<TaskDto> task = api.getTask("lobby");

// Create a new task blueprint
TaskDto blueprint = new TaskDto(
    "arena",              // name
    "1v1 arena server",   // description
    ServerSoftware.PAPER, // software
    "1.21.1",             // version
    2048,                 // maxMemoryMB
    512,                  // minMemoryMB
    List.of("pvp"),       // tags
    List.of("arena-base"),// templates
    Map.of()              // environment variables
);
ActionResult<TaskDto> created = api.createTask(blueprint);

// Update
ActionResult<TaskDto> updated = api.updateTask("arena", revisedBlueprint);

// Delete
api.deleteTask("arena");
```

---

## Routing players

```java
// Transfer a player to a specific service
ActionResult<Void> result = api.connectPlayerToServer(player.getUniqueId(), serviceId);
```

!!! note
    The player must be online on the current server. The `serviceId` passed should
    match the name registered with the Velocity proxy (hyphens become underscores).

---

## Service events

React to service lifecycle changes across the entire fleet:

```java
ServiceEventListener listener = event -> {
    getLogger().info(
        event.serviceId() + " changed from " + event.oldStatus()
        + " to " + event.newStatus()
    );
};

api.addServiceEventListener(listener);

// Remove when your plugin disables
@Override
public void onDisable() {
    api.removeServiceEventListener(listener);
}
```

`ServiceEvent` fields: `serviceId`, `oldStatus`, `newStatus`, `timestamp`.

---

## Log streaming

Subscribe to orchestrator log events at one of two levels:

| Level | Description |
|---|---|
| `IMPORTANT` | Warnings, errors, start/stop events |
| `ALL` | Full verbose output from all services |

```java
UUID subId = UUID.randomUUID();

api.addLogListener(subId, LogLevel.IMPORTANT, event -> {
    // event.serviceId(), event.level(), event.category(),
    // event.message(), event.timestamp()
    getLogger().info("[" + event.serviceId() + "] " + event.message());
});

// Check subscription
api.isSubscribed(subId); // true

// Unsubscribe
api.removeLogListener(subId);
```

---

## Backups

```java
// List backups for a service
List<BackupDto> backups = api.listBackups(serviceId);

// Create a backup
ActionResult<BackupDto> backup = api.createBackup(serviceId);
int slot = backup.data().get().slot();

// Rollback to a slot
ActionResult<ServiceDto> rolled = api.rollbackBackup(serviceId, slot);

// Delete a slot
api.deleteBackup(serviceId, slot);
```

---

## Proxy & system status

```java
// Overall fleet health
SystemStatusDto status = api.getSystemStatus();
status.runningServices();  // int
status.usedMemoryMb();     // long (MB)
status.proxy();            // ProxyStatusDto

// Proxy details
ProxyStatusDto proxy = api.getProxyStatus();
proxy.running();   // boolean
proxy.state();     // String ("RUNNING" / "STOPPED" / ...)
proxy.bindPort();  // int

// Proxy routing config
ProxyConfigDto config = api.getProxyConfig();
config.defaultEntryTask();  // String
config.fallbackTasks();     // List<String>
config.routingPolicy();     // String
```

---

## Service metrics

`ServiceDto.metrics()` returns a `ServiceMetrics` instance when the service is running
and has reported metrics to the orchestrator. It is `null` for stopped services or before
the first metric push.

```java
api.getService(serviceId).ifPresent(service -> {
    ServiceMetrics m = service.metrics();
    if (m != null) {
        getLogger().info("TPS: " + m.tps());
        getLogger().info("Players: " + m.onlinePlayers() + "/" + m.maxPlayers());
        getLogger().info("RAM: " + m.ramUsageMb() + " MB");
        getLogger().info("Last updated: " + m.updatedAt());
    }
});
```

All fields are nullable — check before using.

---

## Console

```java
// Send a command to a service
api.sendCommand(serviceId, "say Hello from the API");

// Fetch the last N lines of console output (max 500)
List<String> lines = api.getConsole(serviceId, 50);
```
