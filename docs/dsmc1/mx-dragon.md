# DSMC1 MX / Dragon (EPIC · SCARLET · Dragon)

Same architecture as DSMC2, one generation apart. The firmware container, its
encryption, the main processor family and the coprocessor design are shared. The
differences are in *how many* of each part the body has and which extra chips are
present.

Reference image: **Epic Dragon build v6.3.106** (camera-type tag `0x0f`, released
2017-12-20) — the last build for EPIC, SCARLET and Dragon. 333 files in the
package.

## What is identical to DSMC2

- **Firmware container.** MX/Dragon updates are the same `DSMC`-magic **v2**
  package as DSMC2 single-model updates. See [firmware.md](../firmware/firmware.md).
- **Encryption and keys.** The v2 package uses the same RSA-OAEP(SHA-1, label
  `dsmc`) → RC4 design and opens with the **same published v2 key** — no new key
  material is needed. Verified by unpacking Epic Dragon 6.3.106 with the
  repository's own [unpacker](../../tools/fw-crypto). See [keys.md](../firmware/keys.md).
- **Config-file cipher.** The `.cfg` files (camera config, lens tables) use the
  same reused-keystream stream cipher, so the same recovered keystream reads DSMC1
  configs too. See [feature-unlock.md](../features/feature-unlock.md).
- **Main processor.** TI OMAP-class ARM running `dsmc_program.mem`, same as DSMC2.
- **ISP and IOB run Xtensa code, loaded from NAND.** DSMC1's `CAMERA_CONFIG.cfg`
  names the loader paths `TENSILICA_ISP_BIN_PATH` and
  `TENSILICA_IOB0/IOB1/PROIO_IOB0_BIN_PATH`, and the ISP instruction-RAM bootstrap
  is byte-identical to DSMC2 — so both generations use the same part. The image
  disassembles cleanly as Xtensa (see [platform.md](../platform.md)), which
  confirms the ISA. **Fabric type (ASIC vs FPGA) is still not settled by the
  firmware** — Xtensa runs in both, and the image uses both words.

Because the container, keys, config cipher, shell and subsystem layout all carry
over, most of this repository — [feature-unlock.md](../features/feature-unlock.md),
[serial-shell.md](../access/serial-shell.md), [shell-commands.md](../access/shell-commands.md),
[calibration.md](../features/calibration.md), [subsystems.md](../features/subsystems.md) — reads
across to MX/Dragon bodies with the counts adjusted below.

## Inside the image

The v2 package unpacks to the same directory layout as a DSMC2 image, so anything
the DSMC2 docs say about these trees applies here too:

| Dir | Contents | Same on DSMC2? |
|---|---|---|
| `dsmc_program.mem` | main ARM application (~17.7 MB) | yes (DSMC2 ~21.6 MB) |
| `cdb2/` | parameter / factory database | yes |
| `cfg/` | camera config (`CAMERA_CONFIG.cfg`, RC4) | yes |
| `isp/`, `iob0/`, `proio_iob0/` | Xtensa `iram.bin`+`dram.bin` per core | yes (DSMC2 adds `iob1/`) |
| `dsp/` | `rdc_dsp_app.out` (C64x DSP app) | yes |
| `fpga/` | `Genlock_Top.bin` | genlock only (DSMC2 adds LSB Kintex-7) |
| `lens/` | `canon_mount` / `nikon_mount` lens tables | yes |
| `luts/` | IPP2 preview `.cube` LUTs | yes |
| `peripherals/` | EVF (`wevf_fpga`), accessory firmware | yes |
| `overlays/`, `res/`, `doc/` | overlays, resources, docs | yes |
| **`turret4k/`** | `rtrt4k.1.bin` — DSMC1 UI tree | **no — DSMC2 uses FlatUI** |

The `bootloader_0x0f.bin` is 118082 B; the DSMC2 bootloader is close but not
identical (the per-model filename carries the camera-type tag, as on DSMC2).

## Camera-type tags

DSMC1 MX/Dragon bodies carry their own camera-type bytes in the same namespace as
the DSMC2 crossgrade variable (see [feature-unlock.md](../features/feature-unlock.md)):

| Tag | Body |
|---|---|
| `0x0f` | EPIC DRAGON (reference image above) |

Other MX/Dragon tags appear in the same table as the DSMC2 `weapon`-family tags;
the DSMC1 bodies are **not** the DSMC2 Epic-W / Scarlet-W, which are the `weapon`
family (`0x11`/`0x16`/`0x17`).

## What differs from DSMC2

| | DSMC1 (Epic Dragon) | DSMC2 (Scarlet-W) |
|---|---|---|
| IOB cores | **1** (`iob0`) | **2** (`iob0`, `iob1`) |
| Large FPGA | genlock FPGA only | + **LSB Xilinx Kintex-7** |
| Wireless | none in the image | **Redpine** Wi-Fi/BT module |
| Coprocessor topology | 2 ISP, 1 IOB, 60 ISP slices | 2 ISP, 1 IOB, 60 ISP slices (same shape) |
| Application image | ~17.7 MB | ~21.6 MB |
| UI tree | `turret4k/` | FlatUI, more rear devices |

The ISP/IOB **instruction images differ build-to-build** (different sizes), as
expected; it is the *encoding and bootstrap* that are shared, not the exact bytes.

## Getting and opening the firmware

RED distributes these builds through its own firmware download page. The relevant
bodies are **Epic Dragon**, **Epic (M-X)** and **Scarlet (M-X)**; the last build
for all three is v6.3.106.

Each download is a `.zip` holding a read-me and one `force_upgrade/*.bin`. The
`.bin` is the v2 package; unpack it with
[tools/fw-crypto/unpack_combo.py](../../tools/fw-crypto):

```
python3 unpack_combo.py epic_dragon_6.3.106.bin --extract --out out/
```
