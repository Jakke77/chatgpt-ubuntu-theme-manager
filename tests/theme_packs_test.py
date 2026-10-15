"""Exercise the data-only import boundary using private temporary user data."""

from concurrent.futures import ThreadPoolExecutor
import copy
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
import warnings
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import theme_packs
from content_policy import ContentPolicyError


class ThemePacksTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="ctm-theme-packs-")
        self.base = Path(self.temp.name)
        self.data = self.base / "data"
        self.env = patch.dict(os.environ, {"XDG_DATA_HOME": str(self.data)})
        self.env.start()
        self.manifest = theme_packs.example_manifest()
        self.root = self.data / "hiili-theme/imported"

    def tearDown(self):
        self.env.stop()
        self.temp.cleanup()

    def write_json(self, manifest=None, name="theme.json"):
        path = self.base / name
        path.write_text(json.dumps(self.manifest if manifest is None else manifest), encoding="utf-8")
        return path

    def write_zip(self, entries=None, name="theme.ctm-theme.zip"):
        path = self.base / name
        if entries is None:
            entries = [("theme.json", json.dumps(self.manifest))]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                for filename, content in entries:
                    archive.writestr(filename, content)
        return path

    def assert_rejected(self, path):
        before = theme_packs.catalog()
        with self.assertRaises(ValueError):
            theme_packs.import_theme(path)
        self.assertEqual(before, theme_packs.catalog())

    def test_example_has_complete_contract(self):
        validated = theme_packs.validate_manifest(self.manifest)
        self.assertEqual(validated, self.manifest)
        self.assertEqual(set(theme_packs.COLOR_KEYS), set(validated["colors"]))

    def test_plain_json_import_and_catalog_are_persistent(self):
        key, metadata = theme_packs.import_theme(self.write_json())
        self.assertEqual(key, "user:metsayo")
        self.assertEqual(metadata["theme"], "Hiili-User-metsayo")
        self.assertTrue(metadata["imported"])
        self.assertEqual(theme_packs.catalog()[key], metadata)
        installed = self.root / "metsayo/theme.json"
        self.assertEqual(json.loads(installed.read_text()), self.manifest)
        self.assertEqual(stat.S_IMODE(installed.stat().st_mode), 0o644)
        self.assertFalse((self.data / "applications").exists())
        self.assertEqual(sorted(str(item.relative_to(self.root)) for item in self.root.rglob("*") if item.is_file()),
                         [".import.lock", "metsayo/theme.json"])

    def test_zip_import(self):
        key, metadata = theme_packs.import_theme(self.write_zip())
        self.assertEqual(metadata["name"], "Metsäyö")
        self.assertIn(key, theme_packs.catalog())

    def test_content_policy_blocks_both_json_and_zip_before_writing(self):
        self.manifest["description"] = "Identity theft and steal passwords"
        for path in (self.write_json(), self.write_zip()):
            with self.subTest(path=path), self.assertRaises(ContentPolicyError):
                theme_packs.import_theme(path)
            self.assertFalse(self.root.exists(), "Rejected content created an imported theme")

    def test_catalog_rechecks_changed_metadata_without_deleting_files(self):
        theme_packs.import_theme(self.write_json())
        installed = self.root / "metsayo/theme.json"
        self.manifest["name"] = "Explicit pornography"
        installed.write_text(json.dumps(self.manifest))
        self.assertEqual(theme_packs.catalog(), {})
        self.assertTrue(installed.is_file())

    def test_color_case_normalized_without_mutating_input(self):
        self.manifest["sample"] = "#ABCDEF"
        self.manifest["colors"]["glyph"] = "#FEDCBA"
        valid = theme_packs.validate_manifest(self.manifest)
        self.assertEqual(valid["sample"], "#abcdef")
        self.assertEqual(valid["colors"]["glyph"], "#fedcba")
        self.assertEqual(self.manifest["sample"], "#ABCDEF")

    def test_duplicate_id_does_not_overwrite_original(self):
        source = self.write_json()
        theme_packs.import_theme(source)
        original = (self.root / "metsayo/theme.json").read_bytes()
        self.manifest["name"] = "Changed"
        self.assert_rejected(self.write_json())
        self.assertEqual((self.root / "metsayo/theme.json").read_bytes(), original)

    def test_concurrent_imports_have_single_winner(self):
        first = self.write_json(name="one.json")
        self.manifest["name"] = "Metsäyö kaksi"
        second = self.write_json(name="two.json")
        barrier = threading.Barrier(2)

        def attempt(path):
            barrier.wait()
            try:
                return theme_packs.import_theme(path)[0]
            except ValueError:
                return None

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(attempt, (first, second)))
        self.assertEqual(results.count("user:metsayo"), 1)
        self.assertEqual(results.count(None), 1)
        self.assertEqual(list(theme_packs.catalog()), ["user:metsayo"])
        self.assertFalse(list(self.root.glob(".import-*")))

    def test_manifest_fields_are_strict(self):
        for field in self.manifest:
            invalid = copy.deepcopy(self.manifest)
            del invalid[field]
            with self.subTest(missing=field), self.assertRaises(ValueError):
                theme_packs.validate_manifest(invalid)
        for extra in ("script", "gtk_css", "desktop_file", "path", "theme"):
            invalid = {**self.manifest, extra: "malicious"}
            with self.subTest(extra=extra), self.assertRaises(ValueError):
                theme_packs.validate_manifest(invalid)

    def test_identifiers_cannot_escape_or_override_builtins(self):
        for identifier in ("../oops", "/tmp/oops", "x\\oops", "hiili", "graphite", "ubuntu", "plum", "petrol",
                           "ab", "Uppercase", "a" * 41, "äbc", "abc\n", "abc/def", 42):
            with self.subTest(identifier=identifier), self.assertRaises(ValueError):
                theme_packs.validate_manifest({**self.manifest, "id": identifier})

    def test_format_versions_types_and_metadata_bounds(self):
        invalid_values = {
            "format": ["other", 1, None], "version": [True, "1", 2, 1.0],
            "name": ["", " ", "a" * 81, "a\nb", "a\x00b", "a\u2028b", "a\u2029b", "\udfff", None],
            "description": ["a" * 601, []], "author": ["a" * 121],
            "license": ["", "a" * 129], "target": ["a" * 161],
            "accent": ["not-a-color", "Green", [], None],
            "sample": ["red", "#fff", "#012345;", "#01234g", None],
        }
        for field, values in invalid_values.items():
            for value in values:
                with self.subTest(field=field, value=repr(value)), self.assertRaises(ValueError):
                    theme_packs.validate_manifest({**self.manifest, field: value})
        with self.assertRaises(ValueError):
            theme_packs.validate_manifest({**self.manifest, 42: "bad key"})

    def test_color_keys_and_values_are_strict(self):
        for key in theme_packs.COLOR_KEYS:
            invalid = copy.deepcopy(self.manifest)
            del invalid["colors"][key]
            with self.subTest(missing_color=key), self.assertRaises(ValueError):
                theme_packs.validate_manifest(invalid)
        for value in ("#fff", "red", "#000000;url(x)", 0, None):
            invalid = copy.deepcopy(self.manifest)
            invalid["colors"]["glyph"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                theme_packs.validate_manifest(invalid)
        invalid = copy.deepcopy(self.manifest)
        invalid["colors"]["unexpected"] = "#ffffff"
        with self.assertRaises(ValueError):
            theme_packs.validate_manifest(invalid)

    def test_light_or_low_contrast_palette_is_rejected(self):
        for key in [item for item in theme_packs.COLOR_KEYS if item.startswith("#")] + ["accent_bg"]:
            invalid = copy.deepcopy(self.manifest)
            invalid["colors"][key] = "#ffffff"
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "kontrast"):
                theme_packs.validate_manifest(invalid)
        # Color samples and folder/glyph colors are previews/decorations rather
        # than the surfaces behind the manager's fixed body/button text.
        valid = copy.deepcopy(self.manifest)
        valid["sample"] = "#ffffff"
        valid["colors"]["glyph"] = "#ffffff"
        self.assertEqual(theme_packs.validate_manifest(valid)["sample"], "#ffffff")

    def test_invalid_json_duplicate_keys_and_nonfinite_values(self):
        valid = json.dumps(self.manifest)
        variants = [b"not JSON", b"\xff", b"[]", b"null", b"NaN",
                    (valid[:-1] + ', "name": "duplicate"}').encode(),
                    valid.replace('"glyph": "#c4ddca"', '"glyph": "#c4ddca", "glyph": "#ffffff"').encode(),
                    valid.replace('"version": 1', '"version": NaN').encode(),
                    b"[" * 2000 + b"]" * 2000]
        for index, data in enumerate(variants):
            path = self.base / f"invalid-{index}.json"
            path.write_bytes(data)
            with self.subTest(index=index):
                self.assert_rejected(path)

    def test_utf8_bom_is_accepted(self):
        path = self.write_json()
        path.write_bytes(b"\xef\xbb\xbf" + path.read_bytes())
        self.assertEqual(theme_packs.import_theme(path)[0], "user:metsayo")

    def test_large_manifest_and_archive_are_bounded(self):
        path = self.base / "large.json"
        path.write_bytes(b" " * (theme_packs.MAX_MANIFEST_BYTES + 1))
        self.assert_rejected(path)
        path = self.write_zip([("theme.json", " " * (theme_packs.MAX_MANIFEST_BYTES + 1))])
        self.assertLess(path.stat().st_size, 1024)  # compressed bomb stays tiny
        self.assert_rejected(path)
        path = self.base / "large.zip"
        path.write_bytes(b"x" * (theme_packs.MAX_ARCHIVE_BYTES + 1))
        self.assert_rejected(path)

    def test_archive_paths_duplicates_and_extra_files_are_rejected(self):
        manifest = json.dumps(self.manifest)
        for filename in ("../theme.json", "/theme.json", "folder/theme.json", "folder\\theme.json", "theme.json/", "THEME.JSON"):
            with self.subTest(filename=filename):
                self.assert_rejected(self.write_zip([(filename, manifest)]))
        for extra in ("theme.json", "folder/", "install.sh", "theme.desktop", "gtk.css", "image.svg"):
            with self.subTest(extra=extra):
                self.assert_rejected(self.write_zip([("theme.json", manifest), (extra, "untrusted")]))
        self.assert_rejected(self.write_zip([]))

    def test_symlink_and_other_special_archive_entries_are_rejected(self):
        for kind in (stat.S_IFLNK, stat.S_IFIFO, stat.S_IFDIR, stat.S_IFCHR, stat.S_IFSOCK):
            entry = zipfile.ZipInfo("theme.json")
            entry.create_system = 3
            entry.external_attr = (kind | 0o777) << 16
            with self.subTest(kind=kind):
                self.assert_rejected(self.write_zip([(entry, json.dumps(self.manifest))]))

    def test_executable_manifest_and_encrypted_archive_are_rejected(self):
        entry = zipfile.ZipInfo("theme.json")
        entry.create_system = 3
        entry.external_attr = (stat.S_IFREG | 0o755) << 16
        self.assert_rejected(self.write_zip([(entry, json.dumps(self.manifest))]))
        path = self.write_zip()
        data = bytearray(path.read_bytes())
        # Set the encryption flag in the local and central file headers.
        local = data.index(b"PK\x03\x04")
        central = data.index(b"PK\x01\x02")
        data[local + 6] |= 1
        data[central + 8] |= 1
        path.write_bytes(data)
        self.assert_rejected(path)

    def test_corrupted_and_unknown_file_types_are_rejected(self):
        path = self.base / "bad.zip"
        path.write_bytes(b"PK invalid archive")
        self.assert_rejected(path)
        self.assert_rejected(self.write_json(name="install.sh"))
        path = self.base / "pipe.json"
        os.mkfifo(path)
        self.assert_rejected(path)

    def test_catalog_ignores_invalid_partial_and_mismatched_entries(self):
        theme_packs.import_theme(self.write_json())
        (self.root / ".import-abc").mkdir()
        for identifier, content in (("invalid", b"{broken"), ("wrong-id", json.dumps(self.manifest).encode()),
                                    ("too-large", b" " * (theme_packs.MAX_MANIFEST_BYTES + 1))):
            directory = self.root / identifier
            directory.mkdir()
            (directory / "theme.json").write_bytes(content)
        (self.root / "linked-dir").symlink_to(self.root / "metsayo", target_is_directory=True)
        directory = self.root / "linked-file"
        directory.mkdir()
        (directory / "theme.json").symlink_to(self.root / "metsayo/theme.json")
        self.assertEqual(list(theme_packs.catalog()), ["user:metsayo"])

    def test_import_root_symlink_is_not_followed(self):
        destination = self.base / "elsewhere"
        destination.mkdir()
        self.root.parent.mkdir(parents=True)
        self.root.symlink_to(destination, target_is_directory=True)
        self.assert_rejected(self.write_json())
        self.assertEqual(list(destination.iterdir()), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
