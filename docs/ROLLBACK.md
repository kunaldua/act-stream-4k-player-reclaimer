# Rollback guide

Do not uninstall the current Home application until another known Home handler
is available. Keep ADB connected throughout rollback and verify after every
command.

Set your exact connected target:

```bash
SERIAL='192.0.2.10:5555'
```

Restore SetupWraith for user 0:

```bash
adb -s "$SERIAL" shell cmd package install-existing --user 0 \
  com.google.android.tungsten.setupwraith
```

Restore the two setup values to their state observed on the tested boxes:

```bash
adb -s "$SERIAL" shell settings put secure user_setup_complete 0
adb -s "$SERIAL" shell settings delete secure tv_user_setup_complete
```

Those values are correct only if they match the state captured before recovery
on your unit.

Once another Home activity resolves, remove FLauncher:

```bash
adb -s "$SERIAL" uninstall org.reclaimer.actcorpcompat.flauncher
```

Uninstalling FLauncher removes its preferences but not personal media. If no
Home activity resolves, launch Android TV Settings through Remote-v1 or ADB and
do not reboot until a known Home handler is restored.
