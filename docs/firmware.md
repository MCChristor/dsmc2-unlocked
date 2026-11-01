# Firmware Packaging and Encryption

This document explains how RED packages and protects DSMC2 firmware. It gives the
formats and the encryption design. It tells you which algorithms are used and how
the layers fit together. It does not give keys, key locations, or a ready-to-run
unpacker.

Written in simplified technical English.

## Two package formats: v2 and v3

A firmware update file is a container. There are two container formats. They are
**file formats, not firmware versions**. One version byte near the start of the
file sets which format it is. The camera accepts both.

| Item | v2 — "standalone" | v3 — "combo" |
|---|---|---|
| Models per file | One | Several |
| Contents | Manifest, bootloader, and the slot image for one model | A table of contents that points at one slice per model |
| Model choice | Not needed — it is already one model | The camera reads the table and picks the slice for its own model |
| Typical use | Older single-model updates | Current multi-model updates |

A v3 combo starts with a table of contents. The table is a count, then one entry
per model. Each entry gives a model type and the position of that model's slice in
the file. At install time the camera reads the table. It finds the entry for its
own model type. It uses only that slice.

This is the packaging side of a fact in [models.md](models.md): model identity is a
small piece of data. One file holds every model. One value picks the model.

## The encryption has two layers

A packaged image has **two separate encryption layers**. You must remove both
layers to get readable firmware. This two-layer design was easy to misread. See
[research-notes.md](research-notes.md).

### Outer layer — understood

The outer layer is a standard design:

1. **Each image has its own random content key.** The build step makes a fresh
   **RC4** key for each image. The key is not reused.
2. **RSA protects that key.** The per-image RC4 key is encrypted with **RSA and
   OAEP padding (SHA-1, with a fixed label)**. The matching RSA private key is
   inside the camera firmware. So the camera can recover the content key. A person
   without that key cannot.
3. **RC4 protects the body.** The image body is RC4-encrypted with the content key.
   Inside the v2 body is a zlib-compressed, readable structure.

This is a clean and common design. You wrap a random session key with a public-key
cipher. You encrypt the bulk data with a fast stream cipher. The private key sits
in the firmware, so the outer layer is reversible once you recover that key from an
image. This document does not publish the key.

The OAEP padding has a useful side effect. It checks itself. With the right key the
padding is valid and the RC4 key comes out clean. With the wrong key it fails at
once. This gave a clear "this key is correct" signal during analysis, with no
guessing.

### Inner layer — not solved

Under the RC4 body there is **another layer**. The real firmware content is also
**AES-encrypted**. The AES is a software AES from the same crypto library the
camera uses in other places. It runs in a stream-like mode, not simple block mode.
The key for this inner layer is not one of the keys from the outer analysis. This
layer is not broken.

### Why some files are readable and others are not

The two-layer design explains an apparent contradiction in the project.

- **A firmware image on disk stays locked.** The inner AES layer is intact and that
  key is not available.
- **A copy from the camera's running memory is plain text.** To run the code, the
  camera does both decryptions itself. By the time the code runs, the firmware is
  fully decrypted in memory.

So the readable data in this project came from the live camera doing the work. It
did not come from breaking the inner cipher offline. This is why the docs never say
the inner layer is "cracked."

## What this allows and does not allow

- **Read and compare firmware:** yes. Use the outer layer and the camera's own
  in-memory decryption. You can analyse and compare builds.
- **Make a package the camera accepts:** this needs the inner layer, which is not
  solved offline. Running modified firmware may not use the package path at all,
  but that route is not documented here.
- **Get the keys for other people:** no. The keys stay private by design. This
  document gives the construction, not the key material.
