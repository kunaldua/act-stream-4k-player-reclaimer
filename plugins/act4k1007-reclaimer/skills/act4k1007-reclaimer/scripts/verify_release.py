#!/usr/bin/env python3
"""Verify the published FLauncher compatibility APK by SHA-256."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


EXPECTED_SHA256 = "ed239a27be2ae3310c16bb21760aed96a8807b4c5881ccc8d4b8d151246eed9a"
EXPECTED_SIZE = 9_323_403


def digest(path: Path) -> tuple[str, int]:
    hasher = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
            size += len(chunk)
    return hasher.hexdigest(), size


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("apk", type=Path)
    args = parser.parse_args()
    try:
        actual_hash, actual_size = digest(args.apk)
    except OSError as error:
        parser.error(str(error))
    print(f"file: {args.apk.name}")
    print(f"size: {actual_size}")
    print(f"sha256: {actual_hash}")
    if actual_hash != EXPECTED_SHA256 or actual_size != EXPECTED_SIZE:
        print("MISMATCH: do not install this file.")
        return 1
    print("Verified release artifact.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
