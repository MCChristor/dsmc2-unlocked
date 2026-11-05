# DSMC1 — The Earlier Generation

This repository's primary subject is the **DSMC2** platform. This page is the
companion reference for the earlier **DSMC1** cameras, so an owner with a DSMC1
fleet can use one set of notes across both generations.

"DSMC1" is really **two different machines** under one marketing name, and they
share almost nothing internally. Knowing which one you hold decides everything —
firmware format, keys, processor, tooling:

| Branch | Bodies | Processor / OS | Firmware file |
|---|---|---|---|
| **DSMC1 MX / Dragon** | EPIC (M-X), SCARLET (M-X), **EPIC DRAGON**, SCARLET Dragon | TI OMAP-class **ARM**, same family as DSMC2 | v2 `DSMC` package (`.bin`) |
| **RED ONE** | RED ONE, RED ONE MX | **PowerPC 405** + VxWorks + Xilinx IOFPGA | `redone.su` (or `su.tar` on old builds) |

The MX/Dragon branch is **one generation behind DSMC2 and nearly identical** to it.
The RED ONE branch is **older and unrelated** — a completely separate platform that
happens to share the DSMC1 label. Both are now fully opened; they just need
different tools. Everything below is verified against real images, not assumed.

- Reference MX/Dragon image: **Epic Dragon build v6.3.106** (camera-type tag
  `0x0f`, released 2017-12-20) — the last build for EPIC, SCARLET and Dragon.
- Reference RED ONE image: **build 16, v3.2.5** (and the plaintext `su.tar` from
  build 15, v2.2.8, used as the crib that cracked it).

---

## Part 1 — DSMC1 MX / Dragon (EPIC · SCARLET · Dragon)

Same architecture as DSMC2, one generation apart. The firmware container, its
encryption, the main processor family and the coprocessor design are shared. The
differences are in *how many* of each part the body has and which extra chips are
present.

### What is identical to DSMC2

- **Firmware container.** DSMC1 MX/Dragon updates are the same `DSMC`-magic **v2**
  package as DSMC2 single-model updates. See [firmware.md](firmware.md).
- **Encryption and keys.** The v2 package uses the same RSA-OAEP(SHA-1, label
  `dsmc`) → RC4 design and opens with the **same published v2 key** — no new key
  material is needed. Verified by unpacking Epic Dragon 6.3.106 with the
  repository's own [unpacker](../tools/fw-crypto). See [keys.md](keys.md).
- **Config-file cipher.** The `.cfg` files (camera config, lens tables) use the
  same reused-keystream stream cipher, so the same recovered keystream reads DSMC1
  configs too. See [feature-unlock.md](feature-unlock.md).
- **Main processor.** TI OMAP-class ARM running `dsmc_program.mem`, same as DSMC2.
- **ISP and IOB run Xtensa code, loaded from NAND.** DSMC1's `CAMERA_CONFIG.cfg`
  names the loader paths `TENSILICA_ISP_BIN_PATH` and
  `TENSILICA_IOB0/IOB1/PROIO_IOB0_BIN_PATH`, and the ISP instruction-RAM bootstrap
  is byte-identical to DSMC2 — so both generations use the same part. The image
  disassembles cleanly as Xtensa (see [platform.md](platform.md)), which confirms
  the ISA. **Fabric type (ASIC vs FPGA) is still not settled by the firmware** —
  Xtensa runs in both, and the image uses both words.

Because the container, keys, config cipher, shell and subsystem layout all carry
over, most of this repository — [feature-unlock.md](feature-unlock.md),
[serial-shell.md](serial-shell.md), [shell-commands.md](shell-commands.md),
[calibration.md](calibration.md), [subsystems.md](subsystems.md) — reads across to
MX/Dragon bodies with the counts adjusted below.

### What differs from DSMC2

| | DSMC1 (Epic Dragon) | DSMC2 (Scarlet-W) |
|---|---|---|
| IOB cores | **1** (`iob0`) | **2** (`iob0`, `iob1`) |
| Large FPGA | genlock FPGA only | + **LSB Xilinx Kintex-7** |
| Wireless | none in the image | **Redpine** Wi-Fi/BT module |
| Coprocessor topology | 2 ISP, 1 IOB, 60 ISP slices | 2 ISP, 1 IOB, 60 ISP slices (same shape) |
| Application image | ~17.7 MB | ~21.6 MB |
| Body-specific trees | `turret4k/` | FlatUI, more rear devices |

