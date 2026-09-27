# Troubleshooting

## ACT screen returns immediately

Disconnect Ethernet temporarily, open the exact Android TV Settings activity
through Remote-v1, and continue only through the stock settings UI. Do not
factory-reset merely to expose Developer Options.

## Build tapping does nothing

This firmware may already have the top-level developer switch enabled while
hiding navigation to the page. Open the exact DevelopmentActivity listed in
`discovery.md`; tapping Android version opens the Easter egg and is unrelated.

## ADB is unauthorized or offline

Keep the RSA prompt visible on the television and approve the displayed host.
Stop if the state does not become `device`. Do not delete device-side keys or
broaden network exposure as a retry.

## Launcher install is rejected

Verify the APK digest and exact firmware profile. Stop on rejection. Do not use
force flags, rename unrelated packages, or remove ACT services. Ordinary
third-party Home packages are rejected by this firmware; the released package
uses the tested firmware-compatible application identifier.

## Voice key opens a pairing screen

The remote may be bonded but not connected over Bluetooth, causing the IR
fallback key to open ACT's pairing screen. Re-pair or reconnect the original
Bluetooth remote through Android TV Settings, then test voice input again.

## Netflix, YouTube or Google Play keys do nothing

Dedicated app keys behaved differently between two otherwise matching units.
On the affected unit, the firmware consumed or redirected the keys before
FLauncher received them. Launcher-level remapping and an experimental patched
APK did not solve this reliably and are not part of the release.

Do not restore the subscription-gated ACT launcher merely to make these keys
appear active. Use FLauncher's application tiles. Treat a future accessibility
remapper as a separate, clearly experimental project.

## `com.skyworthdigital.producttest`

This is a privileged Skyworth factory-test utility, not the ACT activation
service. Leave it installed and do not invoke its unknown USB/update functions.

## ACT onboarding returns after reboot

Do not factory-reset. Reconnect ADB if it remains available and read the three
setup values and Home resolver. Stop for diagnosis instead of repeating all
writes blindly.
