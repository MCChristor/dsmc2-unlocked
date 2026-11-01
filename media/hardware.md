# Media Adapter Hardware

Only one physical task remains to use a bare SATA SSD as a magazine: a
**connector/adapter board** that seats the drive in the mag bay and routes SATA
plus power to the camera's mag connector.

- A genuine MINI-MAG is an **mSATA** module; an **M.2-SATA** module works too
  (M.2-SATA, not M.2 NVMe). An adapter can host either.
- The electrical interface is plain SATA III plus power — nothing proprietary on
  the wire.
- Approved third-party mags (e.g. KipperTie's M.2-SATA unit) prove the mechanical
  and electrical approach scales, including to capacities past RED's own 960 GB.

## The mag connector (TE Connectivity)

The MINI-MAG electrical interface uses TE Connectivity parts. From a public
teardown, the part numbers are:

| Side | TE part number |
|---|---|
| Card reader (male, camera/reader side) | `2129261-1` or `21229276-1` |
| MINI-MAG (female, on the mag) | `2129260-2` |

An adapter board recreates the mag-side (female `2129260-2`) footprint and wires
it to a bare mSATA or M.2-SATA SSD. These are standard orderable TE connectors.

Board design files and photos will be added here as the hardware is built.

> Source for the part numbers: a public YouTube comment by `@我是02老公` on a RED
> MINI-MAG teardown video, which also confirms the OEM device titles in
> [media-table.md](media-table.md) (e.g. 120 GB = `KINGSTON RBU-SMS100S3120GD1`,
> 240 GB = `M500IT_MTFDDAT240MBD`).
