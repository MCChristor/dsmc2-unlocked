# Scope and Contributions

This repo is **documentation only** and intentionally high-level.

## Do not submit
- Private keys, key material, or exact key addresses.
- Firmware images, RAM dumps, or filesystem mirrors.
- Ready-to-run exploit code or a firmware re-signing recipe.

The `.gitignore` blocks the common offenders (`*.der`, `*.bin`, `*.mem`, dump
folders). Do not force-add them.

## Welcome
- Corrections and clarifications to the writeups.
- Additional model / SSD compatibility data points.
- Firmware, coprocessor, and calibration findings (format-level, no keys).
- Hardware notes (adapter boards, connectors, bench setups).

## Why the restraint
This repo documents the DSMC2 platform broadly — the SoC and OS, the model
family, firmware packaging, calibration and coprocessors, and media. RED
discontinued the DSMC2 and its media, so the work exists to keep owned hardware
alive: repair, preservation, and understanding. Keeping keys and turnkey
exploits out keeps it that way.
