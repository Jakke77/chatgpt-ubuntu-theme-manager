"""Hiili appearance installation, with per-user backups and reversible settings."""
from __future__ import annotations

import base64
import configparser
import contextlib
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile

import gi
gi.require_version("Gio", "2.0")
from gi.repository import Gio, GLib
from palettes import VERSION, PALETTES, all_palettes, palette, recolor, variant_for_theme

UUID = "user-theme@gnome-shell-extensions.gcampax.github.com"
DATA = Path(os.environ.get("HIILI_DATA_DIR", "/usr/share/hiili-theme"))
USER_HOME = Path.home()
CONFIG = Path(os.environ.get("XDG_CONFIG_HOME", str(USER_HOME / ".config")))
SHARE = Path(os.environ.get("XDG_DATA_HOME", str(USER_HOME / ".local/share")))
STATE = CONFIG / "hiili-theme"
STATE_FILE = STATE / "state.json"
MARKER = "/* HIILI MANAGED: use Hiili's Restore button to restore the previous file. */"


def settings(schema):
    source = Gio.SettingsSchemaSource.get_default()
    found = source.lookup(schema, True) if source else None
    return Gio.Settings.new_full(found, None, None) if found else None


def atomic_write(path, data, mode=0o644):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".hiili-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data if isinstance(data, bytes) else data.encode())
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(name, mode)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


@contextlib.contextmanager
def locked():
    STATE.mkdir(parents=True, exist_ok=True, mode=0o700)
    with (STATE / "lock").open("a") as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        yield


def load_state():
    if not STATE_FILE.exists():
        return None
    state = json.loads(STATE_FILE.read_text())
    if state.get("format") != 1:
        raise RuntimeError("Ulkoasun varmuuskopion versio on tuntematon.")
    return state


def save_state(state):
    atomic_write(STATE_FILE, json.dumps(state, ensure_ascii=False, indent=2), 0o600)


def file_snapshot(path):
    path = Path(path)
    if path.is_symlink():
        return {"kind": "symlink", "target": os.readlink(path)}
    if path.exists():
        if not path.is_file():
            raise RuntimeError(f"Asetustiedoston paikalla on hakemisto: {path}")
        return {"kind": "file", "data": base64.b64encode(path.read_bytes()).decode(),
                "mode": stat.S_IMODE(path.stat().st_mode)}
    return {"kind": "absent"}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def variant_data(variant="hiili"):
    """Build imported palettes from trusted bundled artwork, never pack code."""
    selected = palette(variant)
    if not selected.get("imported"):
        return DATA / "variants" / variant
    fingerprint = hashlib.sha256((VERSION + json.dumps(selected, sort_keys=True)).encode()).hexdigest()
    parent = SHARE / "hiili-theme/generated"
    target = parent / (variant.removeprefix("user:") + "-" + fingerprint[:16])
    if (target / ".hiili-managed").is_file():
        return target
    parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".palette-", dir=parent))
    try:
        for name in ("gtk3.css", "gtk4.css", "shell.css"):
            atomic_write(staging / name, recolor((DATA / name).read_text(), variant))
        atomic_write(staging / "wallpaper.svg", recolor((DATA / "hiili.svg").read_text(), variant))
        for path in (DATA / "icon-preview").glob("*.svg"):
            atomic_write(staging / "icon-preview" / path.name, recolor(path.read_text(), variant, icons=True))
        atomic_write(staging / ".hiili-managed", fingerprint)
        try:
            staging.rename(target)
        except OSError:
            if not (target / ".hiili-managed").is_file():
                raise
        return target
    finally:
        if staging.exists():
            shutil.rmtree(staging)


def prepare_icons(variant):
    selected = palette(variant)
    if not selected.get("imported"):
        return
    fingerprint = hashlib.sha256((VERSION + json.dumps(selected, sort_keys=True)).encode()).hexdigest()
    target = SHARE / "icons" / selected["theme"]
    marker = target / ".hiili-managed"
    if target.exists():
        if not marker.is_file():
            raise RuntimeError("Samanniminen kuvaketeema on jo olemassa. Sitä ei korvattu.")
        if marker.read_text() == fingerprint:
            return
    target.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".icons-", dir=target.parent))
    try:
        shutil.copytree(DATA.parent / "icons/Hiili", staging, symlinks=True, dirs_exist_ok=True)
        (staging / "icon-theme.cache").unlink(missing_ok=True)
        for path in staging.rglob("*.svg"):
            if not path.is_symlink():
                atomic_write(path, recolor(path.read_text(), variant, icons=True))
        index = staging / "index.theme"
        atomic_write(index, index.read_text().replace("Name=Hiili\n", "Name=" + selected["theme"] + "\n"))
        atomic_write(staging / ".hiili-managed", fingerprint)
        previous = staging.with_name(staging.name + "-previous")
        if target.exists():
            target.rename(previous)
        try:
            staging.rename(target)
        except Exception:
            if previous.exists():
                previous.rename(target)
            raise
        if previous.exists():
            shutil.rmtree(previous)
    finally:
        if staging.exists():
            shutil.rmtree(staging)


