# MINI-MAG Authentication

The camera authenticates an inserted drive with **two independent checks**. The
whole scheme was recovered from the camera firmware and reproduced offline; it
uses only standard MD5 and plain string matching.

## The two gates

### 1. Model-string whitelist (hard gate)

At insert, the camera reads the drive's **ATA IDENTIFY model string** (the usual
16-bit-word byte-swapped ATA string, trimmed of surrounding whitespace) and
compares it, with an **exact match**, against a list of approved model strings
compiled into the firmware. See [media-table.md](media-table.md) for the full
list.

- If the model does not match, the drive is treated as unknown media and is not
  usable as a recording mag.
- The two most useful approved strings are **`RED 512GB V5`** and
  **`SAMSUNG MZMTE1T0HMJH-00000`**.

### 2. SMART-log MD5 signature (soft gate)

The camera then reads a **vendor SMART log, page 0x90**, which holds a signature,
and recomputes the expected signature to compare.

- **Valid signature** → the drive is treated as a genuine RED product and runs at
  full data rate.
- **Wrong or absent signature** → the drive **still mounts and records**, but the
  firmware flags it "not a properly signed RED product" and caps throughput to
  about **30 MB/s**. Fine for stills or low bitrate; too slow for high-bitrate
  R3D.

So the model string is mandatory; the signature is what you need for full speed.

## The signature algorithm

The 16-byte value is a **standard MD5**. It is not RSA, not a CRC, not a fixed
constant. A SMART page-0x90 record is 17 bytes:

```
signature = [ type_byte ] || MD5( digest_input )
```

`digest_input` is, in order:

```
1. salt      6 bytes   (depends on signature type, below)
2. wwn8      8 bytes   (derived from the drive's ATA IDENTIFY World Wide Name)
3. serial    variable  (ONLY for signature types 2 and 3; omitted for type 1)
4. model     variable  (the trimmed ATA IDENTIFY model string)
```

Standard MD5 (IV `67452301 efcdab89 98badcfe 10325476`).

### Signature types

| Type | Meaning |
|---|---|
| 0 | Unsigned |
| 1 | RED signature (does **not** hash the serial) |
| 2 | PV DXL signature |
| 3 | RED signature, serial-bound variant |

### Salts

| Type | Salt (6 bytes) |
|---|---|
| 1 and 3 | `82 3C 16 F5 4A 9C` |
| 2 | `29 C9 E5 2D 08 C6` |

### The WWN block (`wwn8`)

`wwn8` is built from the drive's ATA IDENTIFY World Wide Name (IDENTIFY words
108–111):

```
naa  = word108 & 0x0F
acc  = naa | (word110 << 16) | (word111 << 32)
wwn8 = little-endian 8 bytes of acc
```

Word 109 (the top 16 bits of the full WWN) is not used.

## The important shortcut

On the genuine drive that was captured, the **WWN reads as all zeros**. That
collapses a type-1 signature to `MD5(salt || 00·8 || model)` — **salt and model
only**. Verified against a real magazine:

```
MD5( 82 3C 16 F5 4A 9C  ‖  00 00 00 00 00 00 00 00  ‖  "RED 512GB V5" )
  = c918922e75575f9b989f55c6f1778f7d

genuine page-0x90 record (captured):
  01 | c9 18 92 2e 75 57 5f 9b 98 9f 55 c6 f1 77 8f 7d    ← exact match
```

So for the model string **`RED 512GB V5`** the full 17-byte page-0x90 record is a
**constant you can write verbatim** onto any drive that reports that model and a
zero WWN:

```
01 C9 18 92 2E 75 57 5F 9B 98 9F 55 C6 F1 77 8F 7D
```

A drive that reports a **non-zero** WWN hashes differently, so the copied bytes
will not validate on it. For such a drive, either zero its WWN, or recompute the
MD5 from that drive's own WWN with the formula above.

## Page 0x91 is optional

There is a second SMART page, **0x91**, holding an RC4-encrypted "media
characteristics" block. It is optional: if it is missing, the camera falls back
to the built-in media table (which is exactly what the captured genuine mag did).
You do not need to produce it. The RC4 key, if ever needed, is derived from the
drive's own serial/model/WWN, not a hidden camera secret.

## Reproducing it offline

Everything above is computable with any MD5 library. You need the target drive's
ATA IDENTIFY (for the model and the WWN words), then:

```python
import hashlib
SALT1 = bytes.fromhex("823c16f54a9c")

def red_type1_signature(model: str, wwn8: bytes = b"\x00"*8) -> bytes:
    md5 = hashlib.md5(SALT1 + wwn8 + model.encode()).digest()
    return bytes([0x01]) + md5

# RED 512GB V5 with a zero-WWN drive:
print(red_type1_signature("RED 512GB V5").hex())
# -> 01c918922e75575f9b989f55c6f1778f7d
```

Write those 17 bytes to the drive's SMART GPL log page 0x90 with the SSD
vendor's tool (or any host utility that permits a GPL log write). No camera-side
step is required.
