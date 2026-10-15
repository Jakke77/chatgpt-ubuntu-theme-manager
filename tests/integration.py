#!/usr/bin/python3
"""Exercise actual GSettings keyfile persistence, user files and rollback."""
import base64
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

BASE = Path(__file__).resolve().parents[1]
fixture = Path(tempfile.mkdtemp(prefix="hiili-integration-", dir=BASE / "tests"))
os.environ["XDG_CONFIG_HOME"] = str(fixture / "config")
os.environ["XDG_DATA_HOME"] = str(fixture / "share")
os.environ["GSETTINGS_BACKEND"] = "keyfile"
os.environ["HIILI_DATA_DIR"] = str(BASE / "package/usr/share/hiili-theme")
sys.path.insert(0, str(BASE / "src"))
import engine

config = engine.CONFIG
config.mkdir(parents=True)
for version in ("gtk-3.0", "gtk-4.0"):
    (config / version).mkdir()
    (config / version / "settings.ini").write_text("# My original setting\n[Settings]\ngtk-application-prefer-dark-theme=0\ngtk-font-name=Adwaita Sans 11\n")
css = config / "gtk-4.0/gtk.css"
css.write_text('/* Existing customization */\n@import url("local.css");\nwindow { opacity: 0.99; }\n')
(css.parent / "local.css").write_text("label { letter-spacing: 0.1px; }\n")
original_files = {str(p): p.read_bytes() for p in (css, config / "gtk-3.0/settings.ini", config / "gtk-4.0/settings.ini")}
interface = engine.settings("org.gnome.desktop.interface")
interface.set_string("gtk-theme", "Adwaita")
interface.set_string("icon-theme", "Original-Test-Icons")
interface.set_string("color-scheme", "default")
interface.set_string("accent-color", "orange")
shell = engine.settings("org.gnome.shell")
shell.set_strv("enabled-extensions", ["existing@example.test"])
shell.set_strv("disabled-extensions", [engine.UUID])
engine.Gio.Settings.sync()

engine.apply()
assert engine.status()["active"]
assert engine.UUID in shell.get_strv("enabled-extensions")
assert engine.UUID not in shell.get_strv("disabled-extensions")
assert interface.get_string("icon-theme") == "Hiili"
state_before = engine.load_state()
engine.apply()
state_after = engine.load_state()
assert [x["original"] for x in state_before["settings"]] == [x["original"] for x in state_after["settings"]], "Reapply replaced original backup"
assert (config / "gtk-4.0/hiili-before.css").read_bytes() == original_files[str(css)]
shell.set_strv("enabled-extensions", list(shell.get_strv("enabled-extensions")) + ["installed-later@example.test"])
assert not engine.restore()
for name, content in original_files.items():
    assert Path(name).read_bytes() == content, "Original config not restored byte for byte"
assert not (config / "gtk-4.0/hiili-before.css").exists()
assert interface.get_string("icon-theme") == "Original-Test-Icons"
assert interface.get_string("gtk-theme") == "Adwaita"
assert shell.get_strv("enabled-extensions") == ["existing@example.test", "installed-later@example.test"]
assert engine.UUID in shell.get_strv("disabled-extensions")
print("PASS: apply, reapply, byte-for-byte restoration and unrelated extensions")

# Cross-process reads ensure this is actual persistent GSettings data.
read = subprocess.run(["gsettings", "get", "org.gnome.desktop.interface", "icon-theme"], capture_output=True, text=True, check=True)
assert read.stdout.strip() == "'Original-Test-Icons'"
print("PASS: GSettings persists across processes")

# Every palette must change the actual theme and icons while retaining the
# same original backup across switches. This includes the 1.0 theme name.
for variant, selected in engine.PALETTES.items():
    current = engine.apply(wallpaper=False, variant=variant)
    assert current["variant"] == variant and current["active"]
    assert interface.get_string("gtk-theme") == selected["theme"]
    assert interface.get_string("icon-theme") == selected["theme"]
    assert interface.get_string("accent-color") == selected["accent"]
    colors = engine.DATA / "variants" / variant / "gtk4.css"
    assert colors.is_file()
engine.restore()
assert interface.get_string("icon-theme") == "Original-Test-Icons"
for name, content in original_files.items():
    assert Path(name).read_bytes() == content
print("PASS: all five palettes switch and restore the original settings")

# A downloaded data-only theme becomes a persistent sixth palette, including
# real GTK/Shell assets, icons and wallpaper, with no application launcher.
from theme_packs import example_manifest, import_theme
download = fixture / "metsayo.json"
download.write_text(json.dumps(example_manifest(), ensure_ascii=False))
key, selected = import_theme(download)
assert key == "user:metsayo" and len(engine.all_palettes()) == 6
assert not (engine.SHARE / "applications").exists()
current = engine.apply(variant=key)
assert current["active"] and current["variant"] == key
assert interface.get_string("icon-theme") == selected["theme"]
assets = engine.variant_data(key)
assert selected["colors"]["#11151a"] in (assets / "gtk4.css").read_text()
assert engine.settings("org.gnome.desktop.background").get_string("picture-uri") == (assets / "wallpaper.svg").as_uri()
icons = engine.SHARE / "icons" / selected["theme"]
assert (icons / "index.theme").is_file()
for path in icons.rglob("*"):
    if path.is_symlink():
        assert path.exists(), path
