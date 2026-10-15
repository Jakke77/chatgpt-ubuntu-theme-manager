"""Private, deterministic checks for the public software-version report."""

import io
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import system_info


class SystemInfoTest(unittest.TestCase):
    def os_release(self, text):
        return patch("system_info.Path.open", return_value=io.StringIO(text))

    def test_full_public_report_and_one_fixed_package_query(self):
        output = "\n".join((
            "gnome-shell\t1:51.0-1ubuntu1", "libgtk-4-1:amd64\t4.24.0+ds-1ubuntu2",
            "libadwaita-1-0\t1.10.0-1ubuntu1", "yaru-theme-gtk\t26.10.2-0ubuntu1",
            "yaru-theme-gnome-shell\t26.10.2-0ubuntu1", "yaru-theme-icon\t26.10.2-0ubuntu1",
        ))
        with self.os_release('PRETTY_NAME="Ubuntu 26.10"\nHOME_URL="https://ubuntu.com/"\n'), \
                patch("system_info.subprocess.run", return_value=SimpleNamespace(stdout=output, returncode=0)) as run, \
                patch.dict("os.environ", {"XDG_SESSION_TYPE": "wayland", "USER": "private-user", "HOSTNAME": "private-host"}):
            report = system_info.collect_system_info()
        self.assertEqual(tuple(report), system_info.KEYS)
        self.assertEqual(report["distribution"], "Ubuntu 26.10")
        self.assertEqual(report["gnome"], "51.0")
        self.assertEqual(report["gtk"], "4.24.0")
        self.assertEqual(report["libadwaita"], "1.10.0")
        self.assertEqual(report["yaru_icons"], "26.10.2-0ubuntu1")
        self.assertEqual(report["session"], "Wayland")
        from palettes import VERSION
        self.assertEqual(report["manager"], VERSION)
        run.assert_called_once()
        args, options = run.call_args
        self.assertEqual(args[0], ["dpkg-query", "--show", "--showformat=${Package}\t${Version}\n", *system_info.PACKAGES])
        self.assertEqual(options["timeout"], 3)
        self.assertNotIn("shell", options)
        self.assertEqual(options["env"], {"PATH": "/usr/bin:/bin", "LC_ALL": "C"})
        text = system_info.format_system_info(report)
        self.assertNotIn("private-user", text)
        self.assertNotIn("private-host", text)
        self.assertNotIn("https", text)

    def test_partial_package_query_failure_keeps_installed_versions(self):
        with patch("system_info.subprocess.run", return_value=SimpleNamespace(
            stdout="gnome-shell\t51.0-1\nlibgtk-4-1\t4.24.0-1\n", returncode=1)):
            report = system_info.validate_system_info(system_info._package_versions())
        self.assertEqual(report["gnome"], "51.0")
        self.assertEqual(report["gtk"], "4.24.0")
        self.assertEqual(report["libadwaita"], system_info.UNKNOWN)

    def test_missing_tools_and_timeout_return_unknown(self):
        for error in (FileNotFoundError("private/path"), subprocess.TimeoutExpired("dpkg-query", 3, output="private-host")):
            with self.subTest(error=type(error).__name__), \
                    patch("system_info.Path.open", side_effect=FileNotFoundError()), \
                    patch("system_info.subprocess.run", side_effect=error), \
                    patch.dict("os.environ", {"XDG_SESSION_TYPE": "private-host"}):
                report = system_info.collect_system_info()
            self.assertEqual(report["distribution"], system_info.UNKNOWN)
            self.assertEqual(report["gnome"], system_info.UNKNOWN)
            self.assertEqual(report["session"], system_info.UNKNOWN)
            self.assertNotIn("private", system_info.format_system_info(report))

    def test_distribution_fallback_and_ordinary_names(self):
        examples = (
            ('ID=ubuntu\nVERSION_ID="26.04"\n', "ubuntu 26.04"),
            ('NAME="Ubuntu"\nVERSION_ID="26.10"\n', "Ubuntu 26.10"),
            ('PRETTY_NAME="Debian GNU/Linux 13 (trixie)"\n', "Debian GNU/Linux 13 (trixie)"),
            ('PRETTY_NAME="broken\nNAME="Ubuntu"\nVERSION_ID=26.10\n', "Ubuntu 26.10"),
        )
        for text, expected in examples:
            with self.subTest(text=text), self.os_release(text):
                self.assertEqual(system_info._distribution(), expected)

    def test_bounded_os_release_and_package_output(self):
        with self.os_release("x" * 16385):
            self.assertEqual(system_info._distribution(), system_info.UNKNOWN)
        with patch("system_info.subprocess.run", return_value=SimpleNamespace(stdout="x" * 16385, returncode=0)):
            self.assertEqual(system_info._package_versions(), {})

    def test_untrusted_distribution_uses_safe_fallback(self):
        for value in ("https://private.example", "/home/private-user", "private-host.local", "$(hostname)", "Ubuntu\u200b26.10"):
            with self.subTest(value=value), self.os_release(f'PRETTY_NAME="{value}"\nID=ubuntu\nVERSION_ID=26.10\n'):
                self.assertEqual(system_info._distribution(), "ubuntu 26.10")

    def test_malformed_or_private_package_outputs_are_ignored(self):
        output = "\n".join((
            "hostname\tprivate-host", "gnome-shell\thttps://private.example", "libgtk-4-1\t/home/private",
            "libadwaita-1-0\t1.10.0-1\textra", "yaru-theme-icon\t26.10\u200bprivate", "yaru-theme-gtk\t26.10-1",
        ))
        with patch("system_info.subprocess.run", return_value=SimpleNamespace(stdout=output, returncode=0)):
            self.assertEqual(system_info._package_versions(), {"yaru_gtk": "26.10-1"})

    def test_validation_rejects_extra_fields_and_preserves_input(self):
        info = {"distribution": "Ubuntu 26.10", "gnome": "51.0", "session": "X11"}
        before = info.copy()
        validated = system_info.validate_system_info(info)
        self.assertEqual(info, before)
        self.assertEqual(validated["gtk"], system_info.UNKNOWN)
        for invalid in (None, [], {"hostname": "private-host"}, {"gtk": 4.24}, {"session": "tty"}):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                system_info.validate_system_info(invalid)

    def test_validation_rejects_controls_urls_paths_and_injection(self):
        values = ("51.0\nHOSTNAME=private", "51.0\x00", "/home/private", "https://private.example", "51.0; uname", "$(hostname)")
        for value in values:
            with self.subTest(value=value), self.assertRaises(ValueError):
                system_info.validate_system_info({"gnome": value})

    def test_exact_report_format_and_short_target(self):
        info = {"distribution": "Ubuntu 26.10", "gnome": "51.0", "gtk": "4.24.0", "libadwaita": "1.10.0", "session": "Wayland", "manager": "1.2.2"}
        self.assertEqual(system_info.format_system_info(info), "\n".join((
            "Käyttöjärjestelmä: Ubuntu 26.10", "GNOME Shell: 51.0", "GTK 4: 4.24.0", "libadwaita: 1.10.0",
            "Istunto: Wayland", "Yaru GTK: Tuntematon", "Yaru GNOME Shell: Tuntematon",
            "Yaru-kuvakkeet: Tuntematon", "Teemamanageri: 1.2.2",
        )))
        self.assertEqual(system_info.system_target(info), "Ubuntu 26.10, GNOME 51.0")
        self.assertEqual(system_info.system_target({"distribution": "Ubuntu 24.04"}), "Ubuntu 24.04; GNOME-versio tuntematon")
        with patch("system_info.collect_system_info", return_value=info) as collect:
            self.assertEqual(system_info.system_target(), "Ubuntu 26.10, GNOME 51.0")
        collect.assert_called_once_with()

    def test_full_prompt_keeps_report_but_browser_url_contains_no_prompt_data(self):
        from chatgpt_prompts import PROMPTS, build_prompt, chatgpt_url
        report = system_info.validate_system_info({"distribution": "Ubuntu 26.10", "gnome": "51.0",
                                                   "gtk": "4.24.1", "libadwaita": "1.10.0", "session": "Wayland"})
        target = system_info.system_target(report)
        text = system_info.format_system_info(report)
        for kind in PROMPTS:
            with self.subTest(kind=kind):
                prompt = build_prompt(kind, target, report)
                self.assertIn(text, prompt)
                url = chatgpt_url(kind, target, report)
                self.assertEqual(url, "https://chatgpt.com/")
                self.assertEqual(urlparse(url).query, "")
                self.assertEqual(urlparse(url).fragment, "")
                self.assertIn("älä arvaa puuttuvia versioita", prompt)
                self.assertNotIn("/home/", prompt)

    def test_clean_browser_url_does_not_include_custom_target_for_any_prompt(self):
        from chatgpt_prompts import PROMPTS, build_prompt, chatgpt_url
        for kind in PROMPTS:
            with self.subTest(kind=kind):
                target = "Ubuntu 24.04 / GNOME 46"
                self.assertIn(target, build_prompt(kind, target))
                self.assertEqual(chatgpt_url(kind, target), "https://chatgpt.com/")

    def test_every_prompt_prefers_the_web_chat_default_language(self):
        from chatgpt_prompts import LANGUAGE_INSTRUCTION, PROMPTS, build_prompt
        for kind in PROMPTS:
            with self.subTest(kind=kind):
                prompt = build_prompt(kind, "Ubuntu 26.10 / GNOME 51")
                self.assertIn(LANGUAGE_INSTRUCTION, prompt)
                self.assertNotIn("Keskustele kanssani suomeksi", prompt)
                self.assertNotIn("suomenkielinen", prompt)
                # Language comes from the web conversation, not private local
                # account information appended to this public version report.
                self.assertNotIn("LANG=", prompt)
                self.assertNotIn("LC_ALL=", prompt)
                self.assertNotIn("HOSTNAME=", prompt)
                self.assertNotIn("/home/", prompt)

    def test_prompt_without_report_preserves_a_different_target(self):
        from chatgpt_prompts import build_prompt
        prompt = build_prompt(target="Ubuntu 24.04 / GNOME 46")
        self.assertIn("Ubuntu 24.04 / GNOME 46", prompt)
        self.assertNotIn("Koneelta haetut teeman yhteensopivuustiedot", prompt)
        self.assertNotIn("26.10", prompt)

    def test_report_cannot_add_private_fields_or_bypass_content_checks(self):
        from chatgpt_prompts import build_prompt, chatgpt_url
        from content_policy import ContentPolicyError
        for factory in (build_prompt, chatgpt_url):
            with self.subTest(factory=factory.__name__), self.assertRaises(ValueError):
                factory(system_details={"hostname": "private-host"})
            with self.subTest(factory=factory.__name__), self.assertRaises(ContentPolicyError):
                factory(target="Ubuntu 26.10", system_details={"distribution": "Identity theft"})


if __name__ == "__main__":
    unittest.main()
