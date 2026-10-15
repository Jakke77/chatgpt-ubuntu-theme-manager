#!/usr/bin/python3
"""Build the click-installable Hiili theme, including original SVG icon art."""
from pathlib import Path
import os
import hashlib
import shutil
import subprocess
import textwrap
import sys

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE / "src"))
from palettes import PALETTES, VERSION, APP_NAME, recolor
from chatgpt_prompts import PROMPTS, build_prompt
ROOT = BASE / "package"
OUTPUT = Path(os.environ.get("THEME_MANAGER_OUTPUT", str(BASE / "dist")))
DATA = ROOT / "usr/share/hiili-theme"
ICONS = ROOT / "usr/share/icons/Hiili"


def write(path, content, executable=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip())
    path.chmod(0o755 if executable else 0o644)


def svg(body, defs="", size=64):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 64 64"><defs>{defs}</defs>{body}</svg>\n'


def tile(glyph, accent="#aac2cb"):
    return svg('<rect x="5" y="6" width="54" height="54" rx="16" fill="#030507" opacity=".4"/>'
               '<rect x="5" y="4" width="54" height="54" rx="16" fill="url(#tile)" stroke="#40505e" stroke-width="1.25"/>'
               '<path d="M20 5h24" stroke="#788996" stroke-opacity=".3"/>'
               f'<g fill="none" stroke="{accent}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">{glyph}</g>',
               '<linearGradient id="tile" x2=".5" y2="1"><stop stop-color="#2d3744"/><stop offset="1" stop-color="#151c25"/></linearGradient>')


def folder(glyph=""):
    return svg('<path d="M6 17a5 5 0 0 1 5-5h14l6 6h22a5 5 0 0 1 5 5v28a5 5 0 0 1-5 5H11a5 5 0 0 1-5-5z" fill="#17262e" stroke="#4c6672" stroke-width="1.3"/>'
               '<path d="M6 26h52v25a5 5 0 0 1-5 5H11a5 5 0 0 1-5-5z" fill="url(#folder)" stroke="#526c76" stroke-width="1.3"/>'
               '<path d="M10 28h44" stroke="#849fa7" stroke-opacity=".5"/>'
               f'<g fill="none" stroke="#adc7ce" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">{glyph}</g>',
               '<linearGradient id="folder" x2=".3" y2="1"><stop stop-color="#334c58"/><stop offset="1" stop-color="#1c303c"/></linearGradient>')


