#!/usr/bin/env python3
"""Shared read-only helpers for the ACT4K1007 compatibility gate."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any


SERIAL_RE = re.compile(r"^[A-Za-z0-9._:-]+$")
PROFILE_PATH = (
    Path(__file__).resolve().parent.parent
    / "references"
    / "act4k1007-c2.3.7.json"
)


class DeviceReadError(RuntimeError):
    """Raised when a read-only ADB query cannot be completed safely."""


def load_profile() -> dict[str, Any]:
    return json.loads(PROFILE_PATH.read_text(encoding="utf-8"))


def run(args: list[str], timeout: int = 10) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError as error:
        raise DeviceReadError(f"required executable not found: {args[0]}") from error
    except subprocess.TimeoutExpired as error:
        raise DeviceReadError(f"read-only command timed out: {args[0]}") from error


def require_transport(serial: str) -> None:
    if not SERIAL_RE.fullmatch(serial):
        raise DeviceReadError("ADB serial contains unsupported characters")
    process = run(["adb", "devices", "-l"])
    if process.returncode != 0:
        raise DeviceReadError(process.stderr.strip() or "ADB enumeration failed")
    matches = []
    for line in process.stdout.splitlines()[1:]:
        fields = line.split()
        if fields and fields[0] == serial:
            matches.append(fields)
    if len(matches) != 1:
        raise DeviceReadError("exactly one matching ADB transport is required")
    state = matches[0][1] if len(matches[0]) > 1 else "unknown"
    if state != "device":
        raise DeviceReadError(f"ADB transport state is {state}; expected device")


def adb_shell(serial: str, *args: str) -> str:
    process = run(["adb", "-s", serial, "shell", *args])
    if process.returncode != 0:
        message = process.stderr.strip() or process.stdout.strip() or "ADB read failed"
        raise DeviceReadError(message)
    return process.stdout.strip()


def collect_allowlisted(serial: str) -> dict[str, Any]:
    profile = load_profile()
    require_transport(serial)
    properties = {
        key: adb_shell(serial, "getprop", key)
        for key in profile["required_properties"]
    }
    settings = {
        "global.device_provisioned": adb_shell(
            serial, "settings", "get", "global", "device_provisioned"
        ),
        "secure.user_setup_complete": adb_shell(
            serial, "settings", "get", "secure", "user_setup_complete"
        ),
        "secure.tv_user_setup_complete": adb_shell(
            serial, "settings", "get", "secure", "tv_user_setup_complete"
        ),
    }
    return {"properties": properties, "settings": settings}


def load_fixture(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data.get("properties"), dict) or not isinstance(
        data.get("settings"), dict
    ):
        raise DeviceReadError("fixture must contain properties and settings objects")
    return data


def evaluate(data: dict[str, Any]) -> dict[str, Any]:
    profile = load_profile()
    expected_properties = profile["required_properties"]
    expected_state = profile["required_initial_state"]
    actual_properties = data.get("properties", {})
    actual_settings = data.get("settings", {})

    mismatches = []
    for key, expected in expected_properties.items():
        actual = actual_properties.get(key)
        if actual != expected:
            mismatches.append({"field": key, "expected": expected, "actual": actual})
    for key, expected in expected_state.items():
        actual = actual_settings.get(key)
        if actual != expected:
            mismatches.append({"field": key, "expected": expected, "actual": actual})

    return {
        "profile_id": profile["id"],
        "compatible": not mismatches,
        "mismatches": mismatches,
        "properties": actual_properties,
        "settings": actual_settings,
    }
