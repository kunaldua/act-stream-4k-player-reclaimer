# Release procedure

This procedure deliberately keeps Android signing credentials off GitHub and
out of GitHub Actions.

1. Confirm the working tree contains only reviewed source and documentation.
2. Run `scripts/validate_package.py`, the unit tests, the bundled OpenAI plugin
   and skill validators, and `scripts/audit_public_tree.py`.
3. Build the launcher from the tagged corresponding source or select the
   already verified reference artifact.
4. Verify the APK hash, size, package metadata, ABI, SDK levels, signature, and
   signing-certificate fingerprint locally.
5. Confirm `checksums/SHA256SUMS` matches the exact release asset.
6. Tag the reviewed commit as `v0.1.0-experimental`.
7. Create a GitHub Release from that tag and attach the APK and checksum file.
8. State the exact supported fingerprint, two-unit test count, known app-key
   limitation, Android 9 security limitation, and rollback procedure.
9. Download the published asset once and verify its digest independently.

Do not upload the keystore, password file, Remote-v1 certificate/key pair, raw
device probes, extracted OEM components, or experimental APKs. Do not sign in
CI unless the project later adopts a separately reviewed secret-management and
key-rotation design.
