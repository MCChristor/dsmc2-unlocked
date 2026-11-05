# Code injection — the method behind the custom firmware

> **Status page, not a how-to.** This explains *how* the custom firmware runs its own
> code on the camera and why that is sound. It is not a build-it-yourself guide, and
> you should **not** patch your own body from it — see [builds.md](builds.md).

The DSMC2 application is an ARM firmware on a flat-memory real-time OS (ThreadX, no
MMU, no write-protect on code). That combination means a small block of your own
compiled code, placed in an unused region of the image, can call the firmware's own
functions directly. This is the method behind "you can produce modified firmware the
camera accepts" ([whats-possible.md](whats-possible.md)); the bootloader does not
verify the application image ([keys.md](keys.md)), so a modified image boots.

## Why it works

- **The app is ARM, not Thumb.** Every function uses the compiler's standard prologue,
  and an ARM `BL` interworks automatically — your code can branch-and-link into any
  resident function with no special handling.
- **Flat memory, no W^X.** ThreadX runs everything in one address space with code and
  data both writable. A blob dropped into a code gap can call anything already loaded.
- **The functions are named.** The firmware logs through macros that embed each
  function's own `__FILE__`/`__FUNCTION__` string. Recovering those gives thousands of
  real `Class::method` names at known addresses — so injected C can be written against
  the firmware's own API by name, not against raw offsets.

## How a module is built (conceptually)

1. Take the recovered name→address list and turn it into linker symbol definitions, so
   a C file can reference firmware functions and the OS services (ThreadX/FileX) by name.
2. Compile a small C module with a stock `arm-none-eabi-gcc`, linked to sit at a chosen
   unused region of the image. No RED source and no commercial toolchain are needed —
   the camera's own functions are the library.
3. Place the resulting blob at that region (per-boot over the serial shell, or
   permanently in a firmware image) and point one existing code path at its entry.

The result is ordinary C that calls the camera's real functions. It is the clean,
build-controlled alternative to byte-patching: readable, recompilable, and portable
across bodies (the application binary is identical across DSMC2 models).

## What it enables (in the coming build)

- **Reliability and repair fixes** — e.g. the log-spam fix and the SATA write-retry
  improvement ([reliability.md](reliability.md)).
- **Reimplementing engineering shell commands** that ship as compile-time stubs, as
  clean C against the current firmware's functions (rather than byte-porting a
  different build, whose internal call targets would all differ).
- **A build system** — a stock "production" image plus an engineering "dev" image are
  just two sets of these modules over the same base ([builds.md](builds.md)).

## Boundaries

- Placement is absolute and unforgiving: the module is linked to a fixed region that must
  be genuinely unused, and every injected call must be confirmed to land on the intended
  firmware address before anything runs. Getting this wrong on an early-boot path can stop
  a camera booting. This is exactly why the published build is being hardened and verified
  first, and why this page is not a recipe.
- This runs code on the **application** processor. It does not touch the signed
  environment block (a key no one holds) and it is not a network attack surface — it is
  a local, owner-side modification path.
- Exact symbol maps, addresses, and the build tooling are kept in the private research
  notes; this page documents the technique, not a turnkey kit.
