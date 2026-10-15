#!/usr/bin/python3
"""Exercise real GUI signals on a private desktop; stub only the external URL."""
from pathlib import Path
import importlib.machinery
import json
import os
import sys
import traceback
import zipfile
from types import SimpleNamespace
from urllib.parse import urlparse, parse_qs
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio, GLib, Gdk

BASE = Path(__file__).resolve().parents[1]
APP_LIB = Path(os.environ.get("THEME_MANAGER_TEST_LIB", BASE / "src"))
sys.path.insert(0, str(APP_LIB))
import engine
from chatgpt_prompts import build_prompt
from theme_packs import example_manifest
from content_policy import ContentPolicyError
from system_info import format_system_info, system_target

result_file = Path(sys.argv[1])
original_theme = engine.settings("org.gnome.desktop.interface").get_string("gtk-theme")
captured = []
Gio.AppInfo.launch_default_for_uri = lambda uri, context: captured.append(uri) or True
module = importlib.machinery.SourceFileLoader("manager_gui", str(APP_LIB / "hiili-theme")).load_module()
stage = 0
application = None


def report(error=None):
    result_file.write_text(json.dumps({"ok": error is None, "error": error}, ensure_ascii=False))


def step():
    global stage, application
    try:
        if application is None:
            windows = Gtk.Window.get_toplevels()
            if not windows.get_n_items():
                return True
            application = windows.get_item(0).get_application()
        if stage == 0:
            about = application.show_about()
            assert about.get_application_name() == "ChatGPT Ubuntu Theme Manager"
            about.close()
            policy = application.show_policy()
            assert policy.get_heading() == "Yleiskäyttöön sopivat teemat"
            policy.close()
            invalid = result_file.parent / "invalid-theme.json"
            metadata = example_manifest()
            metadata["name"] = "Explicit pornography"
            invalid.write_text(json.dumps(metadata))
            try:
                application.import_from_path(invalid)
            except ContentPolicyError:
                pass
            else:
                raise AssertionError("GUI import accepted rejected metadata")
            assert len(application.theme_buttons) == 5
            errors = []
            original_policy_error = application.policy_error
            application.policy_error = lambda error: errors.append(error)
            application.prompt_target.set_text("Identity theft and steal passwords")
            application.chatgpt_button.emit("clicked")
            assert len(errors) == 1 and not captured, "Unsafe target opened the browser"
            application.policy_error = original_policy_error
            application.prompt_target.set_text("Ubuntu 26.10 / GNOME 51")
            download = result_file.parent / "metsayo.ctm-theme.zip"
            with zipfile.ZipFile(download, "w", zipfile.ZIP_DEFLATED) as archive:
                archive.writestr("theme.json", json.dumps(example_manifest(), ensure_ascii=False))
            # Exercise the import button and file-dialog completion; stub only
            # the system file picker, just as the external browser is stubbed.
            original_open = Gtk.FileDialog.open
            def select_download(chooser, parent, cancellable, callback):
                assert chooser.get_default_filter().get_name().startswith("Managerin teemat")
                callback(SimpleNamespace(open_finish=lambda result: Gio.File.new_for_path(str(download))), None)
            Gtk.FileDialog.open = select_download
            application.import_button.emit("clicked")
            Gtk.FileDialog.open = original_open
            assert application.selected == "user:metsayo"
            assert "user:metsayo" in application.theme_buttons
            assert engine.status()["variant"] != "user:metsayo", "Import changed the desktop"
            assert not (engine.SHARE / "applications").exists()
            application.apply_button.emit("clicked")
            stage = 10
        elif stage == 10 and application.apply_button.get_sensitive():
            assert engine.status()["variant"] == "user:metsayo", engine.status()
            assert engine.variant_data("user:metsayo").is_dir()
            application.theme_buttons["plum"].set_active(True)
            assert engine.settings("org.gnome.desktop.interface").get_string("gtk-theme") == "Hiili-User-metsayo", "Preview changed the system theme"
            application.apply_button.emit("clicked")
            stage = 1
        elif stage == 1 and application.apply_button.get_sensitive():
            assert engine.status()["variant"] == "plum", engine.status()
            application.theme_buttons["ubuntu"].set_active(True)
            application.apply_button.emit("clicked")
            stage = 2
        elif stage == 2 and application.apply_button.get_sensitive():
            assert engine.status()["variant"] == "ubuntu", engine.status()
            application.prompt_choice.set_selected(1)
            application.detect_button.emit("clicked")
            assert not application.detect_button.get_sensitive()
            stage = 20
        elif stage == 20 and application.detect_button.get_sensitive():
            assert application.system_details is not None
            assert application.system_report_box.get_visible()
            report_text = format_system_info(application.system_details)
            assert application.system_report.get_text() == report_text
            assert application.prompt_target.get_text() == system_target(application.system_details)
            assert "GTK 4:" in report_text and "libadwaita:" in report_text and "Istunto:" in report_text
            assert "Yaru GNOME Shell:" in report_text
            assert "/home/" not in report_text
            application.copy_system_button.emit("clicked")
            def check_system_clipboard(clipboard, result):
                global stage
                try:
                    assert clipboard.read_text_finish(result) == report_text
                    stage = 21
                except Exception:
                    report_error = traceback.format_exc()
                    result_file.write_text(json.dumps({"ok": False, "error": report_error}))
            Gdk.Display.get_default().get_clipboard().read_text_async(None, check_system_clipboard)
            stage = 22
        elif stage == 21:
            application.chatgpt_button.emit("clicked")
            assert len(captured) == 1
            url = urlparse(captured[0])
            assert url.scheme == "https" and url.netloc == "chatgpt.com"
            expected = build_prompt("variant", application.prompt_target.get_text(), application.system_details)
            assert parse_qs(url.query)["q"] == [expected]
            assert format_system_info(application.system_details) in expected
            def check_prompt_clipboard(clipboard, result):
                global stage
                try:
                    assert clipboard.read_text_finish(result) == expected
                    stage = 23
                except Exception:
                    report(traceback.format_exc())
            Gdk.Display.get_default().get_clipboard().read_text_async(None, check_prompt_clipboard)
            stage = 24
        elif stage == 23:
            application.prompt_target.set_text("Ubuntu 24.04 / GNOME 46")
            assert application.system_details_for_prompt() is None
            assert "ei liitetä" in application.system_report_hint.get_text()
            application.chatgpt_button.emit("clicked")
            assert len(captured) == 2
            expected = build_prompt("variant", "Ubuntu 24.04 / GNOME 46")
            assert parse_qs(urlparse(captured[-1]).query)["q"] == [expected]
            assert "Koneelta haetut teeman yhteensopivuustiedot" not in expected
            application.detect_button.emit("clicked")
            stage = 25
        elif stage == 25 and application.detect_button.get_sensitive():
            assert application.prompt_target.get_text() == system_target(application.system_details)
            assert application.system_details_for_prompt() is not None
            application.restore_button.emit("clicked")
            stage = 4
        elif stage == 4 and application.apply_button.get_sensitive():
            assert engine.settings("org.gnome.desktop.interface").get_string("gtk-theme") == original_theme
            assert not engine.status()["backup_available"]
            application.theme_buttons["user:metsayo"].set_active(True)
            report()
            return False
        return True
    except Exception:
        report(traceback.format_exc())
        return False


GLib.timeout_add(120, step)
sys.exit(module.gui())
