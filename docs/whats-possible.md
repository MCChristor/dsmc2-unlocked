# What Is Possible

This page states what the reverse-engineering enables — the outcomes. The methods,
keys, and tools behind them are in [docs/keys.md](keys.md),
[docs/serial-shell.md](serial-shell.md), [docs/log-decode.md](log-decode.md), the
[tools/](../tools) folder, and the [media](../media/) folder.

## Confirmed

- **The firmware is understood.** The packaging and the per-model structure are
  mapped. You can analyse and compare builds offline. You can produce modified
  firmware in a form the camera accepts.
- **Camera behaviour can be changed.** Features and limits that are gated in
  software can be unlocked. This works both as a lasting change and as a per-boot
  change.
- **Media authentication is reverse-engineered.** The scheme is three checks:
  model-string whitelist, an MD5 SMART-log signature, and a ~29-field ATA IDENTIFY
  match. All three are reproduced offline against a genuine magazine. A drive
  mounts once it reports a whitelisted model string and a readable signature page.
  **Full data rate additionally requires passing the signature and the IDENTIFY
  match** — a retail drive typically fails the IDENTIFY capability words and caps
  at ~30 MB/s unless given the `media-any` camera patch. The end-to-end hardware
  path (adapter board) is not yet tested. Full detail and exact conditions are in
  the [media](../media/) folder.

## Bounded by hardware

- **Model identity is configuration.** You can change the camera-type value without
  swapping the binary. **Capability is not only configuration.** It is bounded by
  the sensor and by per-body hardware-capability flags.
- **Sensor resolution is fixed hardware.** A 5K body cannot become 8K. The lineup
  uses genuinely different sensors across models.
- **Some frame-rate and format limits are software gates.** These are *candidate*
  unlock targets on hardware that already supports them. Which gates actually open
  was **not verified on the device**. So treat specific feature gains as unproven
  until tested. Crossgrades only make sense inside one sensor family, and only for
  the software-gated layer.
- **HDMI monitor output tops out at 1080p.** The firmware's display-preset set
  offers only `1080P (HD)` and `720P (HD)` on the brain HDMI port; the only UHD
  display presets are `DISPLAY_PRESET_UHDSDI_*` and the rear `UHDSDI` channel —
  i.e. 4K monitoring exists **only over SDI**, never HDMI. The `BRAIN_HDMI` preset
  family has no UHD variant. This is not a software gate: the HDMI path runs
  through IOB0 and the OMAP display subsystem ([platform.md](platform.md)), so the
  port is a 1080p-class link. To get the camera's 4K picture onto an HDMI display,
  convert its 4K SDI externally — which is exactly what RED's own HDK board does
  (SDI→HDMI, [peripheral-firmware.md](peripheral-firmware.md)).

## In development — to be announced

A **custom firmware** build is in progress. The planned additions are:

- **New anamorphic de-squeeze ratios** beyond the stock set.
- **In-camera IPP2 on original-DRAGON bodies** (e.g. SCARLET-W) — the colour
  pipeline gate is one capability bit, not a sensor lock; see [ipp2.md](ipp2.md).
  Render correctness is pending a hardware shoot-test.
- **Universal media** — any compatible SATA SSD usable as a mag, with no
  genuine-media check at all.

These will be **announced later**. This repository will be updated when the build
ships.

## Where the details are

Everything above is backed by published material in this repository: the keys and
what they open ([keys.md](keys.md)), the debug-shell access path
([serial-shell.md](serial-shell.md)), the package format and decryptor
([firmware.md](firmware.md), [tools/fw-crypto](../tools/fw-crypto)), the log
decoder ([log-decode.md](log-decode.md)), the serial bridge
([hardware/serial-bridge](../hardware/serial-bridge)), and the full media path
([media](../media/)).
