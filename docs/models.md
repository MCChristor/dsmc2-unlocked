# DSMC2 Model Family

## The bodies

DSMC2 is RED's second-generation DSMC modular body. "DSMC" means Digital Still and
Motion Camera. One brain takes interchangeable sensors and accessories. The main
retail bodies are:

| Body | Sensor | Format |
|---|---|---|
| SCARLET-W | 5K Super35 (Dragon) | S35 |
| RAVEN | 4.5K Super35 (Dragon) | S35 |
| WEAPON / DSMC2 (Dragon-X) | 5K / 6K Super35 (Dragon family) | S35 |
| DSMC2 GEMINI | 5K Super35 (dual-sensitivity) | S35 |
| DSMC2 HELIUM | 8K Super35 | S35 |
| DSMC2 MONSTRO | 8K Vista Vision | VV |

The reference body for this research is a **SCARLET-W 5K**. Its sensor is
5120×2700.

### Camera-type tags

Inside a combo firmware package each model is a slice with a camera-type tag. The
same value appears at runtime as `CAMERA_TYPE` in `/env`. The tags seen in the
7.4.1 combo:

| tag | factory type | camera ID |
|---|---|---|
| `0x11` | WEAPON | WEAPON |
| `0x14` | WEAPON | WEAPON (second sensor variant; same `factory.db` as `0x11`) |
| `0x15` | WEAPON | RAVEN |
| `0x16` | SCARLET_WEAPON | SCARLETW |
| `0x17` | EPIC-W | EPIC-W |

How this value drives identity and what it does *not* change (capability, sensor)
is covered in [feature-unlock.md](feature-unlock.md).

## How the camera knows which model it is

This part matters for crossgrades:

- The **application binary and the bootloader are the same** on every model. A
  multi-model ("combo") firmware package is a table of contents. The table points
  at one slice per model. The program image is shared.
- The model identity is **data, not code**. It is a few rows in the factory
  settings database plus one camera-type value.
- A combo packages one slice per model. Each slice holds the same program. Only
  the small per-model data files differ.

## What this means, and what it does not

The model **name** is configuration — the camera-type value selects branding, the
resource manifest, and defaults, and can be changed without swapping the binary
(confirmed). It does **not** follow that one model becomes another: capability is
bounded by the sensor (a 5K body has a 5K sensor; no flag makes it 8K) and by the
per-body hardware-capability flags. The full reasoning, the capability table, and
the "crossgrade gains are unverified on the device" caveat are in
[feature-unlock.md](feature-unlock.md); this page owns only the camera-type tag
table above.

## Per-model data files

Per-model behaviour comes from a small set of data files. In the 7.4.1 package,
the model slices are byte-identical except for eleven files: two rows in the
factory database, eight default presets, and one camera config file. The package
contains **no XML files**. Any XML or manifest data lives on the read-only data
partition of the camera, not in the update package.

So the model differences in the package are small and readable. They are database
rows and text config, not code.

## Firmware timeline (SCARLET-W line)

Release notes from RED's SCARLET-W download page, for the builds in this research.
Function counts (from disassembling each build's application image) track the
changelog — the big feature jump at 7.1.0.1 is a large code jump too.

| Build | Date | Highlights |
|---|---|---|
| 6.3.106 | 2017-12-21 | Standard-OLPF blue-tint fix; 7.5K/MONSTRO display |
| 7.0.2 | — | no release notes published |
| 7.0.3 | 2018-05-21 | DSMC2 BRAIN support; WEAPON→DSMC2 rename in Camera Info |
| 7.0.4 | 2018-08-09 | fixes only: GEMINI green lines, lens-attach freeze, SIGMA 2.0.1, proxy buffer overflow |
| 7.1.0.1 | 2018-11-27 | **largest jump:** MONSTRO flip/mirror, focus peaking, CDL/RMD/LUT import, 5K 4:3, HLG, DNxHD/HR on RAVEN, 30 fps base, more lenses; IPP2 becomes the default pipeline |
| 7.4.1 | 2020-10-19 | 1.8× anamorphic for MONSTRO 8K VV; Zeiss/Fujinon shading; media-mount fix; Output Tone Map default → Medium Contrast; IPP2 LUT output transforms |

The jump from 7.1.0.1 to 7.4.1 added LUTs, overlays, and rear-device firmware and
changed the application image, the factory database, default presets, and several
FPGA/ASIC binaries. Across all these builds the **bootloader is byte-identical**.
