# RED ONE (PowerPC / VxWorks)

The original **RED ONE** is a different, older generation: a **PowerPC 405**
running **VxWorks**, with a Xilinx **IOFPGA** doing the I/O and sensor path. None
of the DSMC2/MX firmware carries over — different CPU, different OS, different
container, different keys. It is included here because its upgrade format is now
fully solved, so RED ONE owners can unpack and study their firmware too.

Reference image: **build 16, v3.2.5** (plus the plaintext `su.tar` from build 15,
v2.2.8, used as the crib that cracked the format).

## The `redone.su` format

The upgrade file is **not a custom cipher**. It is a plain POSIX **tar** with four
members:

| member | content |
|---|---|
| `redone.1` | openssl `enc` AES-256-CBC → gzip → VxWorks PPC405 image (SundanceBootable, ~12.9 MB) |
| `redone.2` | 128-byte RSA-1024 signature over `redone.1` |
| `redone.3` | openssl `enc` AES-256-CBC → gzip → Xilinx FPGA bitstream (iofpga_top, ~4.1 MB) |
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

## Opening the firmware

Use [tools/redone-su/redone_su_decrypt.py](../../tools/redone-su):

```
python3 redone_su_decrypt.py redone.su out/
```

It unpacks the tar, AES-decrypts and inflates `redone.1`/`redone.3` into the
VxWorks image and FPGA bitstream, and saves the two signatures. The decrypted
VxWorks image is a full build (OpenSSL 0.9.8a, source paths under
`/home/sundance/release/SW/Src/bsp_ppc405_0_revB/...`); its upgrade reader looks
for `redone.su` on `/{tffs0,ata00:1,ata10:1,sdmc,usbd0}/upgrade/`.

## What this does and doesn't give you

The two signatures (`redone.2`/`redone.4`) are RSA-1024 over the encrypted
payloads; the **signing** key is not published and is not in the firmware, so this
is read/study access, not a path to repacking a signed `redone.su`. For
preservation that is enough: you can decrypt, inspect and archive both the VxWorks
image and the FPGA bitstream from any build you hold.
