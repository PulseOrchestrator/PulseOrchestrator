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

## Release verification

No setup is required beyond starting the official Launcher. It contains the official raw GitHub manifest endpoint, the allowed GitHub Release download path, and the public Ed25519 verification key. The orchestrator setting is used to discover and display update information; the Launcher independently loads the official manifest, verifies `release-manifest.json.sig`, and validates every downloaded JAR with its SHA-256 checksum and detached Ed25519 signature.

## Check and apply

Use the orchestrator console:

```text
system status
system check-update
system update
```

`system status` should show `LAUNCHER_MANAGED` and a `LIVE` host before you start an update. `system check-update` fetches the safety policy and release information without changing the runtime. `system update` checks again and creates a small request containing only the selected target version, channel, source version, timestamp, and request ID. The Launcher independently reloads the built-in signed manifest source and reclassifies the mode before it downloads anything.

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
4. Launcher checks request freshness and source version, verifies `release-manifest.json.sig` against its compiled Ed25519 key, rejects HTTP or foreign release paths, then downloads the target orchestrator JAR and verifies its SHA-256 checksum plus detached signature.
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

After confirmation, Pulse atomically records the queued update ID, the running services, and proxy state in a one-time restore plan before stopping the runtime. The Launcher requests a controlled host drain and waits for the final operation to confirm that no service or proxy child remains. It then verifies that the old host process and session are gone before starting the replacement host, activates the required artifacts, and consumes the plan as the control plane returns. Verify every expected service and the proxy after startup.

!!! warning "Maintenance validation"
  Confirm that old Java processes exited, that only the previously running services returned once, and that intentionally stopped services remain stopped after the next restart. Do not start a second Launcher or recover manually while the controlled host drain is still in progress.

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

The Launcher treats the local update request as a selector, not as authority for URLs, hashes, or update mode. It accepts only a fresh request for the active source version, then independently reloads its built-in official HTTPS manifest URL. The exact manifest bytes and every required artifact signature must verify with the compiled Ed25519 public key. Initial artifact URLs must use the official GitHub Release path; GitHub's HTTPS CDN redirects are then accepted while the final JAR is still checked against its detached signature and SHA-256 hash. A wrong hash, missing signature, invalid signature, HTTP URL, foreign release path, stale request, unsafe control permission, or inconsistent release metadata fails closed without artifact activation.

Keep the Pulse home folder restricted to the dedicated runtime account. The Launcher verifies `runtime/control` before each managed start and refuses an unsafe owner, permission mode, ACL, or symbolic link.
