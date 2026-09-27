#!/usr/bin/env python3
"""Create an allowlisted ACT4K1007 support report with no device identifier."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from device_profile import DeviceReadError, collect_allowlisted, evaluate, load_fixture


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--serial", help="Exact serial from `adb devices -l`")
    source.add_argument("--fixture", type=Path, help="Sanitized JSON fixture for tests")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        data = collect_allowlisted(args.serial) if args.serial else load_fixture(args.fixture)
        result = evaluate(data)
        report = {
            "schema_version": 1,
            "profile_id": result["profile_id"],
            "compatible": result["compatible"],
            "mismatches": result["mismatches"],
            "properties": result["properties"],
            "setup_state": result["settings"],
            "privacy": "Allowlisted report; review manually before publication.",
        }
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    except (DeviceReadError, OSError, json.JSONDecodeError) as error:
        print(f"report error: {error}", file=sys.stderr)
        return 2
    print(f"Wrote allowlisted report to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
