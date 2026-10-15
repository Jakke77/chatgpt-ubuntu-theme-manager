"""Import a small, data-only palette format without running theme-provided code.

The package contains only ``theme.json``. CSS, icons and wallpapers are generated
by the manager from its own bundled templates, so theme files never provide
installation commands or paths to write outside the manager's data directory.
"""

import contextlib
import fcntl
import json
import os
from pathlib import Path
import re
import shutil
import stat
import tempfile
import unicodedata
import zipfile
import zlib


PACK_FORMAT = "chatgpt-ubuntu-theme"
PACK_VERSION = 1
MAX_MANIFEST_BYTES = 256 * 1024
MAX_ARCHIVE_BYTES = MAX_MANIFEST_BYTES * 2
COLOR_KEYS = (
    "#11151a", "#0b0e12", "#171c22", "#151a20", "#1e252e",
    "#191f27", "#1c232c", "accent_bg", "accent_light", "folder_top",
    "folder_bottom", "folder_stroke", "glyph",
)
ACCENTS = ("blue", "teal", "green", "yellow", "orange", "red", "pink", "purple", "slate")
_FIELDS = frozenset(("format", "version", "id", "name", "description", "author",
                     "license", "target", "accent", "sample", "colors"))
_RESERVED_IDS = frozenset(("hiili", "graphite", "petrol", "plum", "ubuntu"))
_ID = re.compile(r"[a-z][a-z0-9-]{2,39}\Z", re.ASCII)
_HEX = re.compile(r"#[0-9a-fA-F]{6}\Z", re.ASCII)


def _root():
    return Path(os.environ.get("XDG_DATA_HOME", str(Path.home() / ".local/share"))) / "hiili-theme/imported"


def _string(value, field, maximum, *, nonempty=False):
    if not isinstance(value, str) or len(value) > maximum:
        raise ValueError(f"Teeman kenttä {field} pitää olla enintään {maximum} merkin teksti.")
    if nonempty and not value.strip():
        raise ValueError(f"Teeman kenttä {field} ei saa olla tyhjä.")
    if any(unicodedata.category(char) in ("Cc", "Cs", "Zl", "Zp") for char in value):
        raise ValueError(f"Teeman kentässä {field} on ohjausmerkkejä.")
    return value.strip()


