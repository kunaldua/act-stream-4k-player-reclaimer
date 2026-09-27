---
name: act4k1007-reclaimer
description: Recover an ACT4K1007 or SDMC DV8919 box on the verified C2.3.7 Android 9 firmware. Use when diagnosing or replacing the discontinued ACT setup experience; use read-only discovery for other firmware.
---

# ACT4K1007 Reclaimer

Help the owner recover this box through the tested launcher-first path. Do not
turn a similar product name into an assumed hardware match.

## Boundaries

- Work only on a box the user owns or is authorized to modify.
- Do not bypass ACT accounts, subscriptions, DRM, Factory Reset Protection, or
  any other authentication or activation control.
- Do not root, unlock, flash, repartition, format, or disable verified boot.
- Treat the device as unsupported unless every required identity value matches
  `references/act4k1007-c2.3.7.json` in this skill.
- Preserve ACT packages other than the tested per-user SetupWraith removal.
- Never publish raw logs, pairing keys, ADB keys, serials, MAC addresses,
  Android IDs, account names, or home paths.

## Route the request

1. For a new or uncertain box, read
   [references/discovery.md](references/discovery.md) and perform only the
   read-only checks.
2. Once the exact profile matches, read
   [references/recovery.md](references/recovery.md) and work through one state
   transition at a time.
3. For failures or differences between units, read
   [references/troubleshooting.md](references/troubleshooting.md). Do not retry
   a failed mutation with broader flags.
4. For reversal, read [references/rollback.md](references/rollback.md).

## Approval contract

Read-only host checks, port checks, ADB enumeration, property reads, package
queries, and local checksum verification may proceed without confirmation.

Immediately before every command that changes the device:

1. show the exact command;
2. explain its expected visible effect;
3. state the main failure mode;
4. give the rollback command or say why immediate rollback is unavailable;
5. state whether personal data can be erased; and
6. obtain explicit user confirmation for that state transition.

Prior approval for the overall recovery is not approval for later mutations.
Stop on an unexpected identifier, checksum, package-manager response,
disconnect, ambiguous ADB target, or missing rollback path.

## Completion

Finish with the verification checklist in `references/recovery.md`. Report
what changed, what remained installed, the tested rollback, and any known
remote-button limitation. Do not claim that Android 9 is modern, secure, or
vendor-supported merely because the launcher is usable.
