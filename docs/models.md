# DSMC2 Model Family

Written in simplified technical English.

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

## How the camera knows which model it is

This part matters for crossgrades:

- The **application binary and the bootloader are the same** on every model. A
  multi-model ("combo") firmware package is a table of contents. The table points
  at one slice per model. The program image is shared.
- The model identity is **data, not code**. It is a few rows in the factory
  settings database plus one camera-type value.
- A combo packages one slice per model. But each slice is the same program with
  different manifests and resource files.

## What this means, and what it does not

The model **name** is configuration. The camera-type value selects the branding,
the resource manifest, and the defaults. You can change it without swapping the
binary. This is confirmed.

It does **not** follow that one model becomes another. Two things set what a body
can actually do:

- **The sensor.** A 5K body has a 5K sensor. No configuration turns it into 8K.
  Different models use genuinely different sensors (Dragon, Helium, Gemini,
  Monstro). So resolution and sensor behaviour are hardware, not a flag.
- **Hardware-capability flags.** Features above the base model are gated by
  per-body capability flags, not by the model name. A changed camera-type does not
  by itself grant a capability that the board does not report.

So the honest summary is narrow. The **identity** is configuration. The
**capability** is bounded by the sensor and the hardware-capability flags. The
software-gated layer is the realistic unlock target. That means frame-rate caps and
format options on hardware that already supports them. It does not mean a jump to a
different sensor class. The exact per-model capability differences were **not**
fully mapped from the device. So treat crossgrade feature gains as unverified.

## Manifests

Resource manifests drive per-model behaviour. Each firmware slice bundles them.
They hold lens tables, format tables, and feature gates. They are plain-text XML in
the firmware filesystem. This is why the model differences are readable.
