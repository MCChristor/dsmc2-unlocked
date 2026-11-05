# Sensor Calibration — regenerate, back up, transplant

The DSMC2 carries a full in-camera sensor-calibration engine: black shading, column
linearization, defect (bad-pixel) map, and black-sun/blooming. All of it is reachable
from the debug shell (and RCP) through `CAL_*` commands, and the calibration files are
plaintext. That makes three practical things possible without any special tooling.

## Back up the factory calibration (do this before any mod)

`CAL_EXPORT_TO_MEDIA` / `CAL_EXPORT_ALL_TO_MEDIA` dump this body's calibration to an
inserted SSD. The exported `.cal` files are plaintext (column cal, defect map). Keeping
a copy means any calibration change is reversible — restore the body to its own factory
state at any time. This is the first step of any safe experiment.

## Regenerate calibration in-camera (dead / degraded cal repair)

A body can rebuild its own calibration from captured frames — no donor camera, no
external file. `CAL_AUTO` drives the capture-and-build flow: the camera takes dark/raw
frames, builds the column-linearization map, applies it, and writes it back to the
calibration store. This is the repair path for a body whose factory calibration is lost
or corrupt (one failure class behind a bad-looking image on an otherwise-working brain).

## Transplant a known-good calibration

Calibration can also be loaded from media: the camera reads an `ADC_CAL.cal` from an
inserted SSD, remounts the read-only data partition writable, and copies the file in.
Because the format is plaintext, a known-good, foreign, or hand-authored calibration can
be installed this way. Pair it with the backup step above so the original is always
recoverable.

## Note on extra gain modes

If you unlock the sensor-sensitivity capability (extra gain modes, see
[feature-unlock.md](feature-unlock.md)), the calibration engine then expects a matching
calibration file *per gain mode* — the check is skipped only while that capability is
off. Each extra gain mode therefore needs its own calibration, generated in-camera or
transplanted. The feature flips on easily; the calibration it then demands is the real
work.

---
Commands and the calibration store live behind the debug shell
([serial-shell.md](serial-shell.md)). Exact addresses are kept in the private research
notes; this page is the operator-level summary.
