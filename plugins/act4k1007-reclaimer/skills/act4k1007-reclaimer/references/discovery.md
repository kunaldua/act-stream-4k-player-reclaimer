# Discovery and exact-match gate

Use this procedure for every box, including another unit with the same case
label. Everything here is read-only.

## Before ADB

1. Confirm the printed model and that the user owns or may modify the box.
2. Connect HDMI, stable power, and Ethernet to the same LAN as the Mac.
3. Find the box's current IP address in the router.
4. Check TCP ports 6466 and 6467 for the legacy Android TV Remote service.
5. Pair with `atvremote` Remote-v1 and keep its certificate and private key in
   a private directory outside the repository.

Open these exact activities only:

```text
com.android.tv.settings/.MainSettings
com.android.tv.settings/.system.development.DevelopmentActivity
```

If either activity is unavailable, stop rather than guessing another
component. The user must turn on USB debugging and approve the Mac's ADB key on
the television. On the tested firmware, the setting also exposes ADB on TCP
5555; a USB data port is not required.

## ADB verification

Require the user to identify the exact ADB serial when more than one device is
listed. Run:

```bash
python3 scripts/host_check.py
python3 scripts/verify_device.py --serial 192.0.2.10:5555
```

The verifier requires all of these values:

```text
ro.product.model=ACT4K1007
ro.product.manufacturer=SkyworthDigital
ro.product.brand=ACT
ro.product.device=IPBox
ro.product.board=bigfish
ro.hardware=bigfish
ro.build.version.release=9
ro.build.version.sdk=28
ro.product.cpu.abilist=armeabi-v7a,armeabi
ro.stb.chip=HI3798MV200
ro.build.fingerprint=ACT/IPBox/IPBox:9/PPR1.180610.011/C2.3.7_20210525:user/release-keys
```

It also requires `device_provisioned=1`. A mismatch means the published
recovery path is unsupported, even if the launcher might appear compatible.

For a shareable, allowlisted diagnostic record, use:

```bash
python3 scripts/support_report.py --serial 192.0.2.10:5555 --output support-report.json
```

Review that file manually before attaching it to an issue.
