# Rollback

Rollback is composed of separate state transitions. Explain and confirm each
device-changing command before running it.

## Restore SetupWraith for user 0

```bash
adb -s "$SERIAL" shell cmd package install-existing --user 0 \
  com.google.android.tungsten.setupwraith
```

This restores the system package for the primary user without downloading an
APK. Verify the returned package name and query the Home resolver.

## Restore the original setup-state values

The two tested boxes began with `user_setup_complete=0` and no
`tv_user_setup_complete` value:

```bash
adb -s "$SERIAL" shell settings put secure user_setup_complete 0
adb -s "$SERIAL" shell settings delete secure tv_user_setup_complete
```

Do not assume those were another box's original values; capture the initial
state before recovery.

## Remove FLauncher

First ensure SetupWraith or another known Home activity is available. Then:

```bash
adb -s "$SERIAL" uninstall org.reclaimer.actcorpcompat.flauncher
```

This removes FLauncher and its local preferences. It does not remove personal
media. Verify Home resolution before rebooting.

## Recovery stop condition

If no Home activity resolves, keep ADB connected and launch Android TV Settings
directly. Do not reboot until a known Home activity is restored.
