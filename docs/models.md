# DSMC2 Model Family

## The bodies

DSMC2 is RED's second-generation "DSMC" (Digital Still and Motion Camera)
modular body. One brain, interchangeable sensors and accessories. The main
retail variants:

| Body | Sensor | Format |
|---|---|---|
| SCARLET-W | 5K Super35 (Dragon) | S35 |
| RAVEN | 4.5K Super35 (Dragon) | S35 |
| WEAPON / DSMC2 (Dragon-X) | 5K / 6K Super35 (Dragon family) | S35 |
| DSMC2 GEMINI | 5K Super35 (dual-sensitivity) | S35 |
| DSMC2 HELIUM | 8K Super35 | S35 |
| DSMC2 MONSTRO | 8K Vista Vision | Full-frame-ish (VV) |

The reference body for this research is a **SCARLET-W 5K** (sensor 5120×2700).

## How the camera knows which model it is

This is the interesting part for anyone looking at crossgrades:

- The **application binary and the bootloader are the same** across models.
  A multi-model ("combo") firmware package is a table of contents pointing at
  per-model slices, but the program image itself is shared.
- The model identity lives in **data, not code**: a small number of rows in the
  factory settings database plus a camera-type byte.
- Firmware images are packaged **per model** inside a combo, but each slice is
  the same program with different manifests and resource files.

**Implication.** What distinguishes a cheaper body from a dearer one is largely
configuration and resource manifests, not silicon — *within a sensor family*.
What you **cannot** fake is the sensor itself: a 5K body has a 5K sensor and no
amount of configuration turns it into 8K. Frame-rate caps, format options, and
similar software-gated limits are a different story from raw sensor resolution.

## Manifests

Per-model behaviour is driven by resource manifests bundled in each firmware
slice (lens tables, format tables, feature gates). These are plaintext XML
inside the firmware filesystem, which is why model differences are legible.
