# Compatible SSDs — What to Buy (2026)

The camera matches a **model string**, not a part number. So the original RED OEM
drives (Delkin, Innodisk, Centon, Virtium) being discontinued does not matter.
Any SATA SSD that can present an approved model string works.

## Rules

- **SATA only.** mSATA or M.2-SATA. **Not** NVMe (M.2 PCIe), not CFexpress/CF/SD.
- Any drive near **500 MB/s** read comfortably meets the ~300 MB/s R3D data rate.
- The controller and NAND do not gate access — only the model string and the
  signature do. They only affect speed and endurance.

## Buyable mSATA SSDs

| Drive | Sizes | Notes |
|---|---|---|
| Kingston KC600 mSATA | 256 GB / 512 GB / 1 TB | Still manufactured. SATA III, ~550 MB/s. Phison controller (findable flashing tools). |
| KingSpec MT mSATA | up to 1 TB | In stock, low cost. |
| Fanxiang / SHARKSPEED / Kingchuxing mSATA | 512 GB / 1 TB | eBay / Amazon, ~30–130 USD, budget NAND. |
| Samsung PM851 mSATA 1 TB (used) | 1 TB | Special — see the easy path. |

mSATA is a legacy form factor but still made and in stock. M.2-SATA is the newer
option and allows capacities past 960 GB (KipperTie's approved mag uses M.2-SATA
at 2 TB).

## Easy path — Samsung PM851 1 TB (low difficulty)

A genuine Samsung PM851 mSATA 1 TB reports the model string
`SAMSUNG MZMTE1T0HMJH-00000` natively — which is an approved string in the media
table. So:

1. Buy a used Samsung PM851 1 TB mSATA. Common and cheap.
2. Fit it to the [adapter board](hardware.md).
3. Write the correct SMART page-0x90 signature for its identity (offline, with
   the formula in [authentication.md](authentication.md)).

No model-string flashing. The drive is 1 TB — larger than RED's biggest 960 GB
mag. The only real work is the connector board.

## Flashing path — any SSD to `RED 512GB V5` (medium difficulty)

For any other cheap SSD:

1. Identify the controller (Silicon Motion, Phison, etc.).
2. Get the matching mass-production tool (MPTool). Archives live at usbdev.ru and
   upantool.com. The tool is controller-specific and often undocumented in
   English.
3. Set the ATA IDENTIFY model string to `RED 512GB V5`. The MPTool erases the
   NAND, so run it once on an empty drive.
4. Write the page-0x90 signature.

`RED 512GB V5` is type 1 (no serial in the hash), and with a zero-WWN drive the
17-byte signature is the copyable constant given in
[authentication.md](authentication.md). The hard part is finding the correct
MPTool for the controller, not the cryptography.

## Recommendation

Use a **Samsung PM851 1 TB mSATA**: no flashing, 1 TB, and the whole task reduces
to the adapter board plus writing one signature. If a PM851 is unavailable, a
**Kingston KC600 flashed to `RED 512GB V5`** is the next best.

## Field confirmation

This matches what the community and approved vendors have reported independently:

- Reduser analysis of JinniTech's method: the camera reads only the **SSD model
  number** and the **SMART log** for verification — exactly the two gates here.
- Approved third-party mags (Cinelux Nexa-Mag, KipperTie Longtake 2 TB) pass this
  same lock with stock SSDs.
- RED's own statement that the custom part "is not on the drives, but in the
  camera" matches the finding: the drive is a stock SSD; the camera validates.
