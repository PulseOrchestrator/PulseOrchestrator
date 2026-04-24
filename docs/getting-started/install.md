# Install Guide

PulseOrchestrator is a server network manager for Minecraft. It runs on your machine and handles starting, stopping, and monitoring your game servers automatically — you do not need to manage each server by hand.

This guide walks you through installing and starting it for the first time.

---

## What you need

Before you start, make sure you have:

- **Java 21** — the program that runs PulseOrchestrator and your game servers. You can check your version by opening a terminal and typing `java -version`. If you see `21` or higher you are good.
- **The orchestrator jar** — the main PulseOrchestrator file, downloaded from the releases page.
- **The Paper plugin jar** *(optional)* — only needed if you want in-game commands on Paper servers.

!!! tip "Where to find the jars"
    All release files are available on the [GitHub releases page](https://github.com/PulseOrchestrator/PulseOrchestrator/releases). Download the files that match the version you want to run.

---

## Create a home folder

PulseOrchestrator needs a dedicated folder to store everything: your configuration, your server files, logs, and backups. Create an empty folder somewhere permanent.

=== "Windows"
    ```text
    C:\PulseOrchestrator\
    ```

=== "Linux"
    ```text
    /home/yourname/pulseorchestrator/
    ```

Copy the orchestrator jar into that folder.

!!! warning "Keep this folder in a safe place"
    Do not put it in a temporary or download folder. All your server data will live here.

---

## Start the orchestrator

Open a terminal, navigate into your folder, and run the jar.

=== "Windows"
    ```powershell
    java -jar orchestrator-<version>.jar
    ```

=== "Linux (foreground)"
    ```bash
    java -jar orchestrator-<version>.jar
    ```

=== "Linux (background with screen)"
    `screen` keeps the program running after you close your SSH connection.

    If you do not have screen installed: `sudo apt install screen`

    ```bash
    screen -S pulse
    java -jar orchestrator-<version>.jar
    ```

    To leave the screen running in the background: press ++ctrl+a++ then ++d++.

    To come back to it later: `screen -r pulse`

!!! note
    Replace `<version>` with the actual version number, for example `orchestrator-1.0.0-beta.1.jar`.

---

## First-time setup wizard

On the very first start, PulseOrchestrator detects that it has no configuration yet and runs an interactive setup wizard. It will ask you a series of questions. You can press ++enter++ on most of them to accept the suggested default.

### Step 1 — API settings

The API is how PulseOrchestrator communicates with the Minecraft plugins you install. It runs a small web server in the background.

- **API port** — the port number the API listens on. Default is `8080`. Only change this if something else on your machine is already using that port.
- **Bind address** — the network address the API binds to. `127.0.0.1` means it only accepts connections from the same machine. Leave this as the default unless you know what you are doing.

A long random **API secret** is generated for you automatically and saved to `config.json`. You will need to copy this into the plugin configs later.

### Step 2 — Java path

PulseOrchestrator needs to know where Java is installed so it can launch game servers.

- Typing just `java` works if Java is in your system PATH (this is the default on most setups).
- If that does not work, provide the full path: for example `C:\Program Files\Java\jdk-21\bin\java.exe` on Windows or `/usr/bin/java` on Linux.

You also set default memory limits here:

- **Default max memory** — the maximum RAM each game server is allowed to use, in MB. Default is `1024` (1 GB). You can override this per-task later.
- **Default min memory** — the starting memory allocation. Default is `512` MB.

### Step 3 — Port range

PulseOrchestrator assigns a port to each game server it creates, chosen from this range. Players never connect directly to these ports — they connect through the proxy.

- Default range is `25700` to `25800`, which gives room for up to 100 servers.
- Make sure the ports in this range are not blocked by a firewall.

### Step 4 — Proxy port

The built-in proxy is what players actually connect to. It forwards them to the right game server automatically.

- **Bind port** — the port players type when connecting to your network. Default is `25565` (the standard Minecraft port).

### Step 5 — Minecraft EULA

You must accept the [Minecraft End User License Agreement](https://www.minecraft.net/en-us/eula) to run Minecraft servers. The wizard asks for your confirmation before proceeding.

### Step 6 — Done

The wizard writes all your configuration files and creates the folder structure. The orchestrator then starts normally.

---

## Folder structure after setup

Once setup finishes your folder will look like this:

```text
<your folder>/
  config.json          ← main settings (API, memory, ports, etc.)
  tasks.json           ← your server blueprints
  pulse.db             ← database of created services (do not delete)
  templates/
    global/            ← files copied into every new server
  services/            ← the actual running server folders
  server-jars/         ← downloaded server JARs (auto-managed)
  proxy/               ← built-in Velocity proxy files
  logs/                ← orchestrator logs
```

!!! warning "Do not delete pulse.db"
    The `pulse.db` file is the database that tracks all your services. Deleting it means PulseOrchestrator forgets about all existing servers.

---

## Connect the plugins

After the orchestrator is running, any Minecraft plugin that talks to it needs the API address and secret.

You can find the API secret by opening `config.json` and looking for the `apiSecret` field.

The default local API address is:

```text
http://localhost:8080
```

If you are connecting from a different machine (for example a Paper server on another VPS), replace `localhost` with the IP address of the machine running the orchestrator.

### Paper plugin

Put the Paper jar into your Paper server's `plugins/` folder and start the server once to generate the config. Then open `plugins/PulseOrchestrator/config.json` and fill in:

```json
{
  "orchestratorUrl": "http://localhost:8080",
  "apiSecret": "paste-your-secret-here"
}
```

Restart the server after saving.

---

## Next steps

With the orchestrator running, the next step is to define your first **task** (a server blueprint) and create a server from it.

- [Feature Guide](../guides/feature-guide.md) — learn about tasks, services, the proxy, and templates
- [Configuration Reference](../guides/configuration.md) — a full explanation of every setting in `config.json` and `tasks.json`