def generate_icons():
    glyphs = {
        "browser": '<circle cx="32" cy="31" r="16"/><ellipse cx="32" cy="31" rx="7" ry="16"/><path d="M17 25h30M17 37h30"/>',
        "terminal": '<rect x="14" y="17" width="36" height="29" rx="4"/><path d="m21 25 7 6-7 6M33 38h10"/>',
        "files": '<path d="M14 24v19a4 4 0 0 0 4 4h28a4 4 0 0 0 4-4V26a4 4 0 0 0-4-4H33l-5-6H18a4 4 0 0 0-4 4v4z"/><path d="M15 28h34"/>',
        "settings": '<circle cx="32" cy="31" r="7"/><path d="m29 15 6 0 2 5 5 3 5-1 3 6-4 4-1 5 2 5-5 4-5-2-5 1-4 3-6-3 0-5-3-4-5-2 0-7 5-2 3-4z"/>',
        "music": '<path d="M26 42V20l20-4v22M26 25l20-4"/><ellipse cx="21" cy="42" rx="5" ry="4"/><ellipse cx="41" cy="38" rx="5" ry="4"/>',
        "video": '<rect x="13" y="17" width="38" height="29" rx="5"/><path d="m28 24 12 8-12 8z"/>',
        "code": '<path d="m24 23-10 9 10 9m16-18 10 9-10 9m-5-24-6 30"/>',
        "text": '<path d="M21 13h17l9 10v26H21zM38 13v11h9M27 31h14M27 37h14M27 43h9"/>',
        "image": '<rect x="14" y="16" width="36" height="31" rx="4"/><circle cx="25" cy="26" r="4"/><path d="m15 42 12-11 8 8 6-6 8 9"/>',
        "mail": '<rect x="13" y="19" width="38" height="27" rx="4"/><path d="m15 22 17 13 17-13"/>',
        "calendar": '<rect x="15" y="18" width="34" height="30" rx="5"/><path d="M24 14v8m16-8v8M15 28h34M24 35h3m10 0h3m-16 7h3m10 0h3"/>',
        "clock": '<circle cx="32" cy="31" r="17"/><path d="M32 20v12l8 5"/>',
        "calculator": '<rect x="19" y="12" width="27" height="39" rx="5"/><path d="M25 20h15M25 28h2m11 0h2m-15 8h2m11 0h2m-15 8h2m11 0h2"/>',
        "software": '<path d="M17 24h30l3 24H14zM25 24v-5a7 7 0 0 1 14 0v5M26 36h12M32 30v12"/>',
        "monitor": '<rect x="12" y="15" width="40" height="28" rx="4"/><path d="M32 43v7m-9 0h18M17 34h7l4-10 6 13 5-7h8"/>',
        "chat": '<path d="M14 16h36v26H31l-10 8v-8h-7zM23 26h18M23 33h13"/>',
        "game": '<path d="M23 23h18c5 0 10 12 10 20 0 6-7 5-12-2H25c-5 7-12 8-12 2 0-8 5-20 10-20zM20 29v10m-5-5h10M39 30h1m5 6h1"/>',
        "cloud": '<path d="M21 44a10 10 0 0 1-2-20 14 14 0 0 1 27 4 8 8 0 0 1-1 16zM27 35l5-5 5 5M32 30v15"/>',
        "office": '<path d="M21 13h17l9 10v26H21zM38 13v11h9M28 32h12m-12 7h12m-12 6h7"/>',
        "extension": '<path d="M17 20h12a5 5 0 1 1 10 0h8v10a5 5 0 1 0 0 10v8H36a5 5 0 1 0-10 0h-9V37a5 5 0 1 0 0-10z"/>',
        "weather": '<path d="M23 43a9 9 0 0 1 0-18 12 12 0 0 1 23 4 7 7 0 0 1-1 14zM31 17v-4m-12 8-3-3m28 1 3-3"/>',
        "hiili": '<path d="m32 12 18 11-18 11-18-11zM14 32l18 11 18-11M14 41l18 11 18-11"/>',
    }
    aliases = {
        "browser": ["web-browser", "firefox", "firefox-esr", "google-chrome", "com.google.Chrome", "chromium", "chromium-browser", "org.gnome.Epiphany", "brave-browser"],
        "terminal": ["utilities-terminal", "org.gnome.Terminal", "org.gnome.Console", "org.gnome.Ptyxis", "ptyxis", "konsole"],
        "files": ["system-file-manager", "org.gnome.Nautilus", "nautilus", "file-manager"],
        "settings": ["org.gnome.Settings", "preferences-system", "preferences-desktop", "org.gnome.tweaks"],
        "music": ["multimedia-player", "org.gnome.Music", "rhythmbox", "spotify", "com.spotify.Client", "audacious"],
        "video": ["vlc", "org.videolan.VLC", "org.gnome.Totem", "totem", "mpv", "io.github.celluloid_player.Celluloid"],
        "code": ["code", "visual-studio-code", "vscode", "com.visualstudio.code", "codex", "com.openai.codex", "com.openai.Codex"],
        "text": ["org.gnome.TextEditor", "org.gnome.gedit", "gedit", "accessories-text-editor"],
        "image": ["org.gnome.Loupe", "org.gnome.eog", "org.gnome.Shotwell", "org.gnome.Photos", "gimp", "org.gimp.GIMP"],
        "mail": ["thunderbird", "org.mozilla.Thunderbird", "org.gnome.Geary", "org.gnome.Evolution"],
        "calendar": ["org.gnome.Calendar", "x-office-calendar", "tahtiaika"],
        "clock": ["org.gnome.clocks", "preferences-system-time", "tahtiaika-widget"],
        "calculator": ["org.gnome.Calculator", "accessories-calculator"],
        "software": ["org.gnome.Software", "snap-store", "snap-store_snap-store", "system-software-install", "system-software-update"],
        "monitor": ["org.gnome.SystemMonitor", "utilities-system-monitor", "org.gnome.baobab", "org.gnome.DiskUtility", "gparted"],
        "chat": ["chatgpt", "com.openai.ChatGPT", "telegram", "org.telegram.desktop", "discord", "signal-desktop"],
        "game": ["steam", "net.lutris.Lutris", "applications-games"],
        "cloud": ["org.gnome.DejaDup", "drive-cloud", "folder-cloud"],
        "office": ["libreoffice-startcenter", "libreoffice-writer", "libreoffice-calc", "libreoffice-impress", "libreoffice-draw", "org.gnome.Papers", "org.gnome.Evince"],
        "extension": ["com.mattjakeman.ExtensionManager", "org.gnome.Shell.Extensions", "applications-utilities"],
        "weather": ["org.gnome.Weather", "tahtisaa", "varjosaa"],
        "hiili": ["hiili-theme", "fi.hiili.Theme"],
    }
    for index, (name, glyph) in enumerate(glyphs.items()):
        accent = ("#a9c4ca", "#bcc2d1", "#c0afc4", "#afc3b8")[index % 4]
        content = tile(glyph, accent)
        target = ICONS / "scalable/apps" / f"{name}.svg"
        write(target, content)
        write(DATA / "icon-preview" / f"{name}.svg", content)
        for alias in aliases[name]:
            if alias != name:
                path = target.with_name(alias + ".svg")
                if not path.exists():
                    path.symlink_to(target.name)
    folder_glyphs = {
        "folder": "",
        "folder-documents": '<path d="M25 33h14v17H25zM29 38h6m-6 5h6"/>',
        "folder-download": '<path d="M32 32v13m-6-6 6 6 6-6M23 48h18"/>',
        "folder-pictures": '<rect x="23" y="33" width="19" height="16" rx="2"/><path d="m24 46 6-5 5 4 3-3 3 4"/>',
        "folder-music": '<path d="M29 46V35l11-2v11M29 39l11-2"/><ellipse cx="26" cy="47" rx="3" ry="2"/><ellipse cx="37" cy="45" rx="3" ry="2"/>',
        "folder-videos": '<rect x="23" y="34" width="19" height="14" rx="2"/><path d="m30 38 6 3-6 3z"/>',
        "folder-templates": '<path d="M25 33h14v17H25zM31 33v17M25 39h14"/>',
        "folder-publicshare": '<circle cx="32" cy="41" r="8"/><path d="M24 41h16M32 33c-4 4-4 12 0 16m0-16c4 4 4 12 0 16"/>',
        "user-home": '<path d="m23 40 9-8 9 8m-16-2v12h14V38M30 50v-7h4v7"/>',
        "user-desktop": '<rect x="22" y="33" width="20" height="13" rx="2"/><path d="M32 46v5m-5 0h10"/>',
        "user-trash": '<path d="M26 36h13l-1 14H27zM24 35h17M29 32h7m-6 8v6m5-6v6"/>',
        "folder-saved-search": '<circle cx="30" cy="40" r="6"/><path d="m35 45 6 6"/>',
    }
    for name, glyph in folder_glyphs.items():
        content = folder(glyph)
        write(ICONS / "scalable/places" / f"{name}.svg", content)
        if name == "folder":
            write(DATA / "icon-preview/folder.svg", content)
    for alias, name in {"folder-open": "folder", "inode-directory": "folder", "folder-documents-open": "folder-documents", "folder-downloads": "folder-download", "folder-download-open": "folder-download", "user-trash-full": "user-trash", "folder-recent": "folder-saved-search", "user-bookmarks": "folder-saved-search"}.items():
        path = ICONS / "scalable/places" / f"{alias}.svg"
        if not path.exists():
            path.symlink_to(name + ".svg")
    for name, kind in {"text-x-generic": "text", "application-pdf": "office", "x-office-document": "office", "x-office-spreadsheet": "office", "x-office-presentation": "office", "image-x-generic": "image", "audio-x-generic": "music", "video-x-generic": "video", "application-x-executable": "code", "application-x-desktop": "software"}.items():
        target = ICONS / "scalable/mimetypes" / f"{name}.svg"
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            target.symlink_to("../apps/" + kind + ".svg")
    write(ICONS / "index.theme", """
        [Icon Theme]
        Name=Hiili
        Comment=Graphite icons with muted teal, plum and slate details
        Inherits=Yaru-dark,Adwaita,hicolor
        Directories=scalable/apps,scalable/places,scalable/mimetypes

        [scalable/apps]
        Size=64
        Type=Scalable
        MinSize=16
        MaxSize=512
        Context=Applications

        [scalable/places]
        Size=64
        Type=Scalable
        MinSize=16
        MaxSize=512
        Context=Places

        [scalable/mimetypes]
        Size=64
        Type=Scalable
        MinSize=16
        MaxSize=512
        Context=MimeTypes
    """)
    shutil.copy2(DATA / "icon-preview/hiili.svg", DATA / "hiili-logo.svg")
    logo = ROOT / "usr/share/icons/hicolor/scalable/apps/fi.hiili.Theme.svg"
    logo.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(DATA / "hiili-logo.svg", logo)


