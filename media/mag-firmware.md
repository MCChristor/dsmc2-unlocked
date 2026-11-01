# MINI-MAG Controller Firmware (`.rmf`)

A RED MINI-MAG is an mSATA SSD built on a **Silicon Motion SM2246EN** controller.
Its controller firmware ships as a `.rmf` file, which the camera flashes to the mag
via **Menu > Settings > Maintenance > Upgrade > Media**. This page documents the
`.rmf` format, based on the genuine `RED 960GB V3` firmware (`0301-000.rmf`).

> **Status: static analysis.** The format, the identity template, and the file
> checksum are confirmed. The clone route at the end is a **lead, not a verified
> method** — it has not been tested on hardware.

## It is plaintext, not encrypted

The `.rmf` is **not AES-encrypted**. Its entropy is ~6.5 throughout — ordinary
controller firmware plus config, directly readable. (An earlier belief that it was
sealed with the drive's own keys was wrong.) So the file can be inspected and
edited without any key.

## Layout

From `0301-000.rmf` (394,368 bytes):

| offset | content |
|---|---|
| `0x00` | magic `01 05 00 00` |
| `0x04` | u32 checksum = **byte-sum (mod 2³²) of `0x80`..end of file** |
| `0x0C` | media-table model string, `RED 960GB V3` |
| `0x5C` | firmware revision, `0301-000` |
| `0x80`–`0x1F0` | **ATA IDENTIFY template** (stored byte-swapped per 16-bit word) |
| `0x280` | `SM2246AA` controller platform tag |
| `0x289` | `CIDPAGE` controller ID page |
| `0x380` | `MPINFO` → the NAND part (`Toshiba TH58TFT0DDLBA8H`) |
| `0x500`+ | SM2246 firmware code |

## The identity template

The strings the controller reports over ATA live in clear (de-byte-swapped) in the
`0x80`–`0x1F0` block:

```
MODEL  : RED 960GB V4
SERIAL NUM : (serial)
WWN:    (wwn)
VENDOR SPECIFIC: RED Digital
FirmWare 0301-000
```

So the **model string, serial, and WWN a mag reports are stored in the `.rmf`**, at
fixed offsets, in plaintext.

## Why this could matter (unproven)

The camera flashes a `.rmf` to a mag with its own Upgrade > Media menu. If that
path will write a `.rmf` to any SM2246EN-based mSATA drive — not only a genuine RED
mag — then editing the `MODEL` field to an approved string and fixing the `0x04`
checksum (a plain byte-sum, so trivial to recompute) would let the **camera's own
flasher** give any such drive an approved model string. The camera could then write
page 0x90 itself (`signature_write`, see [authentication.md](authentication.md)) —
a clone route that needs no third-party MPTool.

This is **not confirmed.** The open questions are:

- whether Upgrade > Media accepts and flashes a non-RED SM2246 drive at all;
- whether the SM2246 code payload has to match the target drive's exact NAND (the
  `0301-000.rmf` is built for Toshiba `TH58TFT0DDLBA8H`); a mismatched flash could
  brick the drive.

Until those are answered on hardware, treat this as a research direction. The
established no-flash paths in [compatible-ssds.md](compatible-ssds.md) do not depend
on it.
