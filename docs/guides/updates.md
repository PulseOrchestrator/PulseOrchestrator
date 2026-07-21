# Updating Pulse

Pulse uses release metadata to decide whether a new orchestrator can be activated while the Minecraft network stays online or whether the complete runtime needs maintenance.

## Before enabling updates

Launcher-managed updates require:

- Windows and Java 21;
- startup through the Launcher, not directly through the orchestrator JAR;
- a writable Pulse home folder;
- access to the public GitHub release and raw manifest URLs; and
- an update configuration with checks enabled and a release manifest URL.

Example:

```json
{
  "updates": {
    "enabled": true,
    "checkOnStartup": true,
    "autoApply": false,
    "includePrereleases": false,
    "checkIntervalHours": 12,
    "runtimeWarningIntervalHours": 8,
    "githubOwner": "PulseOrchestrator",
    "githubRepo": "PulseOrchestrator",
    "policyUrl": "https://raw.githubusercontent.com/PulseOrchestrator/PulseOrchestrator/refs/heads/main/update-policy.json",
    "releaseManifestUrl": "https://raw.githubusercontent.com/PulseOrchestrator/PulseOrchestrator/refs/heads/main/release-manifest.json"
  }
}
```

Keep `autoApply` disabled when you want every update to be operator-initiated. When enabled, only warm updates may be applied automatically. Maintenance updates always require manual confirmation.

Set `includePrereleases` to `true` only for beta installations. Stable installations should leave it disabled.

## Check and apply

Use the orchestrator console:

```text
system status
system check-update
system update
```

`system status` should show `LAUNCHER_MANAGED` and a `LIVE` host before you start an update. `system check-update` fetches the safety policy and release information without changing the runtime. `system update` checks again, creates a request for the Launcher, and then follows the mode declared by the release.

The update can have one of three results:

| Mode | Downtime | Behavior |
|---|---|---|
| `WARM_UPDATE` | Orchestrator API/CLI restarts briefly; services and proxy stay online | Only explicitly complete and compatible protocol/persistence metadata permits the orchestrator artifact to activate, then it reattaches to the existing Runtime Host |
| `MAINTENANCE_UPDATE` | Services and proxy stop | After confirmation, the runtime stops, required artifacts are activated, and a request-bound plan restores only the previously running proxy and services once |
| `UNSUPPORTED` | None | Pulse explains the blocking reason and makes no change |

## Warm update flow

1. Orchestrator verifies that the target release has complete, internally consistent protocol metadata and an explicitly backward-compatible persistence model for the installed Runtime Host.
2. Orchestrator queues an update request and shuts down only its API, CLI, health monitor, and other control-plane components.
3. Runtime Host keeps Velocity and Minecraft service JVMs running.
4. Launcher downloads the target orchestrator JAR and verifies its SHA-256 checksum.
5. Launcher stores the JAR under `runtime/versions/`, updates `runtime/current-release.json`, and starts it.
6. The new orchestrator reconnects to the Runtime Host and regains live control.

If the new orchestrator exits with an error in the first 20 seconds, the Launcher can make one best-effort attempt to reactivate the previous orchestrator JAR. Services remain under the same Runtime Host during this attempt.

!!! warning "Rollback limits"
    Warm rollback does not undo configuration, task, or database migrations. It also does not cover failures that appear after the startup window. Release compatibility is the primary safety mechanism; rollback is a last recovery attempt.

## Maintenance update flow

A Runtime Host update, incompatible host protocol, or non-backward-compatible persistence change requires maintenance.

Before confirming:

1. notify players;
2. create backups of `pulse.db`, `config.json`, `tasks.json`, `services/`, and `proxy/`;
3. verify enough disk space exists for old and new versioned JARs plus service backups; and
4. keep direct terminal access to the host.

After confirmation, Pulse atomically records the queued update ID, the running services, and proxy state in a one-time restore plan before stopping the runtime. It activates the required orchestrator and Runtime Host artifacts, then consumes that plan as the control plane returns. Verify every expected service and the proxy after startup.

!!! warning "Maintenance validation"
  Confirm that old Java processes exited, that only the previously running services returned once, and that intentionally stopped services remain stopped after the next restart. Host stop acknowledgement remains a beta limitation.

## Verify an update

After either update type:

1. Run `system status` and confirm the host is `LIVE`.
2. Compare the expected running service count.
3. Attach to one service or request its console tail and confirm new lines arrive.
4. Send a harmless command such as `list` and verify its response.
5. Confirm players can connect through the proxy.
6. Review `logs/` and the Launcher/Runtime Host terminal output for errors.
7. Inspect `runtime/current-release.json` only when troubleshooting; do not edit it during normal operation.

For a warm update, service and proxy PIDs should remain unchanged. For a maintenance update, new PIDs are expected.

## When the host is unavailable

If `system status` reports `HOST_UNAVAILABLE`:

- do not assume persisted `RUNNING` states prove that processes are controllable;
- do not start duplicate services manually on the same ports;
- preserve the terminal output and `logs/`;
- inspect the process list for the Launcher, Runtime Host, orchestrator, Velocity, and service JVMs; and
- plan a controlled full restart if the Runtime Host cannot be recovered.

The orchestrator cannot reconstruct lost stdin/stdout handles from a PID alone.

## Manual recovery

If the Launcher cannot activate a release:

1. Stop the complete Pulse runtime and confirm all child Java processes have exited.
2. Back up the Pulse home folder before changing control files.
3. Preserve `runtime/current-release.json`, `runtime/control/`, and logs for diagnosis.
4. Restore the previous known-good orchestrator and Runtime Host JARs from `runtime/versions/` only while Pulse is fully stopped.
5. Restore database/config/service backups when the release included incompatible migrations.
6. Start through the Launcher and verify `system status` before admitting players.

Do not replace an artifact in `runtime/versions/` while Pulse is running. Do not delete `pulse.db` to resolve an update problem.

## Security properties

The current updater verifies downloaded JARs with SHA-256 values from the release manifest. Detached signature URLs are part of the manifest model, but signature verification is not yet enforced by the Launcher. SHA-256 detects an artifact that differs from the manifest; it does not protect against a compromised manifest that supplies both a malicious URL and matching hash.

Use only the official HTTPS manifest and release URLs, protect the GitHub maintainer accounts, and restrict the Pulse home folder to the dedicated runtime account.
