# Media — RED MINI-MAG and Compatible SSDs

The DSMC2 records to a **RED MINI-MAG**: a SATA SSD inside a RED-branded caddy
that the camera authenticates before it will record at full speed. RED has
discontinued these mags and no longer sells or services them, so owners who want
to keep shooting need another media path. This folder documents that path in
full.

> RED MINI-MAG 1TB, 512GB and 240GB appear on RED's official [Discontinued
> Products](https://support.reddigitalcinema.com/hc/en-us/articles/1500000253342-Discontinued-Products)
> page, marked repair parts no longer available.

## The short version

- **Bus is SATA-only** (SATA III, via an on-board SATA3 FPGA). NVMe and
  CFexpress/CF/SD do **not** work — don't buy them.
- A MINI-MAG is a stock **mSATA** SSD (Silicon Motion SM2246EN controller) in a
  caddy. Nothing exotic.
- The camera decides whether to accept a drive from **two things only**: the
  drive's reported **model string**, and an **MD5 signature** stored in a SMART
  log page. Both are reproducible offline — no RSA, no server, no secret you
  cannot derive. See [authentication.md](authentication.md).
- So **any SATA SSD can be a mag** if it reports an approved model string and
  carries the right signature. The controller, NAND, and capacity do not gate
  access — they only affect speed and record time.

## Documents

| Document | What it covers |
|---|---|
| [authentication.md](authentication.md) | The two-gate lock, the exact signature algorithm, page 0x90/0x91 |
| [media-table.md](media-table.md) | The firmware media table: every approved model and its OEM |
| [compatible-ssds.md](compatible-ssds.md) | What to buy in 2026, the easy path, and the flashing path |
| [hardware.md](hardware.md) | The connector/adapter board — the one remaining physical task |

## Status

The authentication scheme is **fully reverse-engineered and reproduced offline**
against a genuine magazine. What remains is purely hardware: a small adapter
board to seat a bare SATA SSD in the mag bay.
