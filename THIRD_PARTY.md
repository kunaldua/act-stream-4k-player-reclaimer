# Third-party provenance

## atvremote

- Project: `drosoCode/atvremote`
- Source: https://github.com/drosoCode/atvremote
- Tested release: `v0.1.3`, Darwin arm64
- Source commit inspected: `967d9ff8e74cae4b5cb149696f7a05ceb0a128c4`
- Release archive SHA-256:
  `6d6144757a695a3a6154885d4e77c6ff54b14ebf5ccc8e8cdd54853d078ba17d`
- License: MIT

The binary is not vendored. Obtain it from its upstream release and verify the
archive before extraction. Remote-v1 with a four-character hexadecimal code
worked on both tested boxes; the Remote-v2 path did not.

## FLauncher

- Project: https://gitlab.com/flauncher/flauncher
- Upstream version: `0.18.0`
- Upstream source commit: `4930cd738a5ab32967953fe8b12790bc4b452872`
- License: GPL-3.0-or-later

The complete modified source used for the compatibility APK is retained under
`launcher/source/`, with build and provenance details in `launcher/BUILD.md`.
