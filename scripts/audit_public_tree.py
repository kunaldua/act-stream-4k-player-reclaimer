#!/usr/bin/env python3
"""Fail when tracked files contain common private or non-redistributable data."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BANNED_SUFFIXES = {
    ".apk", ".aab", ".img", ".bin", ".p12", ".jks", ".keystore",
    ".pem", ".key", ".vdex", ".odex", ".oat", ".dex",
}
BANNED_NAMES = {
    "google-services.json",
    ".flauncher-actcorpcompat-signing-password",
    "adbkey",
}
TEXT_PATTERNS = {
    "private workspace path": re.compile(r"/Users/kunal(?:/|\b)"),
    "observed private LAN address": re.compile(r"\b10\.0\.1\.\d{1,3}\b"),
    "private key block": re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY"),
    "observed pairing code": re.compile(r"\b(?:B501|4ADD)\b"),
}


def tracked_files() -> list[Path]:
    process = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        capture_output=True,
        check=False,
    )
    if process.returncode != 0:
        raise RuntimeError("run this audit inside an initialized Git repository")
    return [ROOT / item.decode() for item in process.stdout.split(b"\0") if item]


def main() -> int:
    failures: list[str] = []
    for path in tracked_files():
        relative = path.relative_to(ROOT)
        # This file necessarily contains the signatures it is designed to
        # detect. Its own content is reviewed as code rather than input data.
        if relative == Path("scripts/audit_public_tree.py"):
            continue
        lowered = path.name.lower()
        if path.suffix.lower() in BANNED_SUFFIXES or lowered in BANNED_NAMES:
            failures.append(f"banned tracked artifact: {relative}")
            continue
        try:
            raw = path.read_bytes()
        except OSError as error:
            failures.append(f"unable to inspect {relative}: {error}")
            continue
        if b"\x00" in raw[:8192]:
            continue
        text = raw.decode("utf-8", errors="replace")
        for label, pattern in TEXT_PATTERNS.items():
            if pattern.search(text):
                failures.append(f"{label}: {relative}")

    if failures:
        print("Public-tree audit failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(f"Public-tree audit passed for {len(tracked_files())} tracked files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
