# RED DSMC2 — Owner's Reverse-Engineering Notes

This repository holds independent reverse-engineering of the **RED DSMC2** camera
platform. It is for owners who want to keep discontinued bodies and media running.
The reference body is a SCARLET-W 5K on firmware 7.4.1.

Written in simplified technical English.

This repository documents *what the platform is* and *what is possible* with it.
Most of it stays high-level. It does not publish the internal methods, the keys, or
the access steps. **Media is the one area documented in full.** The MINI-MAG is
discontinued and unsupported, so the [media](media/) folder gives the whole
cheap-SSD path in detail.

> **Context.** This is independent research on hardware the author owns. RED has
> **discontinued** the DSMC2 line and its MINI-MAG media. The magazines are no
> longer sold or serviced. Nothing here harms a product on sale or a service that
> RED offers. The goal is repair and preservation.
>
> RED lists RED MINI-MAG 1TB, 512GB and 240GB on its official [Discontinued
> Products](https://support.reddigitalcinema.com/hc/en-us/articles/1500000253342-Discontinued-Products)
> page, marked "repair parts no longer available". RED wound the DSMC2 line down
> after the 2024 Nikon acquisition. It is no longer manufactured.

## Contents

| Area | What it covers |
|---|---|
| [docs/platform.md](docs/platform.md) | What the DSMC2 is: processor, OS, coprocessors, buses |
| [docs/models.md](docs/models.md) | The DSMC2 model family and how models differ |
| [docs/whats-possible.md](docs/whats-possible.md) | What the research enables (outcomes) |
| [docs/firmware.md](docs/firmware.md) | Package formats (v2/v3) and how the encryption works |
| [docs/research-notes.md](docs/research-notes.md) | Difficulties, insights, and the research story |
| [media/](media/) | **MINI-MAG and compatible SSDs — documented in full** |

### The media folder

| Document | What it covers |
|---|---|
| [media/README.md](media/README.md) | Overview and the short version |
| [media/authentication.md](media/authentication.md) | The two-gate lock and the signature algorithm |
| [media/media-table.md](media/media-table.md) | Every approved model string and its OEM |
| [media/compatible-ssds.md](media/compatible-ssds.md) | What to buy in 2026, the easy path, the flashing path |
| [media/hardware.md](media/hardware.md) | The connector/adapter board |

## Scope kept private

This repository does not hold the internal keys, the exact reverse-engineering
methods, the camera access steps, or ready-to-run exploit code. The media path is
the one exception; it is documented in full.
