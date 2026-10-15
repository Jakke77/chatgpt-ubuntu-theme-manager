"""Check the local text guard's intended coverage and false-positive limits."""

import copy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from content_policy import ContentPolicyError, POLICY_PROMPT, POLICY_SUMMARY, validate_content


class ContentPolicyTest(unittest.TestCase):
    def setUp(self):
        self.metadata = {
            "id": "metsayo", "name": "Metsäyö", "description": "Rauhallinen tumma metsä.",
            "author": "Matti O'Neill © 2026", "license": "GPL-3.0-or-later",
            "target": "Ubuntu 26.10 / GNOME 51",
        }

    def assert_rejected(self, text, category, field="description"):
        metadata = {**self.metadata, field: text}
        with self.assertRaises(ContentPolicyError) as caught:
            validate_content(metadata)
        message = str(caught.exception)
        self.assertIn(field, message)
        self.assertIn(category, message)
        self.assertNotIn(text, message)
        self.assertIsInstance(caught.exception, ValueError)

    def test_normal_theme_metadata_is_allowed_and_unchanged(self):
        before = copy.deepcopy(self.metadata)
        self.assertIsNone(validate_content(self.metadata))
        self.assertEqual(self.metadata, before)

    def test_ordinary_dark_identity_politics_and_religion_are_allowed(self):
        examples = (
            "Gothic skulls and dark horror", "Black metal", "White Night", "Pink clouds",
            "Rainbow LGBT Pride", "Trans identity expression", "Queer art",
            "Kristillinen metsä", "Islamic geometry", "Jewish heritage", "Buddhist temple",
            "Socialist red", "Conservative blue", "Nude figure art", "Artistic nudity",
            "Vampyyrit ja kallot", "Synkkä goottiyö", "Ubuntu Dark Edition",
            "Windows inspired blue", "ChatGPT community palette", "Al Gore green",
            "Sussex", "Pornainen", "Metsäyö", "Identiteetti", "Identity",
        )
        for text in examples:
            with self.subTest(text=text):
                self.assertIsNone(validate_content({**self.metadata, "name": text}))

    def test_non_latin_text_and_legitimate_joiners_are_not_blanket_banned(self):
        for text in ("夜の森", "غابة الليل", "לילה", "जंगल", "شب\u200cهای تاریک", "Ægir – Öinen metsä"):
            with self.subTest(text=text):
                self.assertIsNone(validate_content({**self.metadata, "author": text}))

    def test_fraud_credentials_and_impersonation(self):
        examples = (
            "Identity theft", "Phishing bank", "Credential stealer", "Steal passwords",
            "Harvest bank details", "Fake bank login", "Pretend to be the police",
            "Impersonate a real person", "Identiteettivarkaus", "Toisena esiintyminen",
            "Salasanojen varastaminen", "Pankkitunnuksia keräävä", "Väärennetty kirjautumissivu",
            "Esiinny poliisina", "Tietojenkalastelu",
        )
        for text in examples:
            with self.subTest(text=text):
                self.assert_rejected(text, "huijaus")

    def test_narrow_fraud_education_phrases_allowed(self):
        for text in (
            "Anti-phishing awareness", "Identity theft prevention", "Phishing education",
            "Identiteettivarkauden ehkäisy", "Tietojenkalastelun torjunta",
            "Against identity theft", "Preventing identity theft",
        ):
            with self.subTest(text=text):
                self.assertIsNone(validate_content({**self.metadata, "description": text}))
        self.assert_rejected("Identity theft prevention and steal passwords", "huijaus")

    def test_explicit_sexual_content_and_child_exploitation(self):
        for text in ("Pornography", "Porno", "Pornoteema", "Oral sex", "Explicit sexual acts", "Blowjob", "Suuseksi"):
            with self.subTest(text=text):
                self.assert_rejected(text, "pornografia")
        for text in ("Child porn", "CSAM", "Lolicon", "Lapsiporno", "Lasten seksuaalinen hyväksikäyttö"):
            with self.subTest(text=text):
                self.assert_rejected(text, "lasten hyväksikäyttö")

    def test_explicit_hate_violent_targeting_and_terrorist_praise(self):
        for text in (
            "White supremacy", "Ethnic cleansing", "Kill all immigrants", "Death to Jews",
            "Muslims must die", "Tappakaa kaikki homot", "Maahanmuuttajat pitää tuhota", "Neekeri",
        ):
            with self.subTest(text=text):
                self.assert_rejected(text, "vihasisältö")
        for text in ("Heil Hitler", "Glory to ISIS", "Support ISIS", "Praise Al Qaeda", "Liity Isisiin", "Eläköön ISIS"):
            with self.subTest(text=text):
                self.assert_rejected(text, "ihannointi")
        self.assertIsNone(validate_content({**self.metadata, "name": "Kill all demons"}))

    def test_graphic_violence_versus_ordinary_horror(self):
        for text in ("Graphic gore", "Dismembered bodies", "Mutilated corpses", "Silvotut ruumiit", "Raakaa väkivaltaa"):
            with self.subTest(text=text):
                self.assert_rejected(text, "raaka väkivalta")
        for text in ("Horror night", "Blood red", "Skulls", "Verikuu", "Zombie sunset"):
            with self.subTest(text=text):
                self.assertIsNone(validate_content({**self.metadata, "name": text}))

    def test_format_controls_accents_case_and_width_cannot_hide_known_phrase(self):
        for text, category in (
            ("PÓRNÓGRAPHY", "pornografia"),
            ("ｐｈｉｓｈｉｎｇ", "huijaus"),
            ("phish\u200bing", "huijaus"),
            ("id\u2060entity theft", "huijaus"),
            ("CREDENTIAL—STEALER", "huijaus"),
            ("credential_stealer", "huijaus"),
            ("TAPPÁKÁÁ KAIKKI HOMOT", "vihasisältö"),
        ):
            with self.subTest(text=text):
                self.assert_rejected(text, category)

    def test_links_and_message_style_markup_are_rejected(self):
        for text in (
            "https://example.invalid", "HTTP://example.invalid/login", "www.example.invalid",
            "mailto:account@example.invalid", "file:///tmp/fake", "javascript:alert(1)",
            "[Trusted support](https://example.invalid)", "[Click](login)", "[Click][trusted]",
            "<b>Official login</b>", "<span foreground='red'>Login</span>",
            "<!-- hidden HTML -->", "<!DOCTYPE html>", "<?xml version='1.0'?>",
            "[url=login]Support[/url]", "h\u200bttps://example.invalid",
        ):
            with self.subTest(text=text):
                self.assert_rejected(text, "linkki tai merkintäkieli")
        for text in ("Matti O'Neill © 2026", "GPL-3.0-or-later", "CC0-1.0", "A < B", "GNOME / Ubuntu"):
            with self.subTest(text=text):
                self.assertIsNone(validate_content({**self.metadata, "author": text}))

    def test_bidi_and_control_characters_cannot_impersonate_ui_messages(self):
        for character in ("\u202e", "\u2066", "\u2069", "\x1b", "\x00", "\n", "\u2028"):
            with self.subTest(character=repr(character)):
                self.assert_rejected("Trusted" + character + "text", "ohjausmerkki")

    def test_every_metadata_field_is_checked_without_echoing_offending_content(self):
        for field in self.metadata:
            with self.subTest(field=field):
                self.assert_rejected("credential-stealer", "huijaus", field=field)

    def test_guard_is_offline_and_does_not_change_data(self):
        original = copy.deepcopy(self.metadata)
        with patch("socket.socket", side_effect=AssertionError("network is forbidden")), \
             patch("urllib.request.urlopen", side_effect=AssertionError("network is forbidden")), \
             patch("builtins.open", side_effect=AssertionError("no files or logs")):
            self.assertIsNone(validate_content(self.metadata))
            self.assert_rejected("Fake bank login", "huijaus")
        self.assertEqual(self.metadata, original)

    def test_public_wording_explains_local_limit_and_allowed_identity_expression(self):
        self.assertIn("ei tunnista kaikkea", POLICY_SUMMARY)
        self.assertIn("identiteetti", POLICY_SUMMARY)
        self.assertIn("pelkkää tekstiä", POLICY_PROMPT)
        self.assertIn("lainmukaisuuden takeeksi", POLICY_PROMPT)

    def test_wrong_field_type_fails_closed_for_direct_callers(self):
        with self.assertRaises(ContentPolicyError):
            validate_content({**self.metadata, "name": ["not text"]})

    def test_partial_metadata_can_guard_the_prompt_target(self):
        self.assertIsNone(validate_content({"target": "Ubuntu 24.04 / GNOME 46"}))
        with self.assertRaises(ContentPolicyError):
            validate_content({"target": "Fake bank login"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
