#!/usr/bin/env python3
"""
🚀 LINUX COMMAND MENU - v2.3.5
Dracula theme + Cache-busting for Gist version check
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime

# ==================== CONFIG ====================
VERSION = "2.3.5"
MENU_FILE = Path.home() / ".linux_command_menu.json"
THEME_FILE = Path.home() / ".linux_command_menu_theme.json"

# ==================== GIST URL ====================
GIST_RAW_URL = "https://gist.githubusercontent.com/LinuxRockz/943cfd94340f8b8289edfbdda5f227c6/raw/b18daadcf1d4344ac435789ed110cd9657153167/commandme.py"

# ==================== THEMES ====================
AVAILABLE_THEMES = {
    "default": {
        "name": "Default (Green/Cyan)",
        "colors": {
            "header": "bright_green",
            "category": "bright_cyan",
            "id": "bright_yellow",
            "name": "green",
            "command": "reset",
            "extra": "magenta",
            "prompt": "bright_yellow",
        },
    },
    "dark": {
        "name": "Dark / Minimal",
        "colors": {
            "header": "cyan",
            "category": "blue",
            "id": "yellow",
            "name": "green",
            "command": "reset",
            "extra": "magenta",
            "prompt": "yellow",
        },
    },
    "ocean": {
        "name": "Ocean Blue",
        "colors": {
            "header": "bright_blue",
            "category": "bright_cyan",
            "id": "bright_yellow",
            "name": "cyan",
            "command": "reset",
            "extra": "blue",
            "prompt": "bright_cyan",
        },
    },
    "matrix": {
        "name": "Matrix Green",
        "colors": {
            "header": "bright_green",
            "category": "green",
            "id": "bright_yellow",
            "name": "green",
            "command": "reset",
            "extra": "bright_green",
            "prompt": "bright_green",
        },
    },
    "solarized": {
        "name": "Solarized",
        "colors": {
            "header": "yellow",
            "category": "cyan",
            "id": "bright_yellow",
            "name": "green",
            "command": "reset",
            "extra": "blue",
            "prompt": "yellow",
        },
    },
    "dracula": {
        "name": "Dracula",
        "colors": {
            "header": "bright_magenta",
            "category": "bright_cyan",
            "id": "bright_yellow",
            "name": "bright_green",
            "command": "reset",
            "extra": "magenta",
            "prompt": "bright_yellow",
        },
    },
}

C = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "green": "\033[32m",
    "cyan": "\033[36m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "red": "\033[31m",
    "bright_green": "\033[92m",
    "bright_blue": "\033[94m",
    "bright_yellow": "\033[93m",
    "bright_cyan": "\033[96m",
    "bright_magenta": "\033[95m",
}


def load_theme():
    if THEME_FILE.exists():
        try:
            with open(THEME_FILE, "r") as f:
                data = json.load(f)
                return AVAILABLE_THEMES.get(
                    data.get("theme", "default"), AVAILABLE_THEMES["default"]
                )
        except:
            pass
    return AVAILABLE_THEMES["default"]


def save_theme(theme_name):
    try:
        with open(THEME_FILE, "w") as f:
            json.dump({"theme": theme_name}, f, indent=4)
        print(
            colored(
                f"✅ Theme saved: {AVAILABLE_THEMES[theme_name]['name']}", "bright_green"
            )
        )
    except Exception as e:
        print(colored(f"❌ Error saving theme: {e}", "red"))


def colored(text, color_key, bold=False, temp_theme=None):
    if temp_theme:
        color_name = temp_theme["colors"].get(color_key, "reset")
    else:
        theme = load_theme()
        color_name = theme["colors"].get(color_key, "reset")
    b = C["bold"] if bold else ""
    return f"{b}{C.get(color_name, C['reset'])}{text}{C['reset']}"


def show_version(latest=None):
    ver = f"v{VERSION}"
    if latest and latest != VERSION:
        ver += colored(f"  → New: v{latest}", "red", bold=True)
    print(
        colored(
            f"Linux Command Menu {ver}  •  {datetime.now().strftime('%Y-%m-%d')}",
            "header",
        )
    )


def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")


def get_gist_version():
    try:
        import requests

        # Cache busting with timestamp
        url = f"{GIST_RAW_URL}?_={int(time.time())}"
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        for line in r.text.splitlines():
            if line.strip().startswith('VERSION = "'):
                return line.split('"')[1]
    except:
        pass
    return None


# ====================== THEME PREVIEW ======================
def show_theme_preview(theme_key):
    temp = AVAILABLE_THEMES[theme_key]
    clear_screen()
    print(colored("═" * 78, "header", temp_theme=temp))
    print(
        colored(
            "🎨 THEME PREVIEW".center(78), "bright_yellow", bold=True, temp_theme=temp
        )
    )
    print(colored("═" * 78, "header", temp_theme=temp))
    print(colored("   🚀 LINUX COMMAND MENU", "header", bold=True, temp_theme=temp))
    print(colored("   Sample Category", "category", bold=True, temp_theme=temp))
    print(
        colored(
            "   ──────────────────────────────────────────────────────────────",
            "blue",
            temp_theme=temp,
        )
    )
    print(
        f"       {colored('1', 'id', bold=True, temp_theme=temp)}  {colored('Update & Upgrade', 'name', temp_theme=temp):<35} → {colored('sudo apt update && sudo apt upgrade -y', 'command', temp_theme=temp)}"
    )
    print(
        f"       {colored('2', 'id', bold=True, temp_theme=temp)}  {colored('Disk Usage', 'name', temp_theme=temp):<35} → {colored('df -h', 'command', temp_theme=temp)}"
    )
    print(colored("\n   Extra Options:", "extra", temp_theme=temp))
    print(f"     {colored('s', 'prompt', temp_theme=temp)} → Shell Aliases")
    print(f"     {colored('t', 'prompt', temp_theme=temp)} → Change Theme")
    print(f"     {colored('u', 'prompt', temp_theme=temp)} → Self Update")
    print(colored("═" * 78, "header", temp_theme=temp))


# ====================== SELF-UPDATER ======================
def self_update():
    clear_screen()
    print(colored("═" * 78, "header"))
    print(colored("🔄 ONE-CLICK SELF UPDATER".center(78), "bright_yellow", bold=True))
    print(colored("═" * 78, "header"))
    print(colored("→ Checking Gist...", "cyan"))
    latest = get_gist_version()
    if not latest:
        print(colored("❌ Could not reach Gist", "red"))
        input(colored("\nPress Enter...", "prompt"))
        return
    if latest == VERSION:
        print(colored(f"✅ You are on the latest version (v{VERSION})", "bright_green"))
        input(colored("\nPress Enter...", "prompt"))
        return
    print(colored(f"\nNew version available: v{latest}", "bright_green"))
    if input(colored("Update now? (y/N): ", "prompt")).strip().lower() != "y":
        return
    try:
        import requests

        url = f"{GIST_RAW_URL}?_={int(time.time())}"
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        new_code = r.text
    except Exception as e:
        print(colored(f"❌ Download failed: {e}", "red"))
        input(colored("\nPress Enter...", "prompt"))
        return
    script_path = Path(sys.argv[0]).resolve()
    backup = script_path.with_suffix(".bak")
    backup.write_text(script_path.read_text(encoding="utf-8"), encoding="utf-8")
    script_path.write_text(new_code, encoding="utf-8")
    print(colored(f"🎉 Updated to v{latest}!", "bright_green"))
    print(colored("Restart the script.", "cyan"))
    input(colored("\nPress Enter...", "prompt"))


# ====================== Shell Aliases, Themes, Main Menu, etc. (shortened for space) ======================
# The rest of the code is the same as the previous full version.
# For brevity here, I'm only showing the changed parts. Replace the entire file with the previous full code, but use the functions above for get_gist_version, show_version, and self_update.

# (Copy the full script from my previous message and replace only the get_gist_version and show_version functions with the ones above.)


def main():
    menu = load_menu()
    while True:
        print_main_menu(menu)
        choice = input(colored("\nEnter choice: ", "prompt")).strip().lower()

        if choice == "s":
            shell_aliases_submenu()
        elif choice == "t":
            themes_submenu()
        elif choice == "u":
            self_update()
        # ... rest of the menu logic (a, m, d, c, r, numbered, q) as before


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(colored("\n👋 Exiting gracefully...", "yellow"))
        sys.exit(0)