The ISP/IOB **instruction images differ build-to-build** (different sizes), as
expected; it is the *encoding and bootstrap* that are shared, not the exact bytes.

### Getting and opening MX/Dragon firmware

RED distributes these builds through its own firmware download page. The relevant
bodies are **Epic Dragon**, **Epic (M-X)** and **Scarlet (M-X)**; the last build
for all three is v6.3.106. (These are distinct from the DSMC2 Epic-W / Scarlet-W,
which are the `weapon` family.)

Each download is a `.zip` holding a read-me and one `force_upgrade/*.bin`. The
`.bin` is the v2 package; unpack it with
[tools/fw-crypto/unpack_combo.py](../tools/fw-crypto):

```
python3 unpack_combo.py epic_dragon_6.3.106.bin --extract --out out/
```

---

## Part 2 — RED ONE (PowerPC / VxWorks)

The original **RED ONE** is a different, older generation: a **PowerPC 405**
running **VxWorks**, with a Xilinx **IOFPGA** doing the I/O and sensor path. None
of the DSMC2/MX firmware carries over — different CPU, different OS, different
container, different keys. It is included here because its upgrade format is now
fully solved, so RED ONE owners can unpack and study their firmware too.

### The `redone.su` format

The upgrade file is **not a custom cipher**. It is a plain POSIX **tar** with four
members:

| member | content |
|---|---|
| `redone.1` | openssl `enc` AES-256-CBC → gzip → VxWorks PPC405 image (SundanceBootable) |
| `redone.2` | 128-byte RSA-1024 signature over `redone.1` |
| `redone.3` | openssl `enc` AES-256-CBC → gzip → Xilinx FPGA bitstream (iofpga_top) |
| `redone.4` | 128-byte RSA-1024 signature over `redone.3` |

The AES layer is `openssl enc -aes-256-cbc -md md5` (`Salted__` header + 8-byte
salt, legacy `EVP_BytesToKey` MD5 KDF). The passphrase is a constant string sitting
in the VxWorks image's own string table — an **obfuscation key, not a secret**, the
same situation as the published v2/v3 keys. It is baked into the tool.

Firmware history across the format change:

- **Build 15 (v2.2.8)** and earlier ship the two payloads in the clear as
  `su.tar` (`iofpga_top.bin.gz` + `SundanceBootable.bin.gz`).
- **Build 16 (v3.2.5)** onward wrap the same payloads in the encrypted
  `redone.su`. The `v3.2.5` package conveniently ships the plaintext `su.tar` and
  the encrypted `redone.su` side by side — that pairing is what recovered the key.

### Opening RED ONE firmware

Use [tools/redone-su/redone_su_decrypt.py](../tools/redone-su):

```
python3 redone_su_decrypt.py redone.su out/
```

It unpacks the tar, AES-decrypts and inflates `redone.1`/`redone.3` into the
VxWorks image and FPGA bitstream, and saves the two signatures. The decrypted
VxWorks image is a full build (OpenSSL 0.9.8a, source paths under
`/home/sundance/release/SW/Src/bsp_ppc405_0_revB/...`); its upgrade reader looks
for `redone.su` on `/{tffs0,ata00:1,ata10:1,sdmc,usbd0}/upgrade/`.

---

## Which body do I have?

| You see… | Branch | Firmware |
|---|---|---|
| EPIC, SCARLET, or DRAGON badge; takes a MINI-MAG or SSD mag; menu like a DSMC2 | **MX / Dragon** | v2 `.bin`, [fw-crypto](../tools/fw-crypto) |
| RED ONE badge; CF / RED-DRIVE / RAM media; older boxy body | **RED ONE** | `redone.su`, [redone-su](../tools/redone-su) |

Unsure from the outside? Check the firmware file the body accepts: a `DSMC`-magic
`.bin` is MX/Dragon; a `redone.su` (or `su.tar`) is RED ONE.

## Status

Both DSMC1 branches are on RED's no-longer-repairable list, which is the reason
their firmware is documented here for preservation. MX/Dragon is covered by the
whole repository (same platform as DSMC2); RED ONE is covered for firmware
unpacking and study. The custom-firmware work in [builds.md](builds.md) targets
**DSMC2**; it is not built or verified for DSMC1 bodies — do not apply DSMC2 build
material to a DSMC1 camera.
