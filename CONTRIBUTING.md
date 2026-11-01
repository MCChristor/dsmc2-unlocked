# Scope and Contributions

This repo documents the RED DSMC2 platform and ships the tools, keys, and methods
to repair and preserve it. Corrections and new data points are welcome.

## Welcome
- Corrections and clarifications to the writeups.
- Additional model / SSD compatibility data points.
- Firmware, coprocessor, and calibration findings.
- Hardware notes (adapter boards, connectors, bench setups).
- Tool fixes and improvements.

## Please don't commit
- **Large binaries** — firmware images, RAM dumps, filesystem mirrors, raw NAND.
  They bloat the repo and are not needed to explain a finding. Describe them, link
  them, or extract the relevant bytes instead. The `.gitignore` blocks the common
  offenders (`*.bin`, `*.mem`, dump folders); don't force-add them. The two small
  firmware RSA keys under `tools/fw-crypto/` are the deliberate exceptions.
- **Anything from hardware you don't own.** This work is on the author's own
  cameras. Keep it that way.
- **RED's package signing private key.** Nobody has it (the camera holds none),
  and this project does not need it — see [docs/keys.md](docs/keys.md).

## Why this exists
RED stopped selling DSMC2 bodies in 2022 and has discontinued the MINI-MAG media
(repair parts no longer available). The point of this repo is to keep owned
hardware alive: repair, preservation, and understanding.
