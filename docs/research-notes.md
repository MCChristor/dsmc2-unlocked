# Research Notes — Difficulties and Insights

The story behind the findings: what was hard, what surprised us, and the ideas
that unblocked the work. This is deliberately at the level of *what happened and
why it mattered* — not a how-to. Methods, addresses, and access steps are not
here.

## Getting data off the camera was the first wall

The obvious low-level readout path is extremely slow — on the order of a few
kilobytes per second. At that rate a full copy of the camera's filesystem (around
**490 files, ~160 MB**) would take roughly **half a day** and tie up the bench the
whole time. Early on this throttled everything: every hypothesis that needed a new
file to check meant another long wait.

**The insight that fixed it:** the firmware already contains a general-purpose
**compression/copy facility** (the camera uses zlib internally for its own NAND
data). Rather than stream raw bytes slowly, you can have the camera compress a
file in place and then move the compact result off over the network. That turned a
~12-hour bulk copy into **minutes**, and it uses only functionality the firmware
shipped with. Once bulk extraction was cheap, the pace of the whole project
changed — you could pull anything, diff it, and move on.

Lesson: on an embedded target, look for a shipped feature that already does the
heavy lifting (compression, a file utility, a network service) before building a
custom exfiltration path. The device's own tools are faster and less fragile than
anything bolted on.

## The firmware had a layer we did not expect

A first analysis of the firmware packaging concluded, confidently, that it was
"fully solved." It was not. A rigorous re-check showed the first pass had **read a
container header field as if it were plaintext** when the body underneath was
still encrypted — the decrypted output still had near-maximum entropy, the
signature of data that is not actually decrypted.

Correcting that meant separating **two independent layers**: an outer wrapper that
we fully understand, and an inner layer that is a different cipher entirely. The
practical upshot is nuanced — some artifacts are readable because the camera does
both steps internally when it loads them, while the same files sitting on disk stay
opaque. Keeping that distinction straight mattered for every later claim about what
is and is not "cracked."

Lesson: entropy is the honesty check. If your "decrypted" output is still
8-bits-per-byte random, you have not decrypted it — you have renamed it. We now
treat an entropy measurement as a required gate before calling anything solved.

## Self-correction was a running theme

Several early notes were later marked wrong and superseded on purpose, and the
record keeps both versions. A few examples:

- A claimed "inner key" that gated firmware turned out **not to exist** the way the
  first pass described; the packaging is simpler than feared in one respect and
  more layered in another.
- A boot-chain assumption ("we need a specific low-level block to proceed") was
  overturned when the relevant loader was obtained another way and shown **not to
  verify** what the first theory assumed it did.
- In the media work, an early reading mis-split a byte of the signature as a
  separate trailer; it is actually the last byte of the hash.

Keeping the wrong turns visible, with the reason each was wrong, is deliberate. It
is also why the public docs hedge where the device evidence stopped — see the
caveats in [whats-possible.md](whats-possible.md) and [models.md](models.md).

## Not everything on the camera is safe to touch

Mapping the processor's memory is useful, but **some regions crash the camera when
read** — boot ROM, certain peripheral and crypto register areas, and a couple of
coprocessor test paths. Only the main application memory window is reliably safe.
A fair amount of early effort went into building that safe-vs-dangerous map, and
respecting it is what let the later work proceed without constant reboots.

Lesson: on a flat-memory system with no protection, "just read everything" is a
good way to lock up the device. A conservative, tested region map is worth the
time it takes to build.

## The media lock looked stronger than it was

The MINI-MAG authentication *looked* like it might be real cryptography — a signed
blob the camera validates. It is not. Taken apart, it reduces to a plain, standard
hash over a few identity fields plus a simple exact-string match. There is no
public-key signature protecting it, no server, and no device-unique secret you
cannot derive. The full, honest write-up is in the [media](../media/) folder,
precisely because the media is discontinued and the lock turned out to be a
convenience gate, not a security boundary.

Lesson: name the primitive before you assume strength. "Signature" in a vendor's
code can mean an RSA signature or an MD5 over a salt — those are very different
threat models, and only disassembly tells you which one you are actually facing.

## What made the platform tractable

A few properties of the DSMC2 made all of this feasible:

- **A flat, no-MMU real-time OS.** No process isolation means that once you can run
  or observe code, the whole address space is visible and coherent. This cuts both
  ways — it is also why careless reads crash the box — but it makes analysis
  direct.
- **Mostly standard, identifiable components.** SQLite, zlib, a well-known crypto
  library, a common flash filesystem, XML manifests. Recognising a stock component
  tells you its format for free and saves reverse-engineering it from scratch.
- **Plaintext per-model manifests.** Model differences are legible because the
  resource manifests are plain XML, which is what let us separate "identity is
  config" from "capability is hardware" honestly.

None of these are secrets; they are observations about how the camera is built,
and they are the reason a single-person project could make progress.
