#!/usr/bin/python3
"""Render the real GTK control window on a private X server and private bus."""
from pathlib import Path
import os
import signal
import subprocess
import sys
import tempfile
import time
import argparse
import shutil
from PIL import ImageGrab

BASE = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--showcase", action="store_true")
parser.add_argument("--smoke", action="store_true")
parser.add_argument("--variant", default="hiili")
args = parser.parse_args()
ROOT = BASE / "tools/root"
fixture = Path(tempfile.mkdtemp(prefix="hiili-ui-", dir=BASE / "tests"))
# AF_UNIX socket paths are short; the repository itself may be deeply nested.
runtime = Path(tempfile.mkdtemp(prefix="ctm-run-"))
env = dict(os.environ)
env.update({"XDG_CONFIG_HOME": str(fixture / "config"), "XDG_DATA_HOME": str(fixture / "share"),
            "XDG_CACHE_HOME": str(fixture / "cache"), "XDG_RUNTIME_DIR": str(runtime),
            "HIILI_DATA_DIR": str(BASE / "package/usr/share/hiili-theme"),
            "XDG_DATA_DIRS": str(BASE / "package/usr/share") + ":/usr/local/share:/usr/share",
            "GSETTINGS_BACKEND": "dconf", "GDK_BACKEND": "x11", "GSK_RENDERER": "cairo",
            "LIBGL_ALWAYS_SOFTWARE": "1", "NO_AT_BRIDGE": "1", "GTK_A11Y": "none",
            "GTK_USE_PORTAL": "0", "GIO_USE_VFS": "local",
            "LD_LIBRARY_PATH": str(ROOT / "usr/lib/x86_64-linux-gnu")})
env["THEME_PREVIEW_VARIANT"] = args.variant
display = next(f":{i}" for i in range(92, 120) if not Path(f"/tmp/.X11-unix/X{i}").exists())
env["DISPLAY"] = display
log = (fixture / "render.log").open("w")
server_binary = shutil.which("Xvfb") or str(ROOT / "usr/bin/Xvfb")
bus_binary = shutil.which("dbus-daemon") or str(ROOT / "usr/bin/dbus-daemon")
server = subprocess.Popen([server_binary, display, "-screen", "0", "820x1000x24", "-nolisten", "tcp", "-ac"], env=env, stdout=log, stderr=log)
bus = None
app = None
try:
    for _ in range(50):
        if Path(f"/tmp/.X11-unix/X{display[1:]}").exists():
            break
        if server.poll() is not None:
            raise RuntimeError((fixture / "render.log").read_text())
        time.sleep(.1)
    else:
        raise RuntimeError("Virtual X server did not start")
    bus = subprocess.Popen([bus_binary, "--session", "--nofork", "--nopidfile", "--print-address=1", "--address=unix:path=" + str(runtime / "bus")], env=env, stdout=subprocess.PIPE, stderr=log, text=True)
    env["DBUS_SESSION_BUS_ADDRESS"] = bus.stdout.readline().strip()
    if not env["DBUS_SESSION_BUS_ADDRESS"]:
        raise RuntimeError("Private test bus did not start: " + (fixture / "render.log").read_text())
    if args.smoke:
        env["THEME_MANAGER_TEST_LIB"] = str(BASE / "package/usr/lib/hiili-theme")
        command = [sys.executable, str(BASE / "tests/gui_smoke.py"), str(fixture / "smoke.json")]
    elif args.showcase:
        command = [sys.executable, str(BASE / "tests/showcase.py")]
    else:
        command = [sys.executable, str(BASE / "src/hiili-theme")]
    app = subprocess.Popen(command, env=env, stdout=log, stderr=log)
    if args.smoke:
        import json
        for _ in range(120):
            if (fixture / "smoke.json").exists():
                break
            if app.poll() is not None:
                raise RuntimeError((fixture / "render.log").read_text())
            time.sleep(.1)
        report = json.loads((fixture / "smoke.json").read_text())
        assert report["ok"], report
        print("PASS: real GUI imports a downloaded ZIP, applies and restores palettes; custom-target URL and clipboard match")
    else:
        time.sleep(2)
    if app.poll() is not None:
        raise RuntimeError((fixture / "render.log").read_text())
    if args.showcase:
        for key in ("gtk-theme", "icon-theme", "color-scheme"):
            result = subprocess.run(["gsettings", "get", "org.gnome.desktop.interface", key], env=env, capture_output=True, text=True, check=True)
            sys.path.insert(0, str(BASE / "src"))
            from palettes import palette
            expected = "'prefer-dark'" if key == "color-scheme" else repr(palette(args.variant)["theme"])
            assert result.stdout.strip() == expected, (key, result.stdout, result.stderr)
        print("PASS: private dconf backend persisted the theme, icons and dark preference")
    suffix = "smoke" if args.smoke else ("esikatselu-" + args.variant if args.showcase else "hallinta")
    screenshot_dir = Path(os.environ.get("SCREENSHOT_OUTPUT_DIR", str(BASE / "test-artifacts")))
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    destination = screenshot_dir / ("chatgpt-ubuntu-theme-manager-1.2-" + suffix + ".png")
    ImageGrab.grab(xdisplay=display).save(destination)
    print("Screenshot:", destination)
    messages = [line for line in (fixture / "render.log").read_text().splitlines() if "Traceback" in line or "ERROR" in line or "CRITICAL" in line or "WARNING" in line]
    print("GTK errors/warnings:", "\n".join(messages) if messages else "none")
finally:
    for process in (app, bus, server):
        if process and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                process.kill()
    log.close()
    shutil.rmtree(runtime)
