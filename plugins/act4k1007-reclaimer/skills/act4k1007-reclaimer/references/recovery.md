# Verified recovery workflow

Use this only after `verify_device.py` reports an exact match. Execute one
device-changing transition at a time under the approval contract in SKILL.md.

Set these local shell values without writing to the device:

```bash
SERIAL='192.0.2.10:5555'
APK='/absolute/path/FLauncher-0.18.0-actcorpcompat.1-armv7-release.apk'
```

## 1. Verify the release APK locally

```bash
python3 scripts/verify_release.py "$APK"
```

Required SHA-256:

```text
ed239a27be2ae3310c16bb21760aed96a8807b4c5881ccc8d4b8d151246eed9a
```

Stop on a mismatch. The expected package is
`org.reclaimer.actcorpcompat.flauncher` version
`0.18.0-actcorpcompat.1`, ARMv7, minimum SDK 21.

## 2. Install the launcher

```bash
adb -s "$SERIAL" install "$APK"
```

Expected result: `Success`. Main failure: Package Manager rejects the APK.
Rollback removes only the newly installed launcher:

```bash
adb -s "$SERIAL" uninstall org.reclaimer.actcorpcompat.flauncher
```

No personal media should be erased, but uninstalling later removes the
launcher's own settings.

## 3. Launch and test once

```bash
adb -s "$SERIAL" shell am start -n \
  org.reclaimer.actcorpcompat.flauncher/me.efesser.flauncher.MainActivity
```

Verify visible focus, D-pad navigation, application launch, and a working
route to Android TV Settings before proceeding. Keep the ACT launcher and
fallback launcher installed.

## 4. Complete the Android per-user setup gates

Apply and verify each value separately:

```bash
adb -s "$SERIAL" shell settings put secure user_setup_complete 1
adb -s "$SERIAL" shell settings get secure user_setup_complete
```

Rollback:

```bash
adb -s "$SERIAL" shell settings put secure user_setup_complete 0
```

Then:

```bash
adb -s "$SERIAL" shell settings put secure tv_user_setup_complete 1
adb -s "$SERIAL" shell settings get secure tv_user_setup_complete
```

Rollback to the original unset state:

```bash
adb -s "$SERIAL" shell settings delete secure tv_user_setup_complete
```

These settings do not erase personal files.

## 5. Record FLauncher as preferred Home

```bash
adb -s "$SERIAL" shell cmd package set-home-activity --user 0 \
  org.reclaimer.actcorpcompat.flauncher/me.efesser.flauncher.MainActivity
```

Expected result: `Success`. Verify with:

```bash
adb -s "$SERIAL" shell dumpsys package preferred-activities
```

SetupWraith can still resolve first because its system Home filter has higher
priority. Do not disable arbitrary components.

## 6. Remove SetupWraith only from user 0

```bash
adb -s "$SERIAL" shell pm uninstall -k --user 0 \
  com.google.android.tungsten.setupwraith
```

Expected result: `Success`. The system APK remains on the read-only system
partition and `-k` retains its app data. This removes deferred setup and its
bundled OTA helper for user 0; it does not erase personal media.

Rollback:

```bash
adb -s "$SERIAL" shell cmd package install-existing --user 0 \
  com.google.android.tungsten.setupwraith
```

## 7. Verify before pressing Home

Read-only checks:

```bash
adb -s "$SERIAL" shell settings get global device_provisioned
adb -s "$SERIAL" shell settings get secure user_setup_complete
adb -s "$SERIAL" shell settings get secure tv_user_setup_complete
adb -s "$SERIAL" shell cmd package resolve-activity --brief \
  -a android.intent.action.MAIN -c android.intent.category.HOME
adb -s "$SERIAL" shell pm list packages -u \
  com.google.android.tungsten.setupwraith
```

Require all three setup values to be `1`, Home to resolve to FLauncher, and
SetupWraith to remain known when uninstalled packages are included.

## 8. Cold-boot verification

Use Android's restart or power-off UI when available. Otherwise, unplug only
when no update or storage write is active, wait approximately ten seconds, and
restore power.

Verify boot to FLauncher, physical Home, voice input, Android TV Settings,
network reconnect, D-pad focus, representative audio/video playback, and
suspend/resume. Document dedicated app-button behavior separately; it is not a
release success criterion.
