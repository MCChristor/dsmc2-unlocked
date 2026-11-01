# RED DSMC2 — Owner's Reverse-Engineering Notes

Independent reverse-engineering of the **RED DSMC2** camera platform, for owners
who want to keep discontinued bodies and media running. Reference body:
SCARLET-W 5K, firmware 7.4.1.

This documents *what the platform is* and *what is possible* with it. Most of it
is deliberately high-level: the internal methods, keys, and access techniques are
not published. The **one fully documented area is media** — because the MINI-MAG
is discontinued and unsupported, the [media](media/) folder covers the whole
cheap-SSD path in detail.

> **Context.** Independent research on hardware the author owns. RED has
> **discontinued** the DSMC2 line and its MINI-MAG media; the magazines are no
> longer sold or serviced. Nothing here undercuts a product on sale or a service
> RED offers. The goal is repair, preservation, and keeping owned hardware alive.
>
> RED lists RED MINI-MAG 1TB / 512GB / 240GB on its official [Discontinued
> Products](https://support.reddigitalcinema.com/hc/en-us/articles/1500000253342-Discontinued-Products)
> page ("repair parts no longer available"). The DSMC2 line was wound down after
> the 2024 Nikon acquisition and is no longer manufactured.

## Contents

| Area | What it covers |
|---|---|
| [docs/platform.md](docs/platform.md) | What the DSMC2 is: SoC, OS, coprocessors, buses |
| [docs/models.md](docs/models.md) | The DSMC2 model family and how models differ |
| [docs/whats-possible.md](docs/whats-possible.md) | What the research enables (outcomes) |
| [docs/firmware.md](docs/firmware.md) | Package formats (v2/v3) and how the encryption works |
| [docs/research-notes.md](docs/research-notes.md) | Difficulties, insights, and the research story |
| [media/](media/) | **MINI-MAG and compatible SSDs — fully documented** |

### The media folder

| Document | What it covers |
|---|---|
| [media/README.md](media/README.md) | Overview and the short version |
| [media/authentication.md](media/authentication.md) | The two-gate lock and the exact signature algorithm |
| [media/media-table.md](media/media-table.md) | Every approved model string and its OEM |
| [media/compatible-ssds.md](media/compatible-ssds.md) | What to buy in 2026, the easy path, the flashing path |
| [media/hardware.md](media/hardware.md) | The connector/adapter board |

## Scope kept private

Internal keys, exact reverse-engineering methods, camera access techniques, and
ready-to-run exploit code are **not** in this repo. The media path is the
documented exception.
