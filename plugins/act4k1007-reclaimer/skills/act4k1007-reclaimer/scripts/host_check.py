#!/usr/bin/env python3
"""Report ACT4K1007 host prerequisites without changing host or device state."""

from __future__ import annotations

import json
import platform
import shutil
import subprocess


TOOLS = {
    "adb": ["version"],
    "python3": ["--version"],
    "openssl": ["version"],
    "shasum": ["-a", "256", "/dev/null"],
    "atvremote": ["-h"],
}


def inspect(name: str, args: list[str]) -> dict[str, object]:
    path = shutil.which(name)
    result: dict[str, object] = {"available": bool(path), "path": path}
    if not path:
        return result
    try:
        process = subprocess.run(
            [path, *args], capture_output=True, text=True, timeout=5, check=False
        )
        lines = (process.stdout or process.stderr).strip().splitlines()
        result["version"] = lines[0][:240] if lines else "available"
    except (OSError, subprocess.TimeoutExpired) as error:
        result["version"] = f"unable to query: {error}"
    return result


def main() -> int:
    tools = {name: inspect(name, args) for name, args in TOOLS.items()}
    report = {
        "host": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "tools": tools,
        "ready_for_adb_stage": bool(tools["adb"]["available"]),
        "notes": [
            "atvremote is required only before ADB is enabled.",
            "This check installs nothing and does not contact a device.",
        ],
    }
    print(json.dumps(report, indent=2))
    return 0 if tools["adb"]["available"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
