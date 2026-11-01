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

**What this does and does not mean.** The model *name* is config: the camera-type
value selects which branding, resource manifest and defaults apply, and it can be
changed without swapping the binary. That is confirmed.

It does **not** follow that any model becomes any other. Two things gate what a
given body can actually do:

- **The sensor.** A 5K body has a 5K sensor; no configuration turns it into 8K.
  Different models in the lineup use genuinely different sensors (Dragon, Helium,
  Gemini, Monstro), so resolution and sensor behaviour are hardware, not a flag.
- **Hardware-capability flags.** Features above the base model are gated by
  per-body capability flags, not by the model name alone. Flipping the
  camera-type does not by itself grant a capability the board does not report.

So the honest summary is narrower than "it's all config": the **identity** is
config, but **capability** is bounded by the sensor and the hardware-capability
flags. What is realistically unlockable is the software-gated layer — frame-rate
caps and format options on hardware that already supports them — not a jump to a
different sensor class. The exact per-model capability differences were **not**
fully mapped from the device, so treat crossgrade feature gains as unverified.

## Manifests

Per-model behaviour is driven by resource manifests bundled in each firmware
slice (lens tables, format tables, feature gates). These are plaintext XML
inside the firmware filesystem, which is why model differences are legible.
