# Known issues

## Dedicated app buttons

Netflix, YouTube, and Google Play buttons worked on one tested unit but not the
other, despite matching public identity properties. On the affected unit, the
firmware appeared to consume or redirect these events before FLauncher could
receive them. Experimental launcher patching did not fix the behavior and is
not included.

Use application tiles inside FLauncher. Dedicated app-button functionality is
not part of the v0.1 success criteria.

## Voice button opens ACT pairing

If the remote is bonded but disconnected over Bluetooth, the voice key can
fall back to an infrared code that launches ACT's pairing screen. Reconnect or
re-pair the original Bluetooth remote in Android TV Settings. Voice search
worked after proper Bluetooth pairing on both tested units.

## Android 9 security

Replacing the launcher does not update Android, the 2021 security patch, DRM
components, codecs, or vendor firmware. Avoid sensitive accounts and consider
placing the box on an isolated or restricted network. Use a currently
supported device for services that require modern security assurances.

## Unsupported firmware

The same enclosure or `DV8919` name may contain different board, storage, or
firmware variants. Any fingerprint mismatch is unsupported. Open a sanitized
research issue rather than bypassing the verifier.
