# Debug Shell Command Reference

This is a reference for the DSMC2 debug shell (`dsh>`). For how to enable and
reach it, see [serial-shell.md](serial-shell.md). The shell is RED-custom (not a
stock RTOS shell) and has 17 top-level commands. `help <command>` lists each one's
subcommands on the device.

Two rules first, repeated from the access page because they can brick a session:

- **Only read known-valid memory.** `read reg` on `0x80000000–0x81FFFFFF` is safe;
  unmapped or peripheral addresses fault the processor and power the camera off.
- **Never write a register you have not read.** `write` is ungated.

## The 17 commands

| command | what it does |
|---|---|
| `read` | read memory (`read reg <start> [end]`) |
| `write` | write memory (`write <addr> <value>`) |
| `nand` | NAND / filesystem operations |
| `cdb` | settings-database commands |
| `get` / `set` | read / set a parameter |
| `maint` | maintenance: module inventory, logs, board info |
| `test` | low-level test routines |
| `ddr_test` | DDR test settings |
| `media` | media operations |
| `player` / `record_start` | playback and record |
| `wlan` | WiFi / BT / Zigbee chip debug |
| `app_start` | send the START-APP message |
| `debug` | debug functions (many hidden from `help`) |
| `shutdown` | power the camera off |
| `exit` | leave the shell |

## The ones that matter for repair and extraction

### `read` / `write` — live memory

```
read reg 0x80000000 0x80000100     # dump a range of DDR (the running firmware)
write 0x80879300 0xe30d1c1c        # 32-bit write to any address
```

Memory runs from `0x80000000`; `file_offset = VA − 0x80000000` maps an address to
an offset in `dsmc_program.mem`. Over serial, `read reg` moves a few KB/s.

### `cdb` — the settings database

```
cdb sql "SELECT name,value FROM parameters WHERE name LIKE 'DEBUG_%'"
cdb get <parameter>
cdb set <parameter> <value>
cdb apply-preset <name>            # apply a staged preset
cdb export-preset <name>           # write a preset to a SATA SSD (ungated)
```

Use **double quotes** around SQL; the shell splits on spaces. The database holds
~2062 parameters.

### `nand` — filesystem

```
nand ls [path]                     # list
nand info / nand show-partition-table
nand zlib -c <src> <dst>           # decompress a file (how the firmware image is pulled)
nand stats / df / du / mark-block
```

`nand zlib` is the extraction workhorse: it decompresses a NAND file to a path you
can then pull over WiFi with RFTP. Five subcommands (`cat`, `cp`, `mv`, `base64`,
`show-sector`) are compiled out and only print a `#define` message — see
[serial-shell.md](serial-shell.md).

### `maint` — modules, logs, identity

```
maint module                       # every attached module + SW/HW version
maint save_log                     # write the decrypted log to a SATA SSD (ungated)
maint print_boot_log
```

`maint save_log` plus the [log decoder](log-decode.md) is the clean way to get a
readable boot log. `maint module` is the tool for module pairing and repair.

### `test` — hardware diagnostics

```
test sata active smartlogpage 0x90 # read a mag's SMART signature page (media auth)
pcs_loop_back                      # ISP transceiver loopback (undocumented, in-binary)
xaui_dma_loopback <size> <iters>   # IOB-ISP DMA loopback
```

The `test` routines (and the undocumented loopback commands) are what localize a
fault on a dead body — they split a bad ISP link from a bad board without the full
boot path.

### `debug` — hidden switches

Most `debug` subcommands are omitted from `help` but exist in the command table.
They back the `DEBUG_*` CDB parameters, for example `debug hw_cap` (dump/set the
capability table), `debug log_to_shell`, `debug mfg_features_enabled`. See
[feature-unlock.md](feature-unlock.md).
