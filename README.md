# ACT Stream 4K Player Reclaimer

Reclaim a user-owned ACT Stream 4K / ACT4K1007 (SkyworthDigital DV8919) that is trapped behind ACT's retired sign-in experience, and make it boot into a usable Android TV launcher again.

This project packages the exact recovery path verified on two matching boxes. It can be used as a guided Codex plugin or as a manual runbook. It does **not** guess at firmware, defeat an account password, root the box, or flash a ROM.

## What owners see before recovery

After a factory reset, the box completes Android TV onboarding and then opens an ACT-branded welcome or sign-in screen. Because the associated ACT service is no longer usable, a legitimate owner can be left with hardware that boots but cannot reach a useful home screen.

The usual escape routes do not work reliably:

- pressing Home may reveal Android TV briefly, but the ACT screen takes over again;
- disconnecting Ethernet may provide a temporary route into Settings, but does not remove the ACT setup flow;
- tapping **Build** seven times may do nothing on this customized firmware;
- tapping **Android version** opens the Android Easter egg, not Developer options;
- the USB-A sockets are host ports for accessories and storage, not a normal USB data connection to a Mac;
- ordinary launcher APKs, including Projectivy in our testing, may be rejected by the customized package manager.

Those constraints are why the recovery is a sequence rather than a single APK install.

## Why each recovery step is needed

| Problem encountered | Why the next step is necessary | What the tested recovery does |
| --- | --- | --- |
| The ACT screen keeps returning and normal Settings navigation is unreliable. | We need a route into the real Android TV settings app without depending on ACT's launcher. | Uses the legacy Android TV Remote v1 protocol over the local network to open `com.android.tv.settings/.MainSettings`. |
| This firmware ignores the normal seven-taps-on-Build gesture. | Developer options must be opened directly before ADB can be enabled. | Opens `com.android.tv.settings/.system.development.DevelopmentActivity`. The owner turns on **USB debugging** on the TV. |
| The box has only USB-A host ports. | A USB cable to the Mac is not an ADB transport for this hardware. | Uses network ADB on TCP port 5555 after USB debugging is enabled. |
| Different products can share the same enclosure and model label. | Applying box-specific changes to a near-match could break it. | Requires the exact tested build fingerprint before any mutation. |
| The OEM package manager rejects normally named third-party launchers. | A compatible launcher package identity is required for installation on this firmware. | Installs a reproducibly derived FLauncher 0.18.0 build as `org.reclaimer.actcorpcompat.flauncher`, shown as **FLauncher (Reclaimer)**. The identifier contains the compatibility token accepted by the device's local allowlist; it does not contact or impersonate the ACT service. |
| Installing a launcher alone does not stop setup components from retaking Home. | Android must be told that setup is complete and which Home activity to prefer. | Sets `user_setup_complete` and `tv_user_setup_complete`, then selects FLauncher as Home. |
| `SetupWraith` can still win the Home intent because it has priority 4. | The remaining per-user setup package has to be removed from the active user. | Runs a reversible user-0 uninstall. The system APK stays on the system partition and can be restored. |
| Remote behavior may differ even between nominally identical boxes. | Button behavior must be checked instead of assumed. | Verifies Home, re-pairs the Bluetooth remote when needed for voice search, and records that branded app buttons are firmware-dependent. |

## How to use this project

Choose one of these routes.

### Option A: guided by Codex (recommended)

The plugin explains each action, starts with read-only inspection, pauses for actions that must be performed on the TV, and asks before every device mutation.

1. Add this repository as a Codex plugin marketplace:

   ```sh
   codex plugin marketplace add kunaldua/act-stream-4k-player-reclaimer --ref main
   ```

2. Restart Codex if the new marketplace does not appear immediately.
3. Open the **Plugins Directory**, select the **ACT4K1007 Reclaimer** marketplace, and install the plugin.
4. Start a new chat and say:

   ```text
   Use $act4k1007-reclaimer to help me reclaim my ACT4K1007.
   ```

5. Follow the prompts. Keep the box visible on a TV and have its original remote available.

This repository is a public Codex marketplace, so anyone can add it with the command above. See OpenAI's [Codex plugin documentation](https://developers.openai.com/plugins/build/plugins) for marketplace management.

Codex does not silently unlock the device. It walks the owner through discovery, remote pairing, Settings access, identity checks, approved changes, reboot verification, and rollback if needed. Pairing codes and IP addresses are session inputs and must never be committed to this repository.

### Option B: follow the manual runbook

Use [docs/MANUAL.md](docs/MANUAL.md) if you prefer to run the commands yourself. You will need:

- an Apple-silicon Mac on the same trusted LAN as the box (the published Remote-v1 helper is the tested Darwin arm64 build);
- Ethernet connected to the box for the initial remote-control and ADB stages;
- the original remote, a display, and optionally a USB keyboard and mouse;
- Android platform-tools (`adb`);
- `atvremote` 0.1.3 for the legacy Remote v1 pairing flow;
- the verified **FLauncher (Reclaimer)** APK from this project's matching release.

