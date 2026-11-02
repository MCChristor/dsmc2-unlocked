# Media — RED MINI-MAG and Compatible SSDs

The DSMC2 records to a **RED MINI-MAG**. A MINI-MAG is a SATA SSD inside a
RED-branded caddy. The camera authenticates the drive. After that, the camera
records at full speed. RED has discontinued these mags and no longer supplies
repair parts for them. Owners who want to keep shooting need another media path.
This folder documents that path in full.

> RED MINI-MAG 1TB, 512GB and 240GB appear on RED's official [Discontinued
> Products](https://support.reddigitalcinema.com/hc/en-us/articles/1500000253342-Discontinued-Products)
> page. They are marked as repair parts that are no longer available.

## The short version

- **The bus is SATA-only** (SATA III, through an on-board SATA3 FPGA). NVMe and
  CFexpress/CF/SD do **not** work. Do not buy them.
- A MINI-MAG is a stock **mSATA** SSD in a caddy. The one genuine firmware we
  examined (960 GB V3) uses the Silicon Motion SM2246EN controller. Nothing is
  exotic.
- The camera runs **three checks** on an inserted drive: the drive's reported
  **model string** (whitelist), an **MD5 signature** in a SMART log page, and an
  **ATA IDENTIFY field match** (`AuthenticateREDMedia` compares ~29 IDENTIFY
  fields against the model's spec row — the sector count is only one of them, and
  the controller-firmware capability/version words are the ones a retail drive
  usually fails). There is no RSA, no server, and no secret you cannot derive. See
  [authentication.md](authentication.md).
- **All three checks gate full rate.** An unapproved or unsigned drive, or one
  whose IDENTIFY fields don't match, still mounts and records — but the firmware
  caps it to ~30 MB/s, which is useless for video. So "it still mounts" is not a
  pass: for a usable drive **all three checks are mandatory**. Only the *mount
  itself* is permissive.
- The controller, NAND, and raw capacity do not gate the mount. But a drive whose
  controller firmware reports the wrong IDENTIFY words **cannot reach full rate
  without a camera-side firmware patch** (`media-any`), because you cannot rewrite
  those words on the drive without reflashing its controller. See
  [authentication.md](authentication.md) and the patch tooling.

## Documents

| Document | What it covers |
|---|---|
| [authentication.md](authentication.md) | The three checks, the exact signature algorithm, page 0x90/0x91 |
| [media-table.md](media-table.md) | The firmware media table: every approved model and its OEM, and whether it can be changed |
| [mag-firmware.md](mag-firmware.md) | The MINI-MAG controller `.rmf` firmware: format, identity template, clone lead |
| [compatible-ssds.md](compatible-ssds.md) | What to buy in 2026, and why a buyable drive needs the camera patch for full rate |
| [hardware.md](hardware.md) | The connector/adapter board — the one remaining physical task |

## Status

The authentication scheme is **fully reverse-engineered statically** and the
signature is **reproduced offline** against a genuine magazine. The end-to-end
hardware path is **not yet tested**: it needs a small adapter board (unbuilt) to
seat a bare mSATA SSD in the mag bay. A retail drive also needs the `media-any`
camera patch for full rate unless its IDENTIFY fields happen to match a spec row.
