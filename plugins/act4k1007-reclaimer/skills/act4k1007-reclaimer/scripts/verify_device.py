#!/usr/bin/env python3
"""Apply the exact ACT4K1007 compatibility gate using read-only queries."""

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
    args = parser.parse_args()
    try:
        data = collect_allowlisted(args.serial) if args.serial else load_fixture(args.fixture)
        result = evaluate(data)
    except (DeviceReadError, OSError, json.JSONDecodeError) as error:
        print(f"verification error: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    if not result["compatible"]:
        print("STOP: this device does not match the published recovery profile.", file=sys.stderr)
        return 3
    print("Exact profile match. This permits the documented launcher workflow only.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
