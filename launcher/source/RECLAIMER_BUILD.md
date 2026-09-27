# FLauncher ACT compatibility build

This directory is a modified build of FLauncher 0.18.0, licensed under
GPL-3.0-or-later. The complete corresponding source is retained here.

## Upstream

- Project: https://gitlab.com/flauncher/flauncher
- Release: 0.18.0
- Source commit: `4930cd738a5ab32967953fe8b12790bc4b452872`
- Upstream release date: 2023-04-21

## Changes

1. The Android application ID is changed from `me.efesser.flauncher` to
   `org.reclaimer.actcorpcompat.flauncher`. The ACT/Skyworth Android 9
   firmware rejects third-party HOME handlers unless their package name
   contains one of its embedded OEM compatibility strings.
2. The visible app name is `FLauncher (Reclaimer)` so this build is not
   presented as upstream or vendor software.
3. Firebase Analytics, Crashlytics, and Remote Config are removed. Unsplash
   integration remains disabled because it depended on Remote Config keys.
4. The local build version is `0.18.0+18001`.

This build does not impersonate or grant access to ACT services. The package
identifier only satisfies the device's local launcher-install compatibility
check on user-owned hardware.

## Local release build

The release signing block reads `SIGNING_KEYSTORE_PATH`,
`SIGNING_KEYSTORE_PASSWORD`, `SIGNING_KEY_ALIAS`, and `SIGNING_KEY_PASSWORD`
from the environment. Preserve the generated keystore: Android requires future
updates to use the same signing identity.
