#!/usr/bin/python3
"""Validate exported prompts, all palette styles and safe Debian upgrade hooks."""
from pathlib import Path
import json
import os
import re
import subprocess
import sys
import tempfile
from urllib.parse import urlparse, parse_qs
from xml.etree import ElementTree

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / "src"))
from palettes import PALETTES
from chatgpt_prompts import PROMPTS, build_prompt, chatgpt_url
from theme_packs import validate_manifest


def prompt_example(prompt):
    blocks = re.findall(r"```json\n(.*?)\n```", prompt, re.DOTALL)
    assert len(blocks) == 1, "Each prompt must include one complete manifest example"
    return validate_manifest(json.loads(blocks[0]))

for kind in PROMPTS:
    url = urlparse(chatgpt_url(kind))
    prompt = build_prompt(kind)
    assert url.scheme == "https" and url.netloc == "chatgpt.com"
    assert parse_qs(url.query)["q"] == [prompt]
    assert "Aloita nyt vain neljästä kysymyksestä ja odota vastauksiani." in prompt
    assert "/home/" not in prompt and "API_KEY" not in prompt
    manifest = prompt_example(prompt)
    assert manifest["format"] == "chatgpt-ubuntu-theme" and manifest["version"] == 1
    assert ".ctm-theme.zip" in prompt and "tasan yksi UTF-8-tiedosto nimeltä theme.json" in prompt
    assert "Manageri hyväksyy myös JSON-tiedoston" in prompt
    # The formats are named to forbid them, so mere word-absence checks would
    # wrongly fail a good prompt and miss an instruction to build a launcher.
    assert "Älä toimita .deb-asentajaa, .desktop-tiedostoa, omaa sovelluskuvaketta valikkoon" in prompt
    assert "Älä anna sudo-komentoja" in prompt
    assert "TOIMITA TEEMA NYKYISEEN MANAGERIIN, älä tee erillistä sovellusta" in prompt
    assert "#e3e8ec-leipätekstin kontrastin jokaista seitsemää" in prompt
    assert "Manageri tarkistaa nämä kontrastit tuonnissa" in prompt
    exported = BASE / "package/usr/share/hiili-theme/prompts" / (kind + ".txt")
    assert exported.read_text().rstrip() == prompt
    custom_target = "Ubuntu 24.04, GNOME 46"
    custom_prompt = build_prompt(kind, target=custom_target)
    custom_url = urlparse(chatgpt_url(kind, target=custom_target))
    assert parse_qs(custom_url.query)["q"] == [custom_prompt]
    assert prompt_example(custom_prompt)["target"] == custom_target
    assert f"Kohdeympäristön lähtötieto: {custom_target}." in custom_prompt
    assert "26.10" not in custom_prompt, "A chosen target must replace the local Ubuntu version"
    assert "Se on ohjetieto, ei väite testatusta yhteensopivuudesta" in custom_prompt
    assert "Älä lupaa testaamatonta toimivuutta" in custom_prompt
print("PASS: all three interview prompts export valid importable manifests, configurable targets, and matching browser URLs")

for selected in PALETTES.values():
    root = BASE / "package/usr/share/icons" / selected["theme"]
    for path in root.rglob("*"):
        if path.is_symlink():
            assert path.exists(), path
        elif path.suffix == ".svg":
            ElementTree.parse(path)
print("PASS: SVG artwork and icon aliases for all five themes")

fixture = max((BASE / "tests").glob("hiili-integration-*"), key=lambda p: p.stat().st_mtime)
themes = [fixture / "share/themes" / item["theme"] for item in PALETTES.values()]
themes.append(fixture / "share/themes/Hiili-User-metsayo")
custom_css = list((fixture / "share/hiili-theme/generated").glob("metsayo-*/gtk4.css"))
assert len(custom_css) == 1
for gtk_version in ("3.0", "4.0"):
    paths = [str(path / "gtk-3.0/gtk.css") for path in themes] if gtk_version == "3.0" else [str(BASE / "package/usr/share/hiili-theme/variants" / key / "gtk4.css") for key in PALETTES]
    if gtk_version == "4.0":
        paths += [str(path) for path in custom_css]
    reader = '''import gi, json, sys
gi.require_version("Gtk", sys.argv[1])
from gi.repository import Gtk
errors=[]
provider=Gtk.CssProvider()
provider.connect("parsing-error",lambda obj,section,error:errors.append(str(error)))
for path in json.loads(sys.argv[2]): provider.load_from_path(path)
assert not errors, errors
'''
    subprocess.run([sys.executable, "-c", reader, gtk_version, json.dumps(paths)], check=True)
print("PASS: full GTK 3 themes and GTK 4 CSS for five built-ins and the imported palette")

env = dict(os.environ, GI_TYPELIB_PATH="/usr/lib/gnome-shell:/usr/lib/x86_64-linux-gnu/mutter-51", LD_LIBRARY_PATH="/usr/lib/gnome-shell:/usr/lib/x86_64-linux-gnu/mutter-51")
reader = '''import gi, sys, json
gi.require_version("St","51")
from gi.repository import St,Gio
for path in json.loads(sys.argv[1]):
    theme=St.Theme()
    assert theme.load_stylesheet(Gio.File.new_for_path(path)),path
'''
subprocess.run([sys.executable,"-c",reader,json.dumps([str(path / "gnome-shell/gnome-shell.css") for path in themes])],env=env,check=True)
print("PASS: GNOME 51 accepts all five built-in and the imported full Shell stylesheets")

fixture = Path(tempfile.mkdtemp(prefix="manager-hooks-", dir=BASE / "tests"))
log = fixture / "hooks.log"
for command in ("gtk-update-icon-cache", "update-desktop-database", "python3"):
    stub = fixture / command
    stub.write_text('#!/bin/sh\nprintf "%s\\n" "$0 $*" >> "$THEME_HOOK_LOG"\n')
    stub.chmod(0o755)
env = {"PATH":str(fixture),"THEME_HOOK_LOG":str(log)}
postinst = BASE / "package/DEBIAN/postinst"
subprocess.run(["/bin/sh",str(postinst),"configure","1.0.0"],env=env,check=True)
assert "session_apply" not in log.read_text(), "Upgrade must preserve the selected appearance"
subprocess.run(["/bin/sh",str(postinst),"configure"],env=env,check=True)
assert log.read_text().count("session_apply") == 1, "Fresh install must apply the default theme"
print("PASS: fresh install activates the theme; upgrade preserves the current appearance")
