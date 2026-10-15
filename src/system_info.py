"""Read only the public software versions relevant to desktop theme support.

The report deliberately has no user, host, hardware, path or network fields.
All commands are fixed argument lists; they neither invoke a shell nor write
configuration. Missing tools and partially installed packages are ordinary
unknown values, never error output copied into a prompt.
"""

from collections.abc import Mapping
import os
from pathlib import Path
import re
import shlex
import subprocess
import unicodedata


UNKNOWN = "Tuntematon"
KEYS = (
    "distribution", "gnome", "gtk", "libadwaita", "session",
    "yaru_gtk", "yaru_shell", "yaru_icons", "manager",
)
LABELS = {
    "distribution": "Käyttöjärjestelmä",
    "gnome": "GNOME Shell",
    "gtk": "GTK 4",
    "libadwaita": "libadwaita",
    "session": "Istunto",
    "yaru_gtk": "Yaru GTK",
    "yaru_shell": "Yaru GNOME Shell",
    "yaru_icons": "Yaru-kuvakkeet",
    "manager": "Teemamanageri",
}
PACKAGES = {
    "gnome-shell": "gnome",
    "libgtk-4-1": "gtk",
    "libadwaita-1-0": "libadwaita",
    "yaru-theme-gtk": "yaru_gtk",
    "yaru-theme-gnome-shell": "yaru_shell",
    "yaru-theme-icon": "yaru_icons",
}
_VERSION = re.compile(r"[0-9][A-Za-z0-9.+:~\-]{0,63}\Z")
_SEMANTIC = re.compile(r"(?:\d+:)?(\d+(?:\.\d+){0,3})(?=[+~\-]|$)")
_NETWORK = re.compile(r"(?:https?://|www\.|mailto:|@|[A-Za-z0-9-]+\.[A-Za-z]{2,}\b)", re.I)


def _safe_value(key, value):
    if not isinstance(value, str):
        raise ValueError("Järjestelmätiedon pitää olla tekstiä: " + key)
    maximum = 120 if key == "distribution" else 64
    if not value or len(value) > maximum or value != value.strip():
        raise ValueError("Järjestelmätiedon pituus on virheellinen: " + key)
    if any(unicodedata.category(char).startswith("C") for char in value):
        raise ValueError("Järjestelmätieto sisältää ohjausmerkkejä: " + key)
    if value == UNKNOWN:
        return value
    if _NETWORK.search(value) or "\\" in value or any(char in value for char in "<>`$={}[];"):
        raise ValueError("Järjestelmätiedon muoto on virheellinen: " + key)
    if key == "distribution":
        # GNU/Linux is a distribution name component, never a filesystem path.
        plain = value.replace("GNU/Linux", "GNU Linux")
        if "/" in plain or not all(char.isalnum() or char in " .,+()'’_-" for char in plain):
            raise ValueError("Käyttöjärjestelmän nimi on virheellinen")
    elif key == "session":
        if value not in ("Wayland", "X11"):
            raise ValueError("Tuntematon istuntotyyppi")
    elif not _VERSION.fullmatch(value):
        raise ValueError("Version muoto on virheellinen: " + key)
    return value


def validate_system_info(info):
    """Return a canonical report; missing fields become unknown, extras fail.

    This accepts only the report's fixed software fields, so a caller cannot
    accidentally add a username or hostname to the exported prompt.
    """
    if not isinstance(info, Mapping):
        raise ValueError("Järjestelmätietojen pitää olla kenttäluettelo")
    if set(info) - set(KEYS):
        raise ValueError("Järjestelmätiedoissa on ylimääräisiä kenttiä")
    return {key: _safe_value(key, info.get(key, UNKNOWN)) for key in KEYS}


def _read_os_release():
    try:
        with Path("/etc/os-release").open("r", encoding="utf-8") as stream:
            text = stream.read(16385)
        if len(text) > 16384:
            return {}
    except (OSError, UnicodeError):
        return {}
    values = {}
    for line in text.splitlines():
        key, separator, raw = line.partition("=")
        if not separator or key not in ("PRETTY_NAME", "NAME", "ID", "VERSION_ID"):
            continue
        try:
            parts = shlex.split(raw, comments=True, posix=True)
        except ValueError:
            continue
        if len(parts) == 1:
            values[key] = parts[0]
    return values


def _distribution():
    values = _read_os_release()
    candidates = (
        values.get("PRETTY_NAME", ""),
        " ".join(filter(None, (values.get("NAME") or values.get("ID"), values.get("VERSION_ID")))),
    )
    for candidate in candidates:
        try:
            return _safe_value("distribution", candidate)
        except ValueError:
            pass
    return UNKNOWN


def _package_versions():
    result = {}
    try:
        process = subprocess.run(
            ["dpkg-query", "--show", "--showformat=${Package}\t${Version}\n", *PACKAGES],
            capture_output=True, text=True, timeout=3, check=False,
            env={"PATH": "/usr/bin:/bin", "LC_ALL": "C"},
        )
    except (OSError, subprocess.SubprocessError, UnicodeError):
        return result
    # dpkg-query returns 1 when any requested package is absent, while still
    # returning valid installed versions for its other requested packages.
    output = process.stdout
    if not isinstance(output, str) or len(output) > 16384:
        return result
    for line in output.splitlines():
        columns = line.split("\t")
        if len(columns) != 2:
            continue
        name, version = columns
        key = PACKAGES.get(name.split(":", 1)[0])
        if key is None:
            continue
        try:
            _safe_value(key, version)
        except ValueError:
            continue
        if key in ("gnome", "gtk", "libadwaita"):
            match = _SEMANTIC.match(version)
            if not match:
                continue
            version = match.group(1)
        result[key] = version
    return result


def collect_system_info():
    """Collect public software versions without modifying the local system."""
    from palettes import VERSION

    session = {"wayland": "Wayland", "x11": "X11"}.get(os.environ.get("XDG_SESSION_TYPE", "").lower(), UNKNOWN)
    report = {
        "distribution": _distribution(), "session": session, "manager": VERSION,
        **_package_versions(),
    }
    return validate_system_info(report)


def system_target(info=None):
    """Return the short editable Ubuntu/GNOME target used by older releases."""
    report = validate_system_info(collect_system_info() if info is None else info)
    distribution = report["distribution"]
    if report["gnome"] != UNKNOWN:
        return f"{distribution}, GNOME {report['gnome']}"[:160]
    return (distribution + "; GNOME-versio tuntematon")[:160]


def format_system_info(info):
    """Format a validated report for selection, clipboard and prompt export."""
    report = validate_system_info(info)
    return "\n".join(f"{LABELS[key]}: {report[key]}" for key in KEYS)