assert selected["colors"]["folder_top"] in (icons / "scalable/places/folder.svg").read_text()
# A failed regeneration during a future manager update must leave the current
# marked icon theme intact instead of deleting it before staging succeeds.
marker = icons / ".hiili-managed"
marker.write_text("older-manager-version")
original_copytree = engine.shutil.copytree
def fail_icon_copy(*args, **kwargs):
    raise RuntimeError("simulated icon regeneration failure")
engine.shutil.copytree = fail_icon_copy
try:
    try:
        engine.prepare_icons(key)
    except RuntimeError:
        pass
    else:
        raise AssertionError("Injected icon generation failure was ignored")
finally:
    engine.shutil.copytree = original_copytree
assert marker.read_text() == "older-manager-version"
assert (icons / "scalable/places/folder.svg").is_file()
engine.prepare_icons(key)
assert marker.read_text() != "older-manager-version"
before = engine.load_state()
engine.apply(wallpaper=False, variant="plum")
engine.apply(wallpaper=False, variant=key)
after = engine.load_state()
assert [x["original"] for x in before["settings"]] == [x["original"] for x in after["settings"]]
command = BASE / "src/hiili-theme"
listed = subprocess.run([sys.executable, str(command), "--list-themes"], capture_output=True, text=True, check=True)
assert json.loads(listed.stdout)[key]["name"] == "Metsäyö"
persisted = subprocess.run([sys.executable, str(command), "--status-json"], capture_output=True, text=True, check=True)
assert json.loads(persisted.stdout)["variant"] == key
installed_manifest = engine.SHARE / "hiili-theme/imported/metsayo/theme.json"
original_manifest = installed_manifest.read_bytes()
changed_manifest = json.loads(original_manifest)
changed_manifest["name"] = "Explicit pornography"
installed_manifest.write_text(json.dumps(changed_manifest))
assert key not in engine.all_palettes(), "Changed content bypassed catalog validation"
state_bytes = engine.STATE_FILE.read_bytes()
assert engine.status()["backup_available"], "Hidden metadata disabled appearance restoration"
try:
    engine.apply(variant=key)
except ValueError:
    pass
else:
    raise AssertionError("Changed metadata bypassed activation validation")
assert engine.STATE_FILE.read_bytes() == state_bytes
assert interface.get_string("gtk-theme") == selected["theme"]
engine.restore()
installed_manifest.write_bytes(original_manifest)
assert interface.get_string("icon-theme") == "Original-Test-Icons"
for name, content in original_files.items():
    assert Path(name).read_bytes() == content
print("PASS: imported palette persists, applies matching CSS/icons/wallpaper and restores without a new launcher")
print("PASS: changed unsafe metadata cannot be selected or applied; original appearance still restores")

# Restore original symlinks rather than replacing them with regular files.
css.unlink()
css.symlink_to("local.css")
engine.apply(wallpaper=False)
assert css.is_file() and not css.is_symlink()
engine.restore()
assert css.is_symlink() and os.readlink(css) == "local.css"
print("PASS: original CSS symlink is restored")

# Preserve changes users make after installation, including the imported original.
css.unlink()
css.write_text("label { color: #c0c0c0; }\n")
engine.apply()
with css.open("a") as f:
    f.write("/* A new user edit */\n")
warnings = engine.restore()
assert warnings and "A new user edit" in css.read_text()
assert (css.parent / "hiili-before.css").exists(), "Retained wrapper lost its original imported CSS"
print("PASS: later user edits and their imported CSS are preserved")

# New fixture for rollback so the intentionally preserved file above is untouched.
second = Path(tempfile.mkdtemp(prefix="hiili-rollback-", dir=BASE / "tests"))
env = dict(os.environ, XDG_CONFIG_HOME=str(second / "config"), XDG_DATA_HOME=str(second / "share"))
code = '''
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import engine
engine.CONFIG.mkdir(parents=True)
css = engine.CONFIG / "gtk-4.0/gtk.css"
css.parent.mkdir()
css.write_text("/* untouched */")
obj = engine.settings("org.gnome.desktop.interface")
obj.set_string("gtk-theme", "Adwaita")
def failure(state):
    raise RuntimeError("simulated activation failure")
engine._extension_enable = failure
try:
    engine.apply()
except RuntimeError:
    pass
else:
    raise AssertionError("Injected failure was ignored")
assert css.read_text() == "/* untouched */"
assert not (css.parent / "hiili-before.css").exists()
assert not (engine.CONFIG / "gtk-3.0/settings.ini").exists()
assert obj.get_string("gtk-theme") == "Adwaita"
assert not engine.load_state()["active"]
print("PASS: an activation failure rolls back file and settings changes")
'''
subprocess.run([sys.executable, "-c", code, str(BASE / "src")], env=env, check=True)
print("All integration checks passed.")
print("Fixture:", fixture)
