# Install Guide

This guide is for operators who download the released jars and want to get PulseOrchestrator running.

## What you need

- Java 21 on the machine that runs the orchestrator
- the released orchestrator jar
- the released Paper plugin jar if you want Paper integration
- the released Velocity plugin jar if you want standalone Velocity integration

## Download the release files

From the release page, download the jars you need:

- the orchestrator jar
- the Paper plugin jar
- the Velocity plugin jar if you use it

Create a persistent folder for the orchestrator runtime, for example:

```text
D:\PulseOrchestrator\
```

That folder becomes the base path where PulseOrchestrator stores its configuration, database, templates, services, proxy files, and logs.

## Start the orchestrator

Run the orchestrator jar.

### Windows

```powershell
java -jar pulseorchestrator-orchestrator-<version>-all.jar
```

### Linux with screen

```bash
screen -S pulse-orchestrator java -jar pulseorchestrator-orchestrator-<version>-all.jar
```

## What happens on first start

On the first launch, PulseOrchestrator opens the setup wizard instead of starting directly.

The wizard walks through these steps:

### 1. API configuration

You choose:

- the API port
- the bind address

An API secret is generated automatically.

### 2. Java configuration

You provide:

- the Java executable path
- the default maximum memory in MB
- the default minimum memory in MB

These values are used as the baseline for provisioned services.

### 3. Service port range

You define the port range that PulseOrchestrator can use for managed services.

### 4. Proxy setup

You choose the bind port for the built-in Velocity proxy.

In `1.0.0`, the built-in proxy is required by the setup flow. The forwarding secret is generated automatically.

### 5. Minecraft EULA confirmation

You must accept the Minecraft EULA to continue.

### 6. Runtime file creation

The wizard creates the runtime structure and writes the first configuration files.

After setup, the base path contains:

```text
<basePath>/
  config.json
  tasks.json
  pulse.db
  templates/
    global/
  services/
  server-jars/
  proxy/
  logs/
```

The generated API secret is stored in `config.json`.

## Configure the plugins

After the orchestrator has completed setup, copy the API URL and API secret into the plugins that should connect to it.

The default local API URL is:

```text
http://localhost:8080
```

### Paper plugin

Put the Paper jar into your Paper server `plugins` folder, start the server once, and then update its config:

```json
{
  "orchestratorUrl": "http://localhost:8080",
  "apiSecret": "copy-from-config-json"
}
```

### Velocity plugin

If you use the standalone Velocity plugin, put its jar into the Velocity `plugins` folder, start Velocity once, and then update its config:

```json
{
  "orchestratorUrl": "http://localhost:8080",
  "apiSecret": "copy-from-config-json",
  "pollIntervalSeconds": 5,
  "connectionTimeoutMs": 5000,
  "readTimeoutMs": 10000
}
```

## Next step

Once installation is complete, the next job is to define your first task blueprints and create services from them. That workflow is covered in the [Feature Guide](../guides/feature-guide.md).
