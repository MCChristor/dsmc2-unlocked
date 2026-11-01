# What Is Possible

What the reverse-engineering enables, stated as outcomes. This page says *what*
is possible, not *how* it was done — the methods, internal keys, and access
techniques are deliberately not published.

## Confirmed

- **The firmware is fully understood.** Its packaging and per-model structure are
  mapped, builds can be analysed and compared offline, and modified firmware can
  be produced in a form the camera accepts.
- **Camera behaviour can be changed.** Features and limits that are gated in
  software can be unlocked, both as persistent changes and as per-boot changes.
- **Media authentication is solved.** The scheme that decides which drive the
  camera accepts is reverse-engineered and reproduced offline against a genuine
  magazine, so **any compatible SATA SSD can serve as a mag**. Full detail is in
  the [media](../media/) folder — this is the one area documented end to end.

## Understood but sensor-limited

- **Frame-rate and format limits are software** and are realistic unlock targets.
  **Sensor resolution is not** — a 5K body cannot become 8K. Crossgrades only
  make sense *within* a sensor family.

## In development — to be announced

A **custom firmware** build is in progress. Planned additions:

- **New anamorphic de-squeeze ratios** beyond the stock set.
- **Universal media** — any compatible SATA SSD usable as a mag with no
  genuine-media check at all.

To be **announced later**; this repo will be updated when it ships.

## Out of scope here

Internal keys, exact methods, access techniques, and ready-to-run exploit code
are not published. The media folder is the exception: that path is fully
documented because the media is discontinued and unsupported.
