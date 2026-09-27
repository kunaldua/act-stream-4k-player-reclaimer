# Building the FLauncher compatibility APK

`launcher/source/` is the complete corresponding source for
`FLauncher-0.18.0-actcorpcompat.1-armv7-release.apk`.

## Provenance

- upstream project: https://gitlab.com/flauncher/flauncher
- upstream release: 0.18.0, published 2023-04-21
- upstream source commit: `4930cd738a5ab32967953fe8b12790bc4b452872`
- license: GPL-3.0-or-later
- Flutter SDK: 3.7.5 / Dart 2.19.2
- Apple-silicon Flutter archive SHA-256:
  `aec66d79633dafa37d5fd00bcec366993921e802050728c5b2e0c3478fd2076f`

## Compatibility changes

- Application ID changed to `org.reclaimer.actcorpcompat.flauncher` because
  the tested firmware rejects ordinary third-party Home handlers.
- Visible name changed to `FLauncher (Reclaimer)`.
- Firebase Analytics, Crashlytics, and Remote Config removed.
- Unsplash integration disabled because it depended on Remote Config keys.
- Upstream Home and Leanback launcher intent filters retained.

The identifier change satisfies a local package-manager compatibility check on
owner-controlled hardware. It does not impersonate an ACT account or provide
access to ACT services.

## Reproducible inputs

Install Flutter 3.7.5, point `android/local.properties` at that SDK, and fetch
the dependency versions pinned by `pubspec.lock`:

```bash
cd launcher/source
flutter pub get
flutter analyze
flutter test
```

The Android release configuration reads these environment variables:

```text
SIGNING_KEYSTORE_PATH
SIGNING_KEYSTORE_PASSWORD
SIGNING_KEY_ALIAS
SIGNING_KEY_PASSWORD
```

Generate and retain your own signing identity, or use the project's offline
release identity if you are an authorized release maintainer. Never commit it.
Android updates must use the same certificate as the installed application.

Build the ARMv7 split:

```bash
flutter build apk --release --split-per-abi \
  --build-name 0.18.0-actcorpcompat.1 --build-number 18001
```

Inspect the resulting ARMv7 APK with Android build tools and confirm package,
SDK, ABI, permissions, signature, and digest before release. The reference
artifact is 9,323,403 bytes and has SHA-256:

```text
ed239a27be2ae3310c16bb21760aed96a8807b4c5881ccc8d4b8d151246eed9a
```

Its signing-certificate SHA-256 is:

```text
41aab1c2781e42e7616d0faad7f37ca4039cfa2bfff27c4fffc89773024ee127
```

The signing certificate fingerprint is public metadata. The corresponding
private key and passwords are not part of the source distribution.