def theme_targets(wallpaper=True, variant="hiili"):
    selected = palette(variant)
    targets = [
        ("org.gnome.desktop.interface", "gtk-theme", selected["theme"]),
        ("org.gnome.desktop.interface", "icon-theme", selected["theme"]),
        ("org.gnome.desktop.interface", "color-scheme", "prefer-dark"),
        ("org.gnome.desktop.interface", "accent-color", selected["accent"]),
        ("org.gnome.shell.extensions.user-theme", "name", selected["theme"]),
    ]
    if wallpaper:
        uri = (variant_data(variant) / selected.get("wallpaper", "wallpaper.svg")).as_uri()
        targets += [
            ("org.gnome.desktop.background", "picture-uri", uri),
            ("org.gnome.desktop.background", "picture-uri-dark", uri),
            ("org.gnome.desktop.background", "picture-options", "zoom"),
            ("org.gnome.desktop.background", "primary-color", "#070508" if variant == "veriyo" else "#090b0e"),
            ("org.gnome.desktop.background", "secondary-color", "#160b12" if variant == "veriyo" else "#10171a"),
        ]
    return targets


def _capture_settings(targets, old=None):
    captured = {(item["schema"], item["key"]): item for item in (old or [])}
    for schema, key, _ in targets:
        obj = settings(schema)
        if not obj or not obj.props.settings_schema.has_key(key):
            continue
        if not obj.is_writable(key):
            raise RuntimeError(f"Järjestelmän käytäntö estää asetuksen muuttamisen: {key}")
        if (schema, key) not in captured:
            value = obj.get_user_value(key)
            captured[schema, key] = {"schema": schema, "key": key,
                                     "original": value.print_(True) if value else None}
    return list(captured.values())


def _resource_tree(resource, prefix, destination):
    for name in resource.enumerate_children(prefix, 0):
        if name.endswith("/"):
            (destination / name).mkdir(parents=True, exist_ok=True)
            _resource_tree(resource, prefix + name, destination / name)
        else:
            atomic_write(destination / name, resource.lookup_data(prefix + name, 0).get_data())


def prepare_theme(variant="hiili"):
    """Reuse the installed Ubuntu version's matching controls and shell CSS."""
    selected = palette(variant)
    assets = variant_data(variant)
    prepare_icons(variant)
    theme = SHARE / "themes" / selected["theme"]
    if theme.exists() and not (theme / ".hiili-managed").is_file():
        raise RuntimeError("Samanniminen Hiili-teema on jo olemassa. Sitä ei korvattu.")
    gtk = theme / "gtk-3.0"
    gtk.mkdir(parents=True, exist_ok=True)
    atomic_write(theme / ".hiili-managed", "Hiili theme assets\n")
    resource = Gio.Resource.load("/usr/share/themes/Yaru-dark/gtk-3.0/gtk.gresource")
    prefix = "/com/ubuntu/themes/Yaru-dark/3.0/"
    _resource_tree(resource, prefix, gtk)
    base = (gtk / "gtk.css").read_text()
    base = base.replace("resource://" + prefix, "")
    replacements = {
        "#e95420": "#496b72", "#f7f7f7": "#e6e9ed", "#181818": "#0e1115",
        "#1c1c1c": "#11151a", "#222222": "#171c22", "#2c2c2c": "#20262d",
        "#2a2a2a": "#1c2229", "#272727": "#191e24", "#343434": "#292f38",
    }
    base = re.sub(r"#[0-9a-fA-F]{6}\b", lambda m: replacements.get(m[0].lower(), m[0]), base)
    atomic_write(gtk / "yaru-base.css", recolor(base, variant))
    css = '@import url("yaru-base.css");\n' + (assets / "gtk3.css").read_text()
    atomic_write(gtk / "gtk.css", css)
    atomic_write(gtk / "gtk-dark.css", css)

    shell = theme / "gnome-shell"
    shell.mkdir(exist_ok=True)
    original = Path("/usr/share/gnome-shell/theme/Yaru-dark")
    for item in original.iterdir():
        if item.is_file():
            shutil.copy2(item, shell / item.name)
    base = (shell / "gnome-shell.css").read_text()
    shell_colors = {"#36363a": "#171b21", "#2e2e32": "#11151a", "#47474c": "#262d35",
                    "#222226": "#101318", "#28282c": "#12161c", "#3a3a3f": "#20262d"}
    base = re.sub(r"#[0-9a-fA-F]{6}\b", lambda m: shell_colors.get(m[0].lower(), m[0]), base)
    atomic_write(shell / "gnome-shell.css", recolor(base, variant) + "\n" + (assets / "shell.css").read_text())
    name = selected["theme"]
    atomic_write(theme / "index.theme", f"[Desktop Entry]\nName={name}\nType=X-GNOME-Metatheme\nComment=Hiili dark theme variant\n\n[X-GNOME-Metatheme]\nGtkTheme={name}\nIconTheme={name}\nCursorTheme=Adwaita\n")


