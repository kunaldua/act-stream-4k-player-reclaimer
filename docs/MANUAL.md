# ACT4K1007 recovery manual

This manual reproduces the launcher-first recovery tested on two
ACT4K1007/SkyworthDigital DV8919 boxes. It makes the owner-controlled Android
hardware useful without rooting or flashing it. It does not restore ACT's
service or bypass an ACT account.

## Prerequisites

- A Mac on the same network as the box
- HDMI display, stable power, Ethernet, and the original remote
- Android Platform Tools (`adb`)
- `atvremote` v0.1.3 for Darwin arm64, obtained from its upstream GitHub
  release and verified against `checksums/SHA256SUMS`
- The FLauncher compatibility APK from this project's matching GitHub Release
- A private directory outside the repository for Remote-v1 pairing keys

Do not continue if losing the current configuration is unacceptable. Although
this workflow is designed not to erase personal media, device changes always
carry some risk.

Use example address `192.0.2.10` below only as a placeholder. Substitute the
address assigned to your box.

## 1. Pair before ADB is available

Put the box and Mac on the same LAN. Locate the box in your router, then create
a private credential directory:

```bash
BOX_IP='192.0.2.10'
CREDENTIAL_DIR="$HOME/.act4k1007-private/box-1"
mkdir -p "$CREDENTIAL_DIR"
```

Pair with the legacy Remote-v1 protocol:

```bash
atvremote -ip "$BOX_IP" -version=1 -pair \
  -cert "$CREDENTIAL_DIR/cert.pem" \
  -key "$CREDENTIAL_DIR/key.pem"
```

Enter the four-character hexadecimal code shown on the television. These keys
control the paired box; never commit or post them.

Open the real Android TV Settings activity:

```bash
atvremote -ip "$BOX_IP" -version=1 \
  -cert "$CREDENTIAL_DIR/cert.pem" \
  -key "$CREDENTIAL_DIR/key.pem" \
  -open 'com.android.tv.settings/.MainSettings'
```

If Developer Options is hidden from navigation, open its exact activity:

```bash
atvremote -ip "$BOX_IP" -version=1 \
  -cert "$CREDENTIAL_DIR/cert.pem" \
  -key "$CREDENTIAL_DIR/key.pem" \
  -open 'com.android.tv.settings/.system.development.DevelopmentActivity'
```

Stop if either activity is unavailable. Do not guess alternate component
names.

## 2. Enable and authorize ADB

On the television, leave **Enable developer options** on and enable **USB
debugging**. On the tested firmware, this also exposes ADB on network port
5555 even though the box has only USB-A host ports.

```bash
SERIAL="$BOX_IP:5555"
adb connect "$SERIAL"
adb devices -l
```

Approve the Mac's RSA fingerprint on the television. Continue only when the
exact target is listed once in state `device`. Stop on `unauthorized`,
`offline`, or multiple ambiguous targets.

## 3. Pass the exact identity gate

From the installed skill directory, run:

```bash
python3 scripts/host_check.py
python3 scripts/verify_device.py --serial "$SERIAL"
```

The second command must report `compatible: true`. It compares the complete
fingerprint and the other allowlisted properties; a model-name match alone is
not enough. It permits only this launcher recovery—not root or flashing.

## 4. Verify the launcher APK

```bash
APK='/absolute/path/FLauncher-0.18.0-actcorpcompat.1-armv7-release.apk'
python3 scripts/verify_release.py "$APK"
```

Required SHA-256:

```text
ed239a27be2ae3310c16bb21760aed96a8807b4c5881ccc8d4b8d151246eed9a
```

Stop on any mismatch.

## 5. Install and test FLauncher

This changes the device by installing a new application. It should not erase
personal media. If installation fails, stop rather than adding force flags.

```bash
adb -s "$SERIAL" install "$APK"
adb -s "$SERIAL" shell am start -n \
  org.reclaimer.actcorpcompat.flauncher/me.efesser.flauncher.MainActivity
```

Before continuing, verify visible focus, D-pad navigation, app launching, and
a working path to Android TV Settings.

Immediate rollback:

```bash
adb -s "$SERIAL" uninstall org.reclaimer.actcorpcompat.flauncher
```

## 6. Complete Android's two setup gates

Each `settings put` changes per-user Android state without erasing media. Apply
and verify the first value:

```bash
adb -s "$SERIAL" shell settings put secure user_setup_complete 1
adb -s "$SERIAL" shell settings get secure user_setup_complete
```

Expected output: `1`. Rollback uses the original tested value `0`.

Apply and verify the television-specific value:

```bash
adb -s "$SERIAL" shell settings put secure tv_user_setup_complete 1
adb -s "$SERIAL" shell settings get secure tv_user_setup_complete
```

Expected output: `1`. Rollback deletes the value because it was originally
unset on the two tested boxes.

## 7. Select FLauncher as Home

```bash
adb -s "$SERIAL" shell cmd package set-home-activity --user 0 \
  org.reclaimer.actcorpcompat.flauncher/me.efesser.flauncher.MainActivity
adb -s "$SERIAL" shell dumpsys package preferred-activities
```

Expected result from the first command: `Success`. SetupWraith may still win
Home resolution because its system intent filter has higher priority.

## 8. Remove SetupWraith only for user 0

This is the narrowest tested change that removes the dead setup flow. The APK
remains on the system partition and `-k` keeps its data. It also removes Google
deferred setup and its bundled OTA helper for user 0 until restored.

```bash
adb -s "$SERIAL" shell pm uninstall -k --user 0 \
  com.google.android.tungsten.setupwraith
```

Expected result: `Success`. Stop if rejected; do not remove ACT packages.

Rollback:

```bash
adb -s "$SERIAL" shell cmd package install-existing --user 0 \
  com.google.android.tungsten.setupwraith
```

## 9. Verify before reboot

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

Use Android's restart UI when available. Otherwise unplug only while no update
or storage write is active, wait around ten seconds, and restore power. Verify
boot to FLauncher, Home, voice input, Settings, networking, D-pad input,
representative audio/video, and suspend/resume.

See [ROLLBACK.md](ROLLBACK.md) before reversing the changes and
[KNOWN-ISSUES.md](KNOWN-ISSUES.md) for remote-button differences.
