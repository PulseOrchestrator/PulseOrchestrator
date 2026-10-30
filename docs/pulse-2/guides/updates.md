# Updates

## Updating Pulse

```bash
pulse self-update --check   # only report
pulse self-update
```

`self-update` installs the newest release of the same major version:

1. It downloads `SHA256SUMS` and checks its Ed25519 signature against the key built into Pulse.
2. It downloads the binary and checks it against `SHA256SUMS`.
3. It replaces the binary and keeps the previous one as `pulse.old` next to it.
4. It restarts the daemon in place. Servers keep running and the new daemon takes them over.

Nothing changes if a signature or checksum does not match. Pre-releases are only installed with `--pre` or when a pre-release is already installed. A new major version is installed by hand.

The binary must be writable by the user running the command. A binary in the Pulse directory, as in [Install](../getting-started/install.md), is. With `/usr/local/bin/pulse` owned by root, run it as root or keep the binary in the Pulse directory.

To go back, replace `pulse` with `pulse.old` and run `pulse daemon restart`.

## Updating servers

Server builds are pinned. `pulse group update <name>` (or `u` in the TUI) resolves the newest build of the group's `version` and uses it from the next start:

```bash
pulse group update lobby
pulse service restart lobby-1
```

Java runtimes follow the server: a new build that needs a newer Java gets it on its next start.