def _write_managed(path, content, state):
    path = Path(path)
    atomic_write(path, content)
    state["files"][str(path)]["written_sha256"] = digest(path)
    save_state(state)


def _gtk_settings(path, state):
    parser = configparser.ConfigParser(interpolation=None)
    parser.optionxform = str
    if path.exists():
        parser.read_string(path.read_text())
    if not parser.has_section("Settings"):
        parser.add_section("Settings")
    parser.set("Settings", "gtk-application-prefer-dark-theme", "1")
    import io
    output = io.StringIO()
    parser.write(output)
    _write_managed(path, output.getvalue(), state)


def _extension_enable(state):
    shell = settings("org.gnome.shell")
    if not shell:
        return
    if "extension" not in state:
        state["extension"] = {"was_enabled": UUID in shell.get_strv("enabled-extensions"),
                              "was_disabled": UUID in shell.get_strv("disabled-extensions")}
        save_state(state)
    enabled = list(shell.get_strv("enabled-extensions"))
    disabled = list(shell.get_strv("disabled-extensions"))
    if UUID not in enabled:
        shell.set_strv("enabled-extensions", enabled + [UUID])
    if UUID in disabled:
        shell.set_strv("disabled-extensions", [x for x in disabled if x != UUID])


def verify_persisted(records):
    """GSettings may accept a write that the asynchronous backend later rejects."""
    records = [x for x in records if x.get("applied")]
    reader = """import json, sys
from gi.repository import Gio
items=json.loads(sys.argv[1])
print(json.dumps([Gio.Settings.new(item['schema']).get_value(item['key']).print_(True) for item in items]))
"""
    result = subprocess.run([sys.executable, "-c", reader, json.dumps(records)],
                            capture_output=True, text=True, timeout=15, check=True)
    persisted = json.loads(result.stdout)
    for item, actual in zip(records, persisted):
        if actual != item["applied"]:
            raise RuntimeError("GNOME ei tallentanut ulkoasuasetusta: " + item["key"])


