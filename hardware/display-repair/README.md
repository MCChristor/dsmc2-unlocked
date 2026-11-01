# Touch LCD Repair

Spare-part and repair notes for the RED DSMC2 **Touch LCD** monitors. The panel
and connector part numbers here come from owner teardowns of the author's own
hardware; RED does not publish them, so verify them against your own unit before
ordering.

## RED DSMC2 Touch 7.0 (7″)

- **LCD panel: `LD070WU2-SM01`.** This panel can be sourced easily. Confirm the
  video interface matches your driver board before fitting (the monitor is a
  MIPI/LVDS-class panel feeding RED's driver).
- **Touch digitizer: `EP0700MU9` by EDT.** This is the hard part — it is
  effectively impossible to source.
  - **`EP0700M06` and `EP0700M12` will not work** as drop-in replacements: they
    use a **different touch controller/driver and a different pin-out**.
  - A substitution may still be possible later with a **custom flex harness** that
    re-maps the pins, since the difference is the connector/driver interface rather
    than the glass size. Untested; noted as a direction, not a solution.
- **Side-button connector board: `DF40C-10DS-0.4V(51)`** (Hirose DF40 series,
  10-pin, 0.4 mm pitch). This connector is fragile. After reseating, secure it (UV
  resin or hot-glue) so it does not work loose again.

> An earlier parts list recorded the 7″ touch panel as `EP0700M12`. That is
> **incorrect** — the original is `EP0700MU9`, and `M12` is not compatible.

## RED DSMC2 Touch 4.7 (4.7″)

- **LCD panel: the screen from a Xiaomi Redmi 1S** fits and can be sourced for a
  few dollars.
- **Touch digitizer: fused to the original glass.** The touch layer is laminated
  to the display, so a swap means separating them first. A phone-display repair
  shop that does glass/digitizer separation can likely do this.
- The side-button connector on the 4.7″ is **not yet confirmed** (it may or may
  not be the same `DF40C` part as the 7.0″).

## Mounting threads (LCD / EVF)

- Stripped mounting threads take a **thread insert, M4 × 0.7**. Use a branded
  thread-repair (coil) kit.

## Public references

RED's operation guides list the monitor specs (the 4.7″ is 1280×720, part
730-0019) but do not name the panels or driver boards. The notes above are for the
**RED Touch 7.0** and **Touch 4.7**; the later **7″ Ultra-Brite** is a separate
monitor and is not covered here.

- [DSMC2 Displays and EVFs (DRAGON-X guide)](https://docs.red.com/955-0181_v7.4/DSMC2_DRAGONX_7_4/Content/2_Components/10_Displays.htm)
