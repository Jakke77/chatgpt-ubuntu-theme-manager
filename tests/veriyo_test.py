"""Check the shipped Veriyö assets and wallpaper selection without desktop writes."""
from pathlib import Path
import json
import sys
import unittest
from unittest.mock import patch
from xml.etree import ElementTree

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / 'src'))
import engine
from palettes import PALETTES, recolor, variant_for_theme
from theme_packs import _read_source, validate_manifest


class VeriyoTests(unittest.TestCase):
    def test_old_manager_import_has_valid_contrast_and_same_colors(self):
        manifest = validate_manifest(json.loads((BASE / 'examples/Veriyo.theme.json').read_text()))
        self.assertEqual(_read_source(BASE / 'examples/Veriyo.ctm-theme.zip'), manifest)
        self.assertEqual(manifest['colors'], PALETTES['veriyo']['colors'])
        self.assertEqual(variant_for_theme('Hiili-Veriyo'), 'veriyo')
        with self.assertRaises(ValueError):
            validate_manifest({**manifest, 'id': 'veriyo'})

    def test_original_wallpapers_are_shipped_unchanged(self):
        target = BASE / 'package/usr/share/hiili-theme/variants/veriyo'
        for image in (BASE / 'assets/veriyo').glob('*.png'):
            self.assertEqual((target / image.name).read_bytes(), image.read_bytes())
            self.assertTrue(image.read_bytes().startswith(b'\x89PNG\r\n\x1a\n'))
        for css in ('gtk3.css', 'gtk4.css', 'shell.css'):
            self.assertEqual((target / css).read_text(), recolor((BASE / 'src' / css).read_text(), 'veriyo'))
        icons = BASE / 'package/usr/share/icons/Hiili-Veriyo'
        for image in icons.rglob('*.svg'):
            ElementTree.parse(image)
        self.assertIn('#f5eaf0', (icons / 'scalable/apps/browser.svg').read_text())

    def test_wallpaper_opt_in_uses_bundled_otava_and_both_background_keys(self):
        with patch.object(engine, 'DATA', BASE / 'package/usr/share/hiili-theme'):
            expected = (engine.DATA / 'variants/veriyo/veriyo-otava.png').as_uri()
            targets = engine.theme_targets(True, 'veriyo')
            backgrounds = {key: value for schema, key, value in targets
                           if schema == 'org.gnome.desktop.background'}
            self.assertEqual(backgrounds['picture-uri'], expected)
            self.assertEqual(backgrounds['picture-uri-dark'], expected)
            self.assertEqual(backgrounds['primary-color'], '#070508')
            self.assertFalse(any(schema == 'org.gnome.desktop.background'
                                 for schema, _, _ in engine.theme_targets(False, 'veriyo')))
            old = engine.theme_targets(True, 'hiili')
            self.assertTrue(any(key == 'picture-uri' and value.endswith('/hiili/wallpaper.svg')
                                for _, key, value in old))


if __name__ == '__main__':
    unittest.main(verbosity=2)
