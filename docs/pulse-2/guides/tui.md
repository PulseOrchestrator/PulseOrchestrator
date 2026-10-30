# Terminal UI

`pulse` without a command opens the TUI. It shows every group with its services, details of the selected service and its live console.

```text
 ◆ pulse   2/3 running · 6 players · RAM 1.2/2.0 GB        ● daemon
╭ Services ──────────────────╮╭ lobby-1 ───────────────────────────╮
│  ▾ proxy  velocity    1/1  ││  RUNNING   26.3#214 · port 30000   │
│    ● proxy-1               ││ players 3/20 · TPS 19.8 · RAM ▰▰▰▱▱│
│  ▾ lobby  paper       1/2  │╰────────────────────────────────────╯
│  ▌ ● lobby-1            3  │╭ Console · lobby-1 ─────── follow ╮
│    ◐ lobby-2     starting  ││ [12:01:03 INFO]: Done (4.2s)! …  │
╰────────────────────────────╯╰──────────────────────────────────╯
 ❯ press : to send a command to lobby-1
 s start  x stop  r restart  : command  u update  m maintenance  ? help
```

| Symbol | Status |
|---|---|
| ● | running |
| ◐ (animated) | preparing or starting, or stopping |
| ✕ | crashed or failed to start, waiting for the next attempt |
| ○ | stopped |

## Keys

| Key | Action |
|---|---|
| ↑ ↓, `j` `k` | Select a group or service |
| `s` `x` `r` | Start, stop, restart. On a group: all its services |
| `:` or Enter | Send a console command to the selected service (↑ ↓ for history, Esc to go back) |
| PgUp PgDn, End | Scroll the console, follow new output again |
| `u` | Update the group to the newest build |
| `n` | Create a group |
| `e` | Edit the selected group |
| `D` or Delete | Delete the selected group: `y` keeps the service directories, `d` deletes them too (static groups) |
| `m` | Switch maintenance mode |
| `?` | Help |
| `q` | Quit. Servers keep running |
| `Q` | Shut down: stop every server and the daemon (asks first). Starting the daemon again with `d` starts the same servers |

Without a running daemon the TUI shows the Pulse directory and starts the daemon on `d`.

In a directory without `pulse.toml` and groups, the TUI first shows the setup of `pulse init`: accept the EULA, choose the port, the lobby software and its memory, and `enter` writes the network and starts the daemon, the proxy and the lobby. `esc` skips it.

Everything the TUI does is also a [command](commands.md).
