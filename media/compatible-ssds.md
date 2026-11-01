# Compatible SSDs — What to Buy (2026)

The camera matches a **model string**, not a part number. So it does not matter
that the original RED OEM drives (Delkin, Innodisk, Centon, Virtium) are
discontinued. Any SATA SSD that can present an approved model string works.

## Rules

- **SATA only.** Use mSATA or M.2-SATA. Do **not** use NVMe (M.2 PCIe). Do not
  use CFexpress/CF/SD.
- Any drive near **500 MB/s** read comfortably meets the ~300 MB/s R3D data rate.
- The controller and NAND do not gate access. Only the model string and the
  signature do. They only affect speed and endurance.

## Buyable mSATA SSDs

| Drive | Sizes | Notes |
|---|---|---|
| Kingston KC600 mSATA | 256 GB / 512 GB / 1 TB | Still manufactured. SATA III, ~550 MB/s. Phison controller (findable flashing tools). |
| KingSpec MT mSATA | up to 1 TB | In stock, low cost. |
| Fanxiang / SHARKSPEED / Kingchuxing mSATA | 512 GB / 1 TB | eBay / Amazon, ~30–130 USD, budget NAND. |
| Samsung PM851 mSATA 1 TB (used) | 1 TB | Special — see the easy path. |

mSATA is a legacy form factor. It is still made and in stock. M.2-SATA is the
newer option. M.2-SATA allows capacities past 960 GB. KipperTie's approved mag
uses M.2-SATA at 2 TB.

## Easy path — Samsung PM851 1 TB (low difficulty)

A genuine Samsung PM851 mSATA 1 TB reports the model string
`SAMSUNG MZMTE1T0HMJH-00000` natively. This is an approved string in the media
table. So:

1. Get a used Samsung PM851 1 TB mSATA (common historically; scarcer now).
2. Fit it to the [adapter board](hardware.md).
3. Insert it and run `signature_write` on the camera — it writes the correct
   page-0x90 signature for that drive. (You can also do it offline with the formula
   in [authentication.md](authentication.md), but the camera is simpler.)

There is no model-string flashing. The only real work is the connector board.

One caveat for **full rate**: the camera checks the drive's reported sector count
against the table row (`AuthenticateREDMedia`), and the
`SAMSUNG MZMTE1T0HMJH-00000` row expects **960 GB** (1,875,385,008 sectors). A
stock PM851 reports its native ~1 TB, so it passes the signature but fails the
geometry check and caps at ~30 MB/s. For full rate, cap the drive to 960 GB with
a host-protected area (HPA) so its reported capacity matches the row. It still
mounts at 1 TB; it just records at the slow class until capped.

## The model string is the only real obstacle

Everything comes down to making the drive **report an approved model string**. The
signature is easy — the camera writes it for you with `signature_write` once the
string matches (see [authentication.md](authentication.md)), so you need no MPTool
and no host GPL-write for that step. There are three ways to get the model string,
in increasing effort.

### 1. Buy a drive that already reports an approved string (no flash)

If you can find a drive whose native model string is in the media table, you do
nothing to it — fit it, insert it, run `signature_write`. The Samsung PM851 mSATA
1 TB reports `SAMSUNG MZMTE1T0HMJH-00000` natively, which is approved. The catch in
2026 is that these specific OEM drives are increasingly scarce and used-only, so do
not build a plan around one part number.

### 2. Override the model string with a SATA bridge (no flash)

Some SATA bridge/adapter chips let you override what the drive reports for ATA
IDENTIFY — the model string and the WWN — without touching the SSD itself. With
one of those you can make **any** SATA SSD present `RED 512GB V5` and a fixed WWN,
then let the camera sign it. This avoids flashing entirely and is not tied to a
scarce drive. It depends on finding a bridge that exposes IDENTIFY override and
still passes the SMART log page through; verify both before relying on it.

### 3. Flash the model string with the controller's MPTool

For any cheap SSD whose controller you can reach:

1. Identify the controller (Silicon Motion, Phison, etc.).
2. Get the matching mass-production tool (MPTool). Archives live at usbdev.ru and
   upantool.com. The tool is controller-specific and often undocumented in English.
3. Set the ATA IDENTIFY model string to `RED 512GB V5` (the MPTool erases the NAND,
   so do it once on an empty drive).
4. Insert and run `signature_write`.

`RED 512GB V5` is the easiest target string (12 chars, type 1, no serial in the
hash). The hard part is finding the right MPTool; the cryptography is not the hard
part.

> **Without firmware patching**, options 1–3 all still require the drive to report
> an approved model string. Making *any* model string accepted — so no bridge and
> no MPTool is needed — requires patching the firmware's whitelist check, which is
> a separate, camera-write step and not covered here.

## Recommendation

The signature is never the obstacle — the model string is. If you can get a drive
that natively reports an approved string (a used PM851 while they last), that is the
least work. Otherwise a **SATA bridge that overrides IDENTIFY** avoids both flashing
and scarce drives; a controller **MPTool flash to `RED 512GB V5`** is the fallback
when you can reach the controller.

## Field confirmation

This matches what the community and approved vendors have reported
independently:

- Reduser analysis of JinniTech's method: the camera reads only the **SSD model
  number** and the **SMART log** for verification. This is exactly the two gates
  here.
- Approved third-party mags exist and pass the model-string and signature gates.
  They are purpose-built drives, not stock SSDs. A working mag needs correct
  controller behaviour (power management, hot-plug, sustained write), not only the
  signature.
- RED's own statement that the custom part "is not on the drives, but in the
  camera" matches the finding that the camera does the validation.

## Controller and MPTool notes

The camera does not check the SSD controller. It does not check the controller's
internal settings. The firmware reads the drive only for the model string, the
hard-disk device type, and the model, serial and WWN that feed the signature hash.
There is no controller, link-speed, or queue check in the accept path.

But the controller still matters for two practical reasons.

First, the drive must answer the vendor SMART log page 0x90. If the controller
does not expose that log, the camera's read fails and the drive does not mount at
all. This is the real hard requirement on the controller.

Second, you set the model string through the controller's production tool. The
drive must report an approved model string for full speed. A drive that cannot be
made to report one still mounts, but only at the low-speed class.

So the controller work is about meeting the two gates, not about passing a hidden
camera check. The accept logic is the same on every DSMC2 body.
