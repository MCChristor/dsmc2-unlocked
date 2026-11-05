# Extracting the Filesystem and Firmware

This page explains how to pull files off the camera — individual files, the whole
filesystem (~489 files, 163 MB), or the firmware image itself. It is the method
that [keys.md](keys.md) refers to when it says "pull the image off the camera".

It uses only stock shell verbs and the WiFi file-transfer service. Nothing is
patched, no memory is written, no gate is flipped, and the camera stays stock —
the only write is a scratch file the tool deletes after each pull.

## Why it works

The shell verbs that read a file by name — `nand cat`, `cp`, `mv`, `base64`,
`show-sector` — are compiled out behind `ENABLE_ADVANCED_SHELL_COMMANDS`. But
**`nand zlib` is not gated**, and it also reads any absolute path (it writes a
zlib-compressed copy to a path you choose). The WiFi file-transfer service (RFTP)
can read back the user export folders (`/luts`, `/looks`, `/presets`, …). So:

1. On the camera, `nand zlib` compresses the target file into an exported folder.
2. Over WiFi, RFTP pulls that compressed copy.
3. On the computer, strip the 12-byte header and inflate.

This is not an exploit — it is a stock feature used with the permissions it
shipped with.

## The container format

`nand zlib` writes:

```
offset 0   "REDZLIB0"      8-byte magic
offset 8   u32 LE          uncompressed length
offset 12  zlib stream
```

This is the same format the firmware's own `read_compressed_file` consumes. To
unpack: check the magic, read the length, inflate from offset 12.

## Manual recipe (one file)

```
# 1. camera shell — compress into an RFTP-exported folder
nand zlib -c /image2/doc/RedUiCalibrationDialog.wiki /pdata/data/luts/_x.z

# 2. computer — pull it over WiFi (RFTP client)
rftp <camera-ip> get /luts/_x.z /tmp/_x.z

# 3. unpack (strip the 12-byte header, inflate), then clean up on the camera
nand rm /pdata/data/luts/_x.z
```

**Filenames with spaces must be double-quoted** on the camera shell, or the verb
splits them and fails:

```
nand zlib -c "/image2/overlays/3D Left (RED).overlay" "/pdata/data/luts/_x.z"
```

## The firmware image

The on-NAND application image is `/image2/dsmc_program.mem` (about 21.6 MB). Pull
it the same way:

```
nand zlib -c /image2/dsmc_program.mem /pdata/data/luts/_big.z
rftp <camera-ip> get /luts/_big.z dsmc_program.mem
```

This is the plaintext image the keys and tools in this repo work against. (It is
the pristine on-NAND copy; a live RAM dump of the running code differs by a small
fraction because the running image mutates itself in place.)

## File-size cap

The common RFTP client has a **16 MB single-file cap**, and it is client-side only
(a constant in the client source). Rebuild it with a larger cap to pull the
firmware image or other big files — the camera side has no such limit at these
sizes. There is **no** chunked or resumed transfer: a file is pulled whole or not
at all, so the client holds it in RAM until complete. Camera-side counters are
32-bit (~2 GB ceiling), which nothing here approaches.

## What you can and cannot reach

- **Reachable:** `/env`, `/image2`, `/rodata`, `/pdata`, `/data`, and anything you
  can stage with `nand zlib` into an exported folder.
- **The inactive OS slot** `/image1` is normally unmounted; `nand remount /image1 RO`
  (ungated) mounts it so it can be read the same way.
- **Not reachable this way:** the `/log` NAND partition is not exported by RFTP
  (stage its contents instead), and the OMAP on-chip boot ROM cannot be read at all
  (`read reg` on its address faults the camera).

## Coprocessor firmware lands here too

A full pull includes the firmware images for the other processors under
`/image2/`: `isp/`, `iob0/`, `iob1/`, `lsbfpga/`, `dsp/`, `redpine/`, `lens/`,
`reardevices/`, `peripherals/`. Which of these are plaintext and which are sealed
is covered in [peripheral-firmware.md](../hardware-fw/peripheral-firmware.md).