def generate_wallpaper():
    write(DATA / "hiili.svg", '''
        <svg xmlns="http://www.w3.org/2000/svg" width="3840" height="2160" viewBox="0 0 3840 2160">
          <defs>
            <linearGradient id="ground" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#080a0e"/><stop offset=".5" stop-color="#141a21"/><stop offset="1" stop-color="#090c11"/></linearGradient>
            <linearGradient id="ridge" x1="0" y1="0" x2=".8" y2="1"><stop stop-color="#26343f"/><stop offset=".34" stop-color="#1a232d"/><stop offset="1" stop-color="#0d1219"/></linearGradient>
            <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#5c858a" stop-opacity=".48"/><stop offset=".5" stop-color="#344b60" stop-opacity=".18"/><stop offset="1" stop-color="#735467" stop-opacity=".22"/></linearGradient>
            <radialGradient id="teal"><stop stop-color="#2a5356" stop-opacity=".25"/><stop offset="1" stop-color="#10232a" stop-opacity="0"/></radialGradient>
            <radialGradient id="plum"><stop stop-color="#573e55" stop-opacity=".2"/><stop offset="1" stop-color="#251d2f" stop-opacity="0"/></radialGradient>
          </defs>
          <rect width="3840" height="2160" fill="url(#ground)"/>
          <ellipse cx="2930" cy="380" rx="1400" ry="1150" fill="url(#teal)"/>
          <ellipse cx="700" cy="1940" rx="1700" ry="900" fill="url(#plum)"/>
          <path d="M-600 2600C200 250 1050 1180 1870 710S2980-310 4340-570L4520 2600Z" fill="url(#ridge)"/>
          <path d="M-600 2600C200 250 1050 1180 1870 710S2980-310 4340-570" fill="none" stroke="url(#edge)" stroke-width="5"/>
          <path d="M-250 2480C550 770 1340 1390 2110 990S3330-40 4310-90L4450 2510Z" fill="#0c1118" opacity=".48"/>
          <path d="M-250 2480C550 770 1340 1390 2110 990S3330-40 4310-90" fill="none" stroke="#617785" stroke-opacity=".13" stroke-width="3"/>
          <path d="M-600 2470C980 1340 1840 1870 2620 1330S3600 650 4340 900L4500 2600Z" fill="#070b10" opacity=".57"/>
          <path d="M-600 2470C980 1340 1840 1870 2620 1330S3600 650 4340 900" fill="none" stroke="#6d576f" stroke-opacity=".2" stroke-width="3"/>
        </svg>
    ''')


