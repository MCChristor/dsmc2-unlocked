# The DSMC2 Platform

A hardware and software overview of the RED DSMC2 camera, as reverse-engineered
from a SCARLET-W 5K running firmware 7.4.1.

## Main processor and OS

- **Application processor:** TI OMAP-class ARM Cortex-A8, 32-bit, single flat
  address space, **no MMU**. Main DDR window is at `0x80000000`.
- **Operating system:** ThreadX (Express Logic, G5.5.5.x), the real-time OS now
  open-source. Compiled with Green Hills.
- **Consequence of flat/no-MMU:** there is no process isolation. Any code that
  runs can read and write the whole address space.

## Coprocessors

The DSMC2 is a multi-processor design. The main ARM orchestrates several
dedicated cores, each with its own firmware image loaded at boot:

| Subsystem | Core | Role |
|---|---|---|
| ISP | Tensilica | Sensor image processing (the R3D wavelet path is hardware) |
| IOB0 | Tensilica | SATA / HBA / HDMI I/O |
| IOB1 | Tensilica | Sensor dark-level and bad-pixel calibration |
| LSB FPGA | Xilinx Kintex-7 | Programmable logic |
| SATA3 FPGA | FPGA | Bridges the media bus (see the media folder) |
| DSP | TI TMS320C6x | Brain-module signal processing |
| WiFi/BT | RSI RS9113 (Redpine) | Wireless |

Accessories (lens mounts, rear I/O modules, battery module, FlatUI, EVF) each
carry their own small MCU firmware, mostly ARM-Thumb (STM32-class).

## Software components

Standard building blocks, identified in the firmware:

- **SQLite3** — the camera settings database (referred to as the CDB).
- **zlib** — on-NAND compression.
- **YAFFS2** — the flash filesystem.
- **LibTomCrypt** — software crypto.
- **TinyXML** — manifests.
- **ProRes + DNxHD** — proxy/output codecs (R3D itself is the hardware wavelet).

## Storage layout

Internal NAND is partitioned into: environment, two OS images (`image1` /
`image2`, one active), a data partition, a log partition, a large read-only
data partition, and a large persistent-data partition. Calibration and
force-update areas live on the persistent-data partition.

## Access

- **Network:** the camera exposes file transfer over WiFi, which is how bulk
  data is pulled off it.
- **RCP:** the RED Command Protocol (documented by RED's own SDK) is the
  sanctioned way to control and automate the camera over Ethernet.