def _luminance(color):
    components = [int(color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [part / 12.92 if part <= 0.04045 else ((part + 0.055) / 1.055) ** 2.4
              for part in components]
    return sum(part * weight for part, weight in zip(linear, (0.2126, 0.7152, 0.0722)))


def _contrast(first, second):
    darker, lighter = sorted((_luminance(first), _luminance(second)))
    return (lighter + 0.05) / (darker + 0.05)


def validate_manifest(value):
    """Validate and return a new canonical manifest; never mutate caller data."""
    if not isinstance(value, dict):
        raise ValueError("Teeman theme.json pitää sisältää JSON-objekti.")
    if any(not isinstance(key, str) for key in value):
        raise ValueError("Teeman kenttien nimien pitää olla tekstiä.")
    if set(value) != _FIELDS:
        missing = sorted(_FIELDS - set(value))
        extra = sorted(set(value) - _FIELDS)
        detail = ("Puuttuu: " + ", ".join(missing) + ". ") if missing else ""
        detail += ("Tuntematon kenttä: " + ", ".join(str(item) for item in extra) + ".") if extra else ""
        raise ValueError("Teeman kentät eivät vastaa tiedostomuotoa. " + detail)
    if value["format"] != PACK_FORMAT or type(value["version"]) is not int or value["version"] != PACK_VERSION:
        raise ValueError("Teemapaketin tiedostomuotoa tai versiota ei tueta.")
    identifier = value["id"]
    if not isinstance(identifier, str) or not _ID.fullmatch(identifier) or identifier in _RESERVED_IDS:
        raise ValueError("Teeman id pitää olla 3–40 pientä kirjainta, numeroa tai yhdysmerkkiä, alkaa kirjaimella ja olla oma nimi.")
    accent = value["accent"]
    if not isinstance(accent, str) or accent not in ACCENTS:
        raise ValueError("Teeman accent ei ole tuettu GNOME-korostusväri.")
    sample = value["sample"]
    if not isinstance(sample, str) or not _HEX.fullmatch(sample):
        raise ValueError("Teeman sample pitää olla väri muodossa #rrggbb.")
    colors = value["colors"]
    if not isinstance(colors, dict) or set(colors) != set(COLOR_KEYS):
        raise ValueError("Teeman colors pitää sisältää täsmälleen kaikki 13 määriteltyä värikenttää.")
    if any(not isinstance(color, str) or not _HEX.fullmatch(color) for color in colors.values()):
        raise ValueError("Teeman kaikkien värien pitää olla muodossa #rrggbb.")
    if any(_contrast("#e3e8ec", colors[key]) < 4.5 for key in COLOR_KEYS if key.startswith("#")):
        raise ValueError("Tämä teemapakettiversio tukee tummia paletteja: tekstin #e3e8ec kontrastin pitää olla vähintään 4.5:1 kaikkiin seitsemään pohjaväriin.")
    if _contrast("#f3f6f6", colors["accent_bg"]) < 4.5:
        raise ValueError("Painiketekstin #f3f6f6 kontrastin pitää olla vähintään 4.5:1 väriin accent_bg.")
    return {
        "format": PACK_FORMAT, "version": PACK_VERSION, "id": identifier,
        "name": _string(value["name"], "name", 80, nonempty=True),
        "description": _string(value["description"], "description", 600),
        "author": _string(value["author"], "author", 120),
        "license": _string(value["license"], "license", 128, nonempty=True),
        "target": _string(value["target"], "target", 160),
        "accent": accent, "sample": sample.lower(),
        "colors": {key: colors[key].lower() for key in COLOR_KEYS},
    }


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Teeman JSON sisältää toistetun kentän: " + key)
        result[key] = value
    return result


def _parse(data):
    if len(data) > MAX_MANIFEST_BYTES:
        raise ValueError("Teeman theme.json on liian suuri (enintään 256 KiB).")
    try:
        value = json.loads(data.decode("utf-8-sig"), object_pairs_hook=_unique_object,
                           parse_constant=lambda value: (_ for _ in ()).throw(ValueError("JSON-vakio ei ole sallittu: " + value)))
    except (UnicodeError, json.JSONDecodeError, RecursionError) as error:
        raise ValueError("Teeman theme.json ei ole kelvollista UTF-8 JSONia.") from error
    return validate_manifest(value)


def _read_bounded(path, maximum):
    # O_NONBLOCK prevents a selected FIFO/device from hanging on open. It has
    # no effect on the regular files accepted below.
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NONBLOCK", 0))
    with os.fdopen(descriptor, "rb") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise ValueError("Teemapaketin pitää olla tavallinen tiedosto.")
        data = stream.read(maximum + 1)
    if len(data) > maximum:
        raise ValueError("Teemapaketti on liian suuri.")
    return data


def _read_source(path):
    path = Path(path)
    if path.suffix.lower() == ".json":
        return _parse(_read_bounded(path, MAX_MANIFEST_BYTES))
    if path.suffix.lower() != ".zip":
        raise ValueError("Valitse .ctm-theme.zip-teemapaketti tai theme.json-tiedosto.")
    # Read the whole archive with a firm bound before letting ZipFile inspect it.
    # This also prevents a changing source file from bypassing the size checks.
    import io
    data = _read_bounded(path, MAX_ARCHIVE_BYTES)
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            entries = archive.infolist()
            if len(entries) != 1 or entries[0].filename != "theme.json" or entries[0].is_dir():
                raise ValueError("ZIP-paketti saa sisältää vain yhden theme.json-tiedoston juurihakemistossa.")
            entry = entries[0]
            mode = entry.external_attr >> 16
            kind = stat.S_IFMT(mode)
            if kind not in (0, stat.S_IFREG) or mode & 0o111 or entry.flag_bits & 1:
                raise ValueError("ZIP-paketti ei saa sisältää linkkejä, erikoistiedostoja, suoritettavia tiedostoja tai salausta.")
            if entry.file_size > MAX_MANIFEST_BYTES or entry.compress_size > MAX_ARCHIVE_BYTES:
                raise ValueError("Teeman theme.json on liian suuri (enintään 256 KiB).")
            with archive.open(entry) as stream:
                manifest = stream.read(MAX_MANIFEST_BYTES + 1)
            return _parse(manifest)
    except (zipfile.BadZipFile, zipfile.LargeZipFile, NotImplementedError, RuntimeError, EOFError, zlib.error) as error:
        raise ValueError("Teemapaketin ZIP-tiedostoa ei voitu lukea.") from error


def _catalog_entry(manifest):
    return {
        **manifest, "theme": "Hiili-User-" + manifest["id"],
        "imported": True,
    }


def catalog():
    """Return valid imported palettes, ignoring unfinished/invalid directories."""
    result = {}
    root = _root()
    if not root.is_dir() or root.is_symlink():
        return result
    try:
        directories = sorted(root.iterdir())
    except OSError:
        return result
    for directory in directories:
        if directory.is_symlink() or not directory.is_dir() or not _ID.fullmatch(directory.name):
            continue
        path = directory / "theme.json"
        if path.is_symlink() or not path.is_file():
            continue
        try:
            manifest = _parse(_read_bounded(path, MAX_MANIFEST_BYTES))
            if manifest["id"] != directory.name:
                continue
            result["user:" + manifest["id"]] = _catalog_entry(manifest)
        except (ValueError, OSError):
            continue
    return result


@contextlib.contextmanager
def _locked(root):
    root.mkdir(parents=True, exist_ok=True)
    if root.is_symlink():
        raise ValueError("Teemakirjasto ei saa olla symbolinen linkki.")
    flags = os.O_CREAT | os.O_RDWR | getattr(os, "O_NOFOLLOW", 0)
    with os.fdopen(os.open(root / ".import.lock", flags, 0o600), "a+") as stream:
        fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
        yield


def import_theme(path):
    """Install a validated manifest atomically and return (variant, metadata).

    Existing IDs are deliberately rejected: importing a file cannot silently
    change the appearance of a theme the user already selected.
    """
    manifest = _read_source(path)
    root = _root()
    with _locked(root):
        target = root / manifest["id"]
        if os.path.lexists(target):
            raise ValueError("Teema samalla id:llä on jo tuotu: " + manifest["id"] + ". Anna uudelle versiolle eri id.")
        temporary = Path(tempfile.mkdtemp(prefix=".import-", dir=root))
        try:
            content = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
            with (temporary / "theme.json").open("xb") as stream:
                stream.write(content)
                stream.flush()
                os.fsync(stream.fileno())
            os.chmod(temporary / "theme.json", 0o644)
            temporary.rename(target)
        finally:
            if temporary.exists():
                shutil.rmtree(temporary)
    return "user:" + manifest["id"], _catalog_entry(manifest)


def example_manifest():
    """A complete theme that can also serve as the format's minimal example."""
    return {
        "format": PACK_FORMAT, "version": PACK_VERSION,
        "id": "metsayo", "name": "Metsäyö", "description": "Tumma metsä: mustaa, havunvihreää ja pehmeitä vihreitä korostuksia.",
        "author": "Yhteisön esimerkkiteema", "license": "CC0-1.0",
        "target": "Ubuntu / GNOME (väripaletti; kohdeversio tarkistetaan erikseen)",
        "accent": "green", "sample": "#315447",
        "colors": {
            "#11151a": "#111914", "#0b0e12": "#0a100c",
            "#171c22": "#1b261f", "#151a20": "#162119",
            "#1e252e": "#26352b", "#191f27": "#202e25",
            "#1c232c": "#2b3b30", "accent_bg": "#3e6b50",
            "accent_light": "#b4d6bd", "folder_top": "#3c6750",
            "folder_bottom": "#1e3828", "folder_stroke": "#719e7e",
            "glyph": "#c4ddca",
        },
    }
