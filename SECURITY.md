# Security and privacy

## Supported recovery path

Version 0.1 supports only the exact ACT4K1007 firmware fingerprint listed in
the README. Do not loosen the identity checks to accommodate a similar-looking
box. Product names, chipsets, and enclosure labels are not sufficient evidence
for a safe device-changing workflow.

The published path is launcher-first. It does not root, unlock, repartition,
format, disable verified boot, flash an image, bypass Factory Reset Protection,
or grant access to ACT accounts or paid services.

## Keep these files private

Never attach or commit:

- Android serials, Android IDs, MAC addresses, account names or home paths;
- ADB private keys or Android TV Remote certificates and keys;
- signing keystores, aliases or passwords;
- raw device probes without manual review;
- extracted firmware, OEM system APKs, framework JARs, VDEX/ODEX files;
- APKs from unrelated third parties.

Use `support_report.py` to create a deliberately small, allowlisted report for
an issue. Review the result before posting it.

## Reporting a security problem

Until a dedicated security contact is published, open a GitHub Security
Advisory rather than a public issue. Do not include live credentials or signing
material even in a private report; describe the affected file or behavior.
