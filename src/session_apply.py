#!/usr/bin/python3
"""Package hook: delegate appearance changes to the active local desktop user."""
import os
import pwd
import subprocess
import sys
from palettes import APP_NAME


def active_users():
    result = subprocess.run(["loginctl", "list-sessions", "--no-legend", "--no-pager"],
                            capture_output=True, text=True, timeout=10, check=True)
    users = {}
    for line in result.stdout.splitlines():
        session = line.split()[0]
        result = subprocess.run(["loginctl", "show-session", session, "-p", "User", "-p", "Active", "-p", "Type", "-p", "Remote"],
                                capture_output=True, text=True, timeout=10, check=True)
        props = dict(item.split("=", 1) for item in result.stdout.splitlines() if "=" in item)
        if props.get("Active") != "yes" or props.get("Type") not in ("wayland", "x11") or props.get("Remote") == "yes":
            continue
        uid = int(props["User"])
        if uid >= 1000 and uid != 65534 and os.path.exists(f"/run/user/{uid}/bus"):
            users[uid] = pwd.getpwuid(uid)
    return list(users.values())


def main():
    action = "--restore" if "--restore" in sys.argv else "--apply"
    try:
        users = active_users()
    except (subprocess.SubprocessError, OSError, ValueError) as error:
        print(f"Hiili: automaattinen käyttöönotto: {error}", file=sys.stderr)
        return 0
    if len(users) != 1:
        print(f"{APP_NAME} on asennettu. Ota teema käyttöön sovellusvalikosta.")
        return 0
    user = users[0]
    result = subprocess.run([
        "runuser", "-u", user.pw_name, "--", "env", "-i",
        f"HOME={user.pw_dir}", f"USER={user.pw_name}", f"LOGNAME={user.pw_name}",
        "PATH=/usr/local/bin:/usr/bin:/bin",
        f"XDG_CONFIG_HOME={user.pw_dir}/.config", f"XDG_DATA_HOME={user.pw_dir}/.local/share",
        f"XDG_RUNTIME_DIR=/run/user/{user.pw_uid}",
        f"DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/{user.pw_uid}/bus",
        "XDG_CURRENT_DESKTOP=ubuntu:GNOME", "LANG=fi_FI.UTF-8",
        "/usr/bin/hiili-theme", action, "--quiet",
    ], timeout=90)
    if result.returncode:
        print(f"{APP_NAME} on asennettu. Avaa ohjelma sovellusvalikosta viimeistelläksesi käyttöönoton.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