def generate_variants():
    for key, selected in PALETTES.items():
        folder = DATA / "variants" / key
        for name in ("gtk3.css", "gtk4.css", "shell.css"):
            write(folder / name, recolor((DATA / name).read_text(), key))
        write(folder / "wallpaper.svg", recolor((DATA / "hiili.svg").read_text(), key))
        preview = folder / "icon-preview"
        for path in (DATA / "icon-preview").glob("*.svg"):
            write(preview / path.name, recolor(path.read_text(), key, icons=True))
        if key == "hiili":
            continue
        icons = ICONS.with_name(selected["theme"])
        shutil.copytree(ICONS, icons, symlinks=True)
        (icons / "icon-theme.cache").unlink(missing_ok=True)
        index = icons / "index.theme"
        index.write_text(index.read_text().replace("Name=Hiili\n", "Name=" + selected["name"] + "\n"))
        for path in icons.rglob("*.svg"):
            if not path.is_symlink():
                path.write_text(recolor(path.read_text(), key, icons=True))
        subprocess.run(["gtk-update-icon-cache", "-q", "-t", "-f", str(icons)], check=True)


def build():
    if ROOT.exists():
        shutil.rmtree(ROOT)
    ROOT.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    lib = ROOT / "usr/lib/hiili-theme"
    lib.mkdir(parents=True, exist_ok=True)
    for name in ("engine.py", "session_apply.py", "hiili-theme", "palettes.py", "chatgpt_prompts.py", "theme_packs.py", "content_policy.py", "system_info.py"):
        shutil.copy2(BASE / "src" / name, lib / name)
        (lib / name).chmod(0o755 if name in ("hiili-theme", "session_apply.py") else 0o644)
    for name in ("gtk3.css", "gtk4.css", "shell.css"):
        shutil.copy2(BASE / "src" / name, DATA / name)
    command = ROOT / "usr/bin/hiili-theme"
    command.parent.mkdir(parents=True, exist_ok=True)
    if not command.exists():
        command.symlink_to("../lib/hiili-theme/hiili-theme")
    command.with_name("chatgpt-ubuntu-theme-manager").symlink_to("../lib/hiili-theme/hiili-theme")
    generate_icons()
    generate_wallpaper()
    generate_variants()
    for key, (title, _) in PROMPTS.items():
        write(DATA / "prompts" / (key + ".txt"), build_prompt(key) + "\n")
    from theme_packs import example_manifest
    import json
    write(DATA / "examples/theme.json", json.dumps(example_manifest(), ensure_ascii=False, indent=2) + "\n")
    write(ROOT / "usr/share/applications/fi.hiili.Theme.desktop", """
        [Desktop Entry]
        Type=Application
        Name=ChatGPT Ubuntu Theme Manager
        Comment=Valitse tumma työpöytäteema tai suunnittele uusi ChatGPT:n kanssa
        Exec=chatgpt-ubuntu-theme-manager
        Icon=fi.hiili.Theme
        Terminal=false
        Categories=Settings;DesktopSettings;
        Keywords=theme;dark;appearance;teema;tumma;ulkoasu;
        StartupNotify=true
        Actions=Apply;Restore;

        [Desktop Action Apply]
        Name=Ota Hiili käyttöön
        Exec=hiili-theme --apply

        [Desktop Action Restore]
        Name=Palauta aiempi ulkoasu
        Exec=hiili-theme --restore
    """)
    write(ROOT / "DEBIAN/control", f"""
        Package: hiili-theme
        Version: {VERSION}
        Section: x11
        Priority: optional
        Architecture: all
        Maintainer: Hiili Theme <hiili@localhost>
        Depends: python3, python3-gi, gir1.2-gtk-4.0 (>= 4.18), gir1.2-adw-1 (>= 1.6), yaru-theme-gtk, yaru-theme-gnome-shell, yaru-theme-icon, gnome-shell-extensions, dconf-gsettings-backend, libglib2.0-bin
        Description: ChatGPT Ubuntu Theme Manager with importable dark palettes
         Finnish graphical manager for dark GTK and GNOME Shell themes,
         matching SVG icons, wallpapers and reversible appearance backups.
         Includes five palettes, JSON theme import and ChatGPT prompt templates.
         Community project; not affiliated with OpenAI or Canonical.
    """)
    write(ROOT / "DEBIAN/postinst", """
        #!/bin/sh
        set -e
        if [ "$1" = configure ]; then
            if command -v gtk-update-icon-cache >/dev/null 2>&1; then
                gtk-update-icon-cache -q -t -f /usr/share/icons/Hiili || true
            fi
            if command -v update-desktop-database >/dev/null 2>&1; then
                update-desktop-database /usr/share/applications || true
            fi
            if [ -z "${2:-}" ]; then
                python3 /usr/lib/hiili-theme/session_apply.py || true
            fi
        fi
        exit 0
    """, executable=True)
    write(ROOT / "DEBIAN/prerm", """
        #!/bin/sh
        set -e
        case "$1" in
            remove|deconfigure) python3 /usr/lib/hiili-theme/session_apply.py --restore || true ;;
        esac
        exit 0
    """, executable=True)
    docs = ROOT / "usr/share/doc/hiili-theme"
    docs.mkdir(parents=True, exist_ok=True)
    for name in ("CONTENT_POLICY.md", "SUPPORT.md"):
        shutil.copy2(BASE / name, docs / name)
    write(docs / "copyright", """
        Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
        Upstream-Name: Hiili

        Files: *
        Copyright: 2026 Hiili contributors
        License: GPL-3.0+
         This program is free software: you can redistribute it and/or modify
         it under the terms of the GNU General Public License as published by
         the Free Software Foundation, either version 3 of the License, or
         (at your option) any later version.
         On Debian systems the complete license is available at
         /usr/share/common-licenses/GPL-3.

        Comment:
         Hiili reuses the locally installed Ubuntu Yaru GTK and Shell assets at
         activation time. Those assets retain their upstream copyright and
         licensing. No Yaru artwork is included in this binary package.
         Yaru source: https://github.com/ubuntu/yaru
         See /usr/share/doc/yaru-theme-gtk/copyright and
         /usr/share/doc/yaru-theme-gnome-shell/copyright.
    """)
    shutil.copy2("/usr/share/common-licenses/GPL-3", docs / "LICENSE")
    count = len(list(ICONS.rglob("*.svg")))
    subprocess.run(["gtk-update-icon-cache", "-q", "-t", "-f", str(ICONS)], check=True)
    subprocess.run(["desktop-file-validate", str(ROOT / "usr/share/applications/fi.hiili.Theme.desktop")], check=True)
    installed_size = sum(path.stat().st_size for path in (ROOT / "usr").rglob("*") if path.is_file() and not path.is_symlink())
    control = ROOT / "DEBIAN/control"
    control.write_text(control.read_text() + f"Installed-Size: {(installed_size + 1023) // 1024}\n")
    checksums = []
    for path in sorted((ROOT / "usr").rglob("*")):
        if path.is_file() and not path.is_symlink():
            checksums.append(hashlib.md5(path.read_bytes()).hexdigest() + "  " + str(path.relative_to(ROOT)))
    write(ROOT / "DEBIAN/md5sums", "\n".join(checksums) + "\n")
    subprocess.run(["dpkg-deb", "--root-owner-group", "--build", str(ROOT), str(OUTPUT / f"chatgpt-ubuntu-theme-manager_{VERSION}_all.deb")], check=True)
    print(f"{APP_NAME} {VERSION} built; {len(PALETTES)} themes, {count} icon names each.")


if __name__ == "__main__":
    build()