Download the APK only from this project's matching GitHub Release and verify it against [`checksums/SHA256SUMS`](checksums/SHA256SUMS). Do not substitute an APK from a file-sharing site or rebuild one and assume it is equivalent.

## What happens in a guided recovery

1. **Put the box and computer on the same network.** The legacy remote protocol is the only tested route to the hidden Settings activities before ADB is available.
2. **Pair the temporary network remote.** The TV displays a four-character code. Enter it only into the local pairing prompt; do not post it in an issue or log.
3. **Open Android TV Settings and Developer options directly.** This avoids the ACT takeover and the disabled Build-number gesture.
4. **Turn on USB debugging on the TV.** Despite the label, this enables the tested network ADB connection on this box.
5. **Connect with ADB and approve the computer on the TV.** Codex collects read-only identity, package, launcher, setup-state, and disk-space information.
6. **Verify the exact fingerprint.** A mismatch stops the procedure. Similar-looking hardware is not accepted.
7. **Back up diagnostic state.** The workflow records text metadata and package state, not personal media or credentials.
8. **Install the verified launcher.** The APK checksum and package identity are checked before installation.
9. **Complete Android TV setup state and select Home.** These changes prevent the obsolete setup flow from reclaiming the screen.
10. **Disable SetupWraith for user 0.** This is the final reversible step needed on the tested firmware for Home to remain stable.
11. **Reboot and test.** Confirm that FLauncher starts automatically, Home returns to it, voice works after Bluetooth pairing, and the box remains usable after a full power cycle.

The plugin requests confirmation before steps 8–10. It shows the commands and explains their effect before running them.

## Tested scope

Verified on two ACT Stream 4K / ACT4K1007 boxes reporting:

- model: `ACT4K1007`;
- manufacturer: `SkyworthDigital`;
- Android: `9` / SDK `28`;
- CPU ABI: `armeabi-v7a`;
- board and hardware: `bigfish`;
- SoC property: `HI3798MV200`;
- build fingerprint: `ACT/IPBox/IPBox:9/PPR1.180610.011/C2.3.7_20210525:user/release-keys`.

The successful end state is FLauncher as the persistent Home app, with Home and voice input working after reboot. Netflix, Google Play, and YouTube shortcut buttons varied between the two boxes and are not part of the success criteria.

If the fingerprint differs, stop. Open an issue with redacted diagnostic output so support for that build can be researched separately.

## Safety boundaries

This project is for hardware you own or are explicitly authorized to service. It will not:

- bypass ACT credentials, subscriptions, paid services, DRM, or account locks;
- root the device or weaken Android security controls;
- flash bootloaders, recovery images, or unverified firmware;
- treat a similar model name as proof of hardware compatibility;
- publish pairing codes, local IP addresses, ADB keys, signing keys, or private device dumps.

The launcher change is reversible. `SetupWraith` can be restored for user 0 with:

```sh
adb shell cmd package install-existing --user 0 com.google.android.tungsten.setupwraith
```

See [docs/ROLLBACK.md](docs/ROLLBACK.md) for the complete rollback procedure.

## Project map

- [docs/MANUAL.md](docs/MANUAL.md) — command-by-command recovery runbook
- [docs/KNOWN-ISSUES.md](docs/KNOWN-ISSUES.md) — pairing, launcher, voice, and shortcut-button limitations
- [docs/ROLLBACK.md](docs/ROLLBACK.md) — restore the original per-user state
- [SECURITY.md](SECURITY.md) — diagnostic-report and disclosure policy
- [launcher/BUILD.md](launcher/BUILD.md) — launcher source, changes, and reproducibility
- [plugins/act4k1007-reclaimer/skills/act4k1007-reclaimer/SKILL.md](plugins/act4k1007-reclaimer/skills/act4k1007-reclaimer/SKILL.md) — guided Codex workflow

## Privacy and release hygiene

The repository intentionally contains no APK, firmware dump, credentials, signing material, pairing code, private LAN address, or personal filesystem path. Before publishing a change, run:

```sh
python3 scripts/audit_public_tree.py
```

Maintainers should also inspect the entire Git history before making a private repository public; deleting a secret from the latest commit does not remove it from older commits.

## Development

Run package validation, the standard-library unit tests, and the public-tree audit before committing:

```sh
python3 scripts/validate_package.py
python3 -m unittest discover -s tests -v
python3 scripts/audit_public_tree.py
```

The launcher is based on FLauncher 0.18.0. Firebase Analytics, Crashlytics, Remote Config, and the Unsplash integration were removed from the verified build. See [launcher/BUILD.md](launcher/BUILD.md) before reproducing it.

## Licensing

The plugin, original scripts, and original documentation are available under the MIT License. `launcher/source/` is a modified FLauncher work licensed under GPL-3.0-or-later; see its own `LICENSE` and [launcher/BUILD.md](launcher/BUILD.md).

ACT, SkyworthDigital, Android, Google, and FLauncher are names of their respective owners. This is an independent interoperability project.
