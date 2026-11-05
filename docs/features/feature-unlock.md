# Features, Capabilities, and Model Identity

This page explains what separates one DSMC2 model from another, what can be
changed in software, and what is fixed by the hardware. It is the "why" behind the
crossgrade and feature-unlock claims in [whats-possible.md](../whats-possible.md).

## Model identity is configuration

Every model in a generation runs the **same application binary and the same
bootloader** — they are byte-identical across models in a given firmware build.
What differs is small configuration:

- A **camera-type value**. In a firmware package this is the slice's table-of-
  contents tag; at runtime it is the `CAMERA_TYPE` value in the `/env` partition.
  They are the same namespace and agree.
- A few rows in the per-model settings database (`factory.db`): the factory-type
  string and the camera-ID string. For example, a SCARLET-W differs from a WEAPON
  in exactly two of ~2062 parameter rows.

So "which model the camera thinks it is" is just data. Changing it is possible.
But — see below — that does not grant another model's capabilities. The full
camera-type tag table (which tag maps to which factory type and camera ID) is in
[models.md](../models.md#camera-type-tags).

## Capability is not only configuration

Capability is bounded by two things the camera-type value does not change:

1. **The sensor.** Resolution and the sensor family are physical. A 5K body does
   not become 8K by relabelling it. Crossgrades only make sense *inside one sensor
   family*, and only for the software-gated layer on top.
2. **A hardware-capability table.** The firmware carries a **114-entry capability
   table** (`HW_CAP_*`). The `hw_cap` module loads each capability's state from
   **both the settings database and licence files**, keyed to the board identity.
   This is the real feature-gating layer.

A sample of the table (index → capability):

```
  1 HW_CAP_WIFI            7 HW_CAP_3D_LUT        9 HW_CAP_SW
  2 HW_CAP_FIZ             6 HW_CAP_ND_CONTROL   54 HW_CAP_STROBE
  3 HW_CAP_GIG_ETHERNET   38 HW_CAP_SIDE_HANDLE  90 HW_CAP_RETURN_FEED
  4 HW_CAP_TETHERING     107 HW_CAP_SENSOR_SENSITIVITY
111 HW_CAP_ALLOW_UPGRADE_WITH_ENGINEERING_KEY
```

The index is the position in the array, confirmed against the `key_actions` table
in `factory.db` (each UI action stores its own capability index, and every one
matches).

## What each software-gated feature does

Each item below is gated by a capability bit or a manifest entry, not by the
sensor or any other hardware. So on a body whose silicon already supports it, the
gate is what withholds it. These are candidate unlocks; which ones actually turn on
was not all verified on the device (see the status note at the end of this page).

- **3D LUT** (`HW_CAP_3D_LUT`, index 7) — load a 3D colour cube onto the
  monitor/output path, so a graded look is viewed on set. The transform runs in the
  LSB FPGA. Nothing sensor-specific.
- **In-camera IPP2** (`HW_CAP_COLOR_SCIENCE_IPP2`, index 84) — select RED's newer
  colour pipeline (REDWideGamut / Log3G10) in-camera instead of only in post. Gated
  by one capability bit with no sensor branch. Render accuracy on an
  original-DRAGON sensor is still pending a shoot-test; full detail in
  [ipp2.md](ipp2.md).
- **LookAround** — show the sensor area outside the recording frame, for framing
  and watching for boom/rig intrusions. Pure display feature (the look-around bit,
  see [anamorphic.md](anamorphic.md)).
- **ProRes recording** — record Apple ProRes alongside or instead of R3D. The
  encoder is present in the firmware ([platform.md](../platform.md)); the gate is a
  capability flag, not the codec's absence.
- **Anamorphic ratios** — desqueeze preview for anamorphic lenses. The stock ratio
  set is enumerated in a format table; added ratios need a table edit, not only a
  flag (see [anamorphic.md](anamorphic.md)).
- **Higher REDCODE ratios** — the minimum/maximum REDCODE compression offered.
  These are values in a parameter-descriptor table, not a per-model code branch, so
  the offered range is data that can be widened. It is codec compression only,
  independent of the sensor.
- **Extra project frame-rate offerings** — the manifest lists which sensor-FPS
  entries the UI presents. A higher-tier manifest lists more, but only **up to the
  sensor's physical readout ceiling**, which is computed from sensor timing and is
  identical silicon-to-silicon. This exposes offerings; it does not raise the
  hardware limit ([whats-possible.md](../whats-possible.md)).

**Why a SCARLET-W does not show them.** The application binary and bootloader are
identical across models in a build; what differs is the camera-type value, a couple
of settings rows, and which capability bits / manifest entries are set for that
body. A SCARLET-W simply has these bits clear or absent from its manifest. For a
software-gated feature on hardware that supports it, that is the whole difference —
the code and the silicon are the same. This is the observable fact; the commercial
reason RED chose that split is not recorded in the firmware and is not claimed here.

> **Not a software gate — needs the part.** Some capabilities map to hardware a
> given body may lack: `HW_CAP_WIFI` (radio), `HW_CAP_GIG_ETHERNET` (PHY, via an
> expander), `HW_CAP_PRESTON_FIZ` (lens-motor interface), `HW_CAP_SIDE_HANDLE` (the
> attached handle). Setting the bit shows the menu, but the feature only works when
> that hardware is actually present or attached.

## Changing capabilities and debug flags

The settings database (CDB) can be written by a preset, and a preset can therefore
set capability and debug flags the menus hide. Two categories exist:

- **`HW_CAP_<name>` parameters** — set a capability on by writing the matching CDB
  parameter. Some features (anything not bounded by the sensor) flip this way.
- **`DEBUG_*` parameters** — a set of debug switches that also have `debug`
  shell subcommands (most are omitted from `help`). Examples:
  `DEBUG_ENABLE_SHELL`, `DEBUG_LOG_TO_SHELL`, `DEBUG_MFG_FEATURES_ENABLED`,
  `DEBUG_LOAD_ASIC_BINS_FROM_HOST`, `DEBUG_BOOT_TO_SHELL`.

From the debug shell you can also read the whole table live with `debug hw_cap`
and set an index with `debug hw_cap <index> 1`. See
[serial-shell.md](../access/serial-shell.md) and [tools/preset](../../tools/preset) for how to
set them persistently.

> **One capability is special:** index `111`,
> `HW_CAP_ALLOW_UPGRADE_WITH_ENGINEERING_KEY`, gates whether the camera will accept
> a firmware package signed with RED's *engineering* key instead of the release
> key. It is the mechanism behind engineering-signed upgrades. We hold neither
> signing key, so this is noted for completeness, not as a lever — and it does not
> matter, because the bootloader does not verify the installed image at all
> ([platform.md](../platform.md), [keys.md](../firmware/keys.md)).

## The licence system

Some capabilities are loaded from **licence files** (`.key` files on the camera),
not just the settings database. This is the mechanism RED uses to enable paid
feature options per body.

A licence file is **not** plain text. It goes through the firmware's generic key
container: an RSA-encrypted, signature-checked blob that decrypts and decompresses
to a small SQLite database with a `hw_caps` table — the capabilities that file
grants. The chain is SHA-1 + RSA signature verify, then RSA-unwrap a key, then RC4
decrypt, then zlib inflate.

Two things follow from what is in the firmware image:

- **The camera holds private keys.** Several RSA private keys are embedded in the
  image (the generic key/asset keys, separate from the two firmware-package keys in
  [keys.md](../firmware/keys.md)). Because a private key gives its public half, the material to
  *produce* a container the camera will open and trust is on the device.
- **So the licence format is forgeable in principle** — the gate is not a secret
  RED holds alone. What is not yet pinned down is which of the embedded keys a
  licence uses and the exact field layout, so this is **not a turnkey result**.

> **Status: researched, not completed or camera-verified.** The container format
> and primitive chain are read from the firmware; a working forged licence has not
> been produced or tested. Treat this as "the gate is understood and looks
> forgeable", not "here is a licence generator".

For most feature flags you do not need a licence at all — the CDB/preset and
`debug hw_cap` routes above set capabilities directly, which is simpler than
minting a licence. The licence path matters only for capabilities that are loaded
*only* from a licence file.

## What is proven and what is not

- **Proven:** model identity is config; the app binary and bootloader are
  identical across models; the capability table, its indices, and the CDB/licence
  loading path are mapped from the binary.
- **Not verified on the device:** *which specific* software-gated frame-rate or
  format features actually turn on when their gate is flipped. Treat those as
  candidate targets until tested on hardware.
