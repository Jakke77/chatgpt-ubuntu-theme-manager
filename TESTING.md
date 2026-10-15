# Building and checking a release

The released application was tested on Ubuntu 26.10 / GNOME 51. The checks
below do not establish support for other Ubuntu or GNOME versions.

Build dependencies on Ubuntu:

```bash
sudo apt install python3 dpkg libgtk-3-bin desktop-file-utils
python3 build.py
```

The result is `dist/chatgpt-ubuntu-theme-manager_1.2.1_all.deb`.
Generated data in `package/` is ignored by Git. Building does not apply a
theme or modify the active desktop.

Runtime and integration checks also need the dependencies listed in the
`.deb` control metadata: PyGObject, GTK 4 >= 4.18, libadwaita >= 1.6, Ubuntu
Yaru GTK/Shell/icon packages, GNOME Shell extensions and the dconf backend.
GTK 3 GI bindings and the GNOME Shell/Mutter 51 introspection libraries are
used by the native style parser checks. Run the checks in this order:

```bash
python3 build.py
python3 tests/theme_packs_test.py
python3 tests/content_policy_test.py
python3 tests/integration.py
python3 tests/release_checks.py
```

`release_checks.py` uses the private generated fixture from `integration.py`.
These fixtures live under `tests/hiili-*/` and do not use the active user's
appearance configuration. Tests also simulate activation failures and check
restoration of original files and independent GNOME extensions.

For the GUI workflow test, install Pillow, Xvfb and D-Bus in addition to the
runtime dependencies:

```bash
sudo apt install python3-pil xvfb dbus-daemon
python3 tests/render_ui.py --smoke
```

This runs the built package's program files with private XDG directories, a
private D-Bus session and a virtual X server. Theme import, palette selection,
apply/restore and clipboard/URL matching are exercised. The system file picker
and external browser launch are stubbed; the test never sends a ChatGPT message.
Screenshots are saved under ignored `test-artifacts/`, or a directory set by
`SCREENSHOT_OUTPUT_DIR`. Existing theme files and settings on the real desktop
are not used by these tests.

The native style checks are tied to the verified GNOME 51 environment. A
passing test on a different distribution is not promised. Sandboxed D-Bus
policies may prevent the private dconf backend from writing, which the test
reports as an activation failure.

There is no scheduled CI or automatic release maintenance. See [SUPPORT.md](SUPPORT.md).
