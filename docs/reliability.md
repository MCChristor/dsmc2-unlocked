# Reliability findings

Reverse engineering turns up genuine bugs, not just locks. These are repair-positive
findings — they explain real failures and will be addressed by the coming custom
firmware ([builds.md](builds.md)). They are documented here as findings; this is not a
patch-it-yourself page.

## SATA write has no retry (real, worth fixing)

The recording write path, on any I/O error, returns the failure immediately — **no retry,
no re-queue**. A hardware SATA error is only logged. The practical effect: a single
transient SSD/SATA glitch aborts the write and ends the clip ("recording stopped, media
error"), even though a retry would have absorbed it. On marginal drives, long cables, or
non-RED SSDs this is the difference between a dropped take and a clean one. The fix —
re-queue the failed transfer once or twice before giving up — is slated for the custom
build's production image.

## Log spam

A configuration-apply path logs every key/value it applies — thousands of lines on a
healthy body each time settings are applied — flooding the already-slow log path. A
one-instruction change silences it; it is part of the production image.

## Note on firmware upgrades

The firmware-upgrade path resets the configuration database to factory on the next boot,
which wipes config-DB-based unlocks (the licence-file path survives). Worth knowing
before an upgrade.