def apply(wallpaper=True, variant="hiili"):
    if os.geteuid() == 0:
        raise RuntimeError("Teema otetaan käyttöön tavallisena käyttäjänä.")
    with locked():
        targets = theme_targets(wallpaper, variant)
        state = load_state()
        if not state or not state.get("active"):
            state = {"format": 1, "version": VERSION, "active": False, "settings": [], "files": {}}
        state["settings"] = _capture_settings(targets, state["settings"])
        files = [CONFIG / "gtk-3.0/settings.ini", CONFIG / "gtk-4.0/settings.ini",
                 CONFIG / "gtk-4.0/gtk.css", CONFIG / "gtk-4.0/hiili-before.css"]
        for path in files:
            if str(path) not in state["files"]:
                state["files"][str(path)] = file_snapshot(path)
        before = CONFIG / "gtk-4.0/hiili-before.css"
        before_record = state["files"][str(before)]
        if before_record["kind"] != "absent":
            raise RuntimeError("gtk-4.0/hiili-before.css on jo olemassa. Sitä ei korvattu.")
        state["active"] = True
        save_state(state)
        try:
            prepare_theme(variant)
            original_css = state["files"][str(CONFIG / "gtk-4.0/gtk.css")]
            imports = []
            if original_css["kind"] == "file" and original_css["data"]:
                _write_managed(before, base64.b64decode(original_css["data"]), state)
                imports.append(before.as_uri())
            elif original_css["kind"] == "symlink":
                target = Path(original_css["target"])
                if not target.is_absolute():
                    target = CONFIG / "gtk-4.0" / target
                imports.append(target.resolve().as_uri())
            imports.append((variant_data(variant) / "gtk4.css").as_uri())
            wrapper = MARKER + "\n" + "\n".join(f'@import url("{uri}");' for uri in imports) + "\n"
            _write_managed(CONFIG / "gtk-4.0/gtk.css", wrapper, state)
            for version in ("gtk-3.0", "gtk-4.0"):
                _gtk_settings(CONFIG / version / "settings.ini", state)
            _extension_enable(state)
            for schema, key, value in targets:
                obj = settings(schema)
                record = next((x for x in state["settings"] if x["schema"] == schema and x["key"] == key), None)
                if not record:
                    continue
                if not obj.set_string(key, value):
                    raise RuntimeError(f"Asetuksen muuttaminen epäonnistui: {key}")
                record["applied"] = obj.get_value(key).print_(True)
                save_state(state)
            Gio.Settings.sync()
            changed_keys = {(schema, key) for schema, key, _ in targets}
            verify_persisted([record for record in state["settings"]
                              if (record["schema"], record["key"]) in changed_keys])
            state["version"] = VERSION
            state["variant"] = variant
            save_state(state)
        except Exception:
            _restore(state, respect_changes=False)
            raise
    return status()


def _restore(state, respect_changes=True):
    warnings = []
    css_path = CONFIG / "gtk-4.0/gtk.css"
    css_record = state.get("files", {}).get(str(css_path), {})
    keep_css_backup = bool(respect_changes and css_record.get("written_sha256") and
                           (not css_path.is_file() or css_path.is_symlink() or
                            digest(css_path) != css_record["written_sha256"]))
    for path_string, record in state.get("files", {}).items():
        if "written_sha256" not in record:
            continue
        path = Path(path_string)
        if keep_css_backup and path == CONFIG / "gtk-4.0/hiili-before.css":
            continue
        expected_parent = path.parent in (CONFIG / "gtk-3.0", CONFIG / "gtk-4.0")
        if not expected_parent:
            raise RuntimeError("Varmuuskopiossa on tuntematon asetustiedoston polku.")
        if respect_changes and (not path.is_file() or path.is_symlink() or digest(path) != record["written_sha256"]):
            warnings.append(f"Myöhemmin muokattu tiedosto säilytettiin: {path}")
            continue
        if record["kind"] == "absent":
            path.unlink(missing_ok=True)
        elif record["kind"] == "symlink":
            path.unlink(missing_ok=True)
            path.symlink_to(record["target"])
        else:
            atomic_write(path, base64.b64decode(record["data"]), record.get("mode", 0o644))
    for record in state.get("settings", []):
        obj = settings(record["schema"])
        if not obj:
            continue
        if respect_changes and record.get("applied") and obj.get_value(record["key"]).print_(True) != record["applied"]:
            continue
        if record["original"] is None:
            obj.reset(record["key"])
        else:
            value = GLib.Variant.parse(None, record["original"], None, None)
            obj.set_value(record["key"], value)
    extension = state.get("extension")
    shell = settings("org.gnome.shell")
    if extension and shell:
        for key, wanted in (("enabled-extensions", extension["was_enabled"]),
                            ("disabled-extensions", extension["was_disabled"])):
            values = list(shell.get_strv(key))
            values = [x for x in values if x != UUID]
            if wanted:
                values.append(UUID)
            shell.set_strv(key, values)
    Gio.Settings.sync()
    state["active"] = False
    state["restore_warnings"] = warnings
    save_state(state)
    return warnings


def restore(respect_changes=True):
    with locked():
        state = load_state()
        if not state or not state.get("active"):
            return []
        return _restore(state, respect_changes)


def status():
    obj = settings("org.gnome.desktop.interface")
    state = load_state()
    current_variant = variant_for_theme(obj.get_string("gtk-theme")) if obj else None
    saved_variant = (state or {}).get("variant", "hiili")
    if saved_variant not in all_palettes():
        saved_variant = "hiili"
    return {"version": VERSION, "active": current_variant is not None,
            "variant": current_variant or saved_variant,
            "backup_available": bool(state and state.get("active")),
            "theme": obj.get_string("gtk-theme") if obj else None,
            "icons": obj.get_string("icon-theme") if obj else None,
            "color_scheme": obj.get_string("color-scheme") if obj else None}
