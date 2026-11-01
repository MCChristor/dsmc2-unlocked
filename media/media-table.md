# The Firmware Media Table

The camera carries a table of approved recording media. After the model-string
whitelist match, the camera looks the drive up here to get its parameters
(capacity, data-rate class) and the **required signature type**. Access is gated
only by the model string plus the signature — the controller, NAND and physical
capacity are not checked for access, only used for record-time math.

## Official RED models

Each RED SKU is manufactured by one of several OEM SSD makers. The **model
string** is what the camera matches; the OEM is who actually builds the drive.

| Model string | OEM(s) | Signature type |
|---|---|---|
| `KINGSTON RBU-SMS100S3120GD` / `GD1` | Kingston | 1 |
| `Micron_M500_MTFDDAT240MAV` / `480MAV` | Micron | 1 |
| `M500IT_MTFDDAT240MBD` | Micron | 3 |
| `RED 480GB V1` / `V2` / `V3` | Innodisk / Centon / Delkin | 3 |
| `RED 512GB V5` | Delkin | 1 (type 2 = PV DXL) |
| `RED 512GB V6` | Innodisk | 1 |
| `RED 960GB V1` / `V2` / `V3` | Centon / Delkin / Virtium | 3 |
| `RED 120GB V5` / `V6` / `V7` | Centon / Innodisk / Virtium | 3 |
| `RED 240GB V4` / `V5` / `V6` | Innodisk / Virtium / Centon | 3 |
| `SAMSUNG MZMTE1T0HMJH-00000` | Samsung (PM851 mSATA 1 TB) | 1 (type 2 = PV DXL) |
| `PV DXLM1TB V1` / `V2` / `V3` | Centon / Delkin / Virtium | 2 |

There are 19 distinct official RED model strings (120/240/480/512/960 GB across
versions), plus the OEM part-number strings above. Older firmware also knows a
wider set of OEM drives (Toshiba, Viking, Memoright, Transcend and others) by
their raw part numbers.

## Capacities

The table stores each drive's real usable geometry (capacity in 512-byte
sectors), and the values are exact standard SSD sizes:

| Model group | Usable capacity |
|---|---|
| 120 GB V6/V7 | 120,034,123,776 B (120 GB) |
| 240 GB V4/V5/V6 | 240,057,409,536 B (240 GB) |
| 480 GB V1/V2/V3 | 480,103,981,056 B (480 GB) |
| 960 GB V2/V3 | 960,197,124,096 B (960 GB) |

Note the marketing vs usable quirk: the **"512GB" MINI-MAG is a 480 GB drive**.
Media-table entry `RED 512GB V5` is a 480 GB Delkin unit.

## The two best clone targets

- **`RED 512GB V5`** — type 1, and the hash does not include the serial. With a
  zero-WWN drive the signature is a copyable constant (see
  [authentication.md](authentication.md)).
- **`SAMSUNG MZMTE1T0HMJH-00000`** — a real Samsung PM851 mSATA 1 TB reports this
  string natively, so no model-string flashing is needed at all.

## Confirmed real-world device titles

From a public RED MINI-MAG teardown (YouTube comment by `@我是02老公`), these are
the **actual ATA device titles** genuine mags report — useful because the device
title is exactly what the camera's model-string gate matches:

| RED label | Reported device title | Underlying drive |
|---|---|---|
| 120 GB V3 | `KINGSTON RBU-SMS100S3120GD1` | Kingston |
| 240 GB V1 | `M500IT_MTFDDAT240MBD` | Micron M500IT |
| 480 GB V3 | `Micron_M500_MTFDDAT480MAV` | Micron M500 |
| 960 GB V1 / "1 TB" | `RED 1TB V1` | Virtium StorFly 300CE |
| 960 GB V3 | `RED 960GB V3` | — |
| 2 TB (approved) | `KipperTie Longtake 2TB V1` | KipperTie M.2-SATA |

Two things worth noting:

- Some SKUs report a **raw OEM part number** as the title (the Kingston and Micron
  ones), while others report a **RED-branded** title (`RED 1TB V1`,
  `RED 960GB V3`). Either form is just a string the camera matches exactly.
- The **KipperTie 2 TB** reports its **own** title, `KipperTie Longtake 2TB V1`,
  and the camera still accepts it — so the approved-partner titles are part of
  the whitelist too, not only RED's own.
