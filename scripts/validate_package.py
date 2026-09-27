#!/usr/bin/env python3
"""Validate the repository's portable plugin, compatibility manifest, and marketplace."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_NAME = "act4k1007-reclaimer"
PLUGIN_ROOT = ROOT / "plugins" / PLUGIN_NAME
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?$")
SHA256_LINE = re.compile(r"^[0-9a-f]{64}  [^/]+$")


def load_object(path: Path, failures: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        failures.append(f"cannot read valid JSON from {path.relative_to(ROOT)}: {error}")
        return {}
    if not isinstance(value, dict):
        failures.append(f"{path.relative_to(ROOT)} must contain a JSON object")
        return {}
    return value


def validate_manifest(path: Path, *, portable: bool, failures: list[str]) -> dict:
    manifest = load_object(path, failures)
    if manifest.get("name") != PLUGIN_NAME:
        failures.append(f"{path.relative_to(ROOT)} has the wrong plugin name")
    version = manifest.get("version")
    if not isinstance(version, str) or SEMVER.fullmatch(version) is None:
        failures.append(f"{path.relative_to(ROOT)} has an invalid semantic version")
    if not isinstance(manifest.get("description"), str) or not manifest["description"].strip():
        failures.append(f"{path.relative_to(ROOT)} needs a description")
    if manifest.get("license") != "MIT":
        failures.append(f"{path.relative_to(ROOT)} must declare the repository MIT license")
    if "[TODO:" in path.read_text(encoding="utf-8"):
        failures.append(f"{path.relative_to(ROOT)} contains an unfinished TODO")
    if portable:
        if manifest.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
            failures.append("portable plugin.json has the wrong schema")
        interface = manifest.get("extensions", {}).get("com.openai", {}).get("interface", {})
    else:
        if manifest.get("skills") != "./skills/":
            failures.append("compatibility manifest must point at ./skills/")
        interface = manifest.get("interface", {})
    for key in ("displayName", "shortDescription", "longDescription", "developerName", "category", "defaultPrompt"):
        if not interface.get(key):
            failures.append(f"{path.relative_to(ROOT)} is missing interface.{key}")
    return manifest


def validate_skill(failures: list[str]) -> None:
    skill = PLUGIN_ROOT / "skills" / PLUGIN_NAME / "SKILL.md"
    text = skill.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if match is None:
        failures.append("skill is missing YAML frontmatter")
        return
    frontmatter = match.group(1)
    name = re.search(r"^name:\s*(.+?)\s*$", frontmatter, re.MULTILINE)
    description = re.search(r"^description:\s*(.+?)\s*$", frontmatter, re.MULTILINE)
    if name is None or name.group(1) != PLUGIN_NAME:
        failures.append("skill frontmatter has the wrong name")
    if description is None or not description.group(1).strip():
        failures.append("skill frontmatter needs a description")
    if "[TODO:" in text:
        failures.append("skill contains an unfinished TODO")


def validate_marketplace(failures: list[str]) -> None:
    marketplace = load_object(ROOT / ".agents" / "plugins" / "marketplace.json", failures)
    if marketplace.get("name") != PLUGIN_NAME:
        failures.append("marketplace has the wrong name")
    entries = marketplace.get("plugins")
    if not isinstance(entries, list) or len(entries) != 1:
        failures.append("marketplace must contain exactly one plugin")
        return
    entry = entries[0]
    if entry.get("name") != PLUGIN_NAME:
        failures.append("marketplace entry has the wrong plugin name")
    if entry.get("source") != {"source": "local", "path": f"./plugins/{PLUGIN_NAME}"}:
        failures.append("marketplace source must point at the bundled plugin")
    if entry.get("policy") != {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}:
        failures.append("marketplace policy is incomplete")


def validate_checksums(failures: list[str]) -> None:
    lines = (ROOT / "checksums" / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    if not lines or any(SHA256_LINE.fullmatch(line) is None for line in lines):
        failures.append("checksums/SHA256SUMS is malformed")
    names = {line.split("  ", 1)[1] for line in lines if "  " in line}
    expected = {
        "FLauncher-0.18.0-actcorpcompat.1-armv7-release.apk",
        "Darwin-arm64-atvremote.tar.gz",
    }
    if names != expected:
        failures.append("checksums/SHA256SUMS does not list the two documented artifacts")


def main() -> int:
    failures: list[str] = []
    portable = validate_manifest(PLUGIN_ROOT / "plugin.json", portable=True, failures=failures)
    compatibility = validate_manifest(
        PLUGIN_ROOT / ".codex-plugin" / "plugin.json", portable=False, failures=failures
    )
    if portable.get("version") != compatibility.get("version"):
        failures.append("portable and compatibility manifests have different versions")
    validate_skill(failures)
    validate_marketplace(failures)
    validate_checksums(failures)
    if failures:
        print("Package validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print("Package validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
