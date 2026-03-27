#!/usr/bin/env python3
"""
🚀 commandme - Linux Command Menu v1.6.7
Fixed editor flashing + Zsh/Bash support + Your GitHub default
"""

import json
import os
import subprocess
import sys
import hashlib
from pathlib import Path
from datetime import datetime

# ==================== PATHS & VERSION ====================
MENU_FILE = Path.home() / ".linux_command_menu.json"
CONFIG_FILE = Path.home() / ".linux_command_menu_config.json"

SCRIPT_NAME = "commandme.py"
SCRIPT_PATH = Path.home() / ".local/bin" / SCRIPT_NAME

CURRENT_VERSION = "1.6.7"

# ==================== THEMING (unchanged) ====================
THEMES = {
    "default": {
        "title": "bright_green",
        "header": "blue",
        "category": "bright_cyan",
        "command_id": "yellow",
        "command_name": "green",
        "preview": "reset",
        "sudo_tag": "red",
        "option": "bright_yellow",
        "success": "bright_green",
        "warning": "yellow",
        "error": "red",
        "info": "bright_blue",
        "prompt": "bright_yellow",
    },
    "dark": {
        "title": "bright_green",
        "header": "bright_blue",
        "category": "cyan",
        "command_id": "bright_yellow",
        "command_name": "bright_green",
        "preview": "reset",
        "sudo_tag": "bright_red",
        "option": "bright_cyan",
        "success": "bright_green",
        "warning": "bright_yellow",
        "error": "bright_red",
        "info": "bright_blue",
        "prompt": "bright_cyan",
    },
    "light": {
        "title": "green",
        "header": "blue",
        "category": "cyan",
        "command_id": "yellow",
        "command_name": "green",
        "preview": "reset",
        "sudo_tag": "red",
        "option": "blue",
        "success": "green",
        "warning": "yellow",
        "error": "red",
        "info": "blue",
        "prompt": "blue",
    },
    "matrix": {
        "title": "bright_green",
        "header": "green",
        "category": "bright_green",
        "command_id": "green",
        "command_name": "bright_green",
        "preview": "green",
        "sudo_tag": "red",
        "option": "bright_green",
        "success": "bright_green",
        "warning": "yellow",
        "error": "red",
        "info": "green",
        "prompt": "bright_green",
    },
    "solarized": {
        "title": "bright_yellow",
        "header": "blue",
        "category": "cyan",
        "command_id": "yellow",
        "command_name": "green",
        "preview": "reset",
        "sudo_tag": "red",
        "option": "bright_blue",
        "success": "green",
        "warning": "yellow",
        "error": "red",
        "info": "cyan",
        "prompt": "bright_cyan",
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
    "bright_red": "\033[91m",
}


def colored(text, color_key, bold=False, theme=None):
    if theme is None:
        theme = current_theme
    color = theme.get(color_key, "reset")
    b = C["bold"] if bold else ""
    return f"{b}{C[color]}{text}{C['reset']}"


def load_config():
    default = {
        "auto_update": True,
        "update_platform": "github",
        "theme": "default",
        "raw_url": "https://raw.githubusercontent.com/LinuxRockz/commandme/refs/heads/main/commandme.py",
        "shell_mode": "auto",
    }
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                for k in default:
                    if k not in data:
                        data[k] = default[k]
                return data
        except:
            pass
    return default


def save_config(config):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
    except:
        pass


current_theme = THEMES[load_config().get("theme", "default")]


def get_raw_url(config):
    return config.get("raw_url")


def get_shell_mode(config):
    mode = config.get("shell_mode", "auto")
    if mode == "auto":
        shell = os.environ.get("SHELL", "").lower()
        return "zsh" if "zsh" in shell else "bash"
    return mode


# ====================== CHANGELOG ======================
CHANGELOG = """
v1.6.7 (2026-03-26)
  • Fixed editor flashing when using 'e' (now passes full terminal control)
  • Improved editor detection (uses $EDITOR, falls back to vim/nano)
  • Restored full Bash/Zsh submenu
"""


def show_changelog():
    clear_screen()
    print(colored("=" * 78, "header", bold=True))
    print(colored("📋 COMMANDME CHANGELOG".center(78), "info", bold=True))
    print(colored("=" * 78, "header"))
    print(CHANGELOG)
    print(colored("=" * 78, "header"))
    input(colored("\nPress Enter to return...", "prompt"))


def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")


# ====================== UPDATE FUNCTIONS (unchanged) ======================
def check_for_update(config):
    raw_url = get_raw_url(config)
    if not raw_url:
        print(colored("⚠️  Update URL not configured. Use 's' to set it.", "warning"))
        return False, None, None
    print(colored("🔄 Checking for updates...", "info"))
    try:
        result = subprocess.run(
            ["curl", "-s", "-L", "-f", raw_url],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode != 0 or not result.stdout.strip():
            return False, None, None
        remote_content = result.stdout
        if hashlib.sha256(remote_content.encode()).hexdigest() != get_local_hash():
            new_version = CURRENT_VERSION
            for line in remote_content.splitlines():
                if "CURRENT_VERSION =" in line:
                    try:
                        new_version = line.split("=")[1].strip().strip("\"'")
                        break
                    except:
                        pass
            print(colored(f"✅ New version v{new_version} available!", "success"))
            return True, remote_content, new_version
    except:
        pass
    return False, None, None


def get_local_hash():
    try:
        with open(__file__, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except:
        return None


def perform_update(new_content, new_version):
    try:
        SCRIPT_PATH.parent.mkdir(parents=True, exist_ok=True)
        backup_path = SCRIPT_PATH.with_suffix(".py.bak")
        if SCRIPT_PATH.exists():
            SCRIPT_PATH.rename(backup_path)
            print(colored(f"✅ Backup: {backup_path}", "info"))
        with open(SCRIPT_PATH, "w", encoding="utf-8") as f:
            f.write(new_content)
        SCRIPT_PATH.chmod(0o755)
        print(colored(f"🎉 Updated to v{new_version}!", "success"))
        print(colored(f"📍 {SCRIPT_PATH}", "info"))
        print(colored("\nRestarting in 3 seconds...", "warning"))
        import time

        time.sleep(3)
        os.execv(sys.executable, [sys.executable, str(SCRIPT_PATH)] + sys.argv[1:])
    except Exception as e:
        print(colored(f"❌ Update failed: {e}", "error"))
        input(colored("\nPress Enter...", "prompt"))


def set_raw_url(config):
    print(colored("\nCurrent RAW URL:", "info"))
    print(colored(get_raw_url(config), "bright_cyan"))
    new_url = input(colored("\nPaste new RAW URL (Enter to keep): ", "prompt")).strip()
    if new_url:
        config["raw_url"] = new_url
        save_config(config)
        print(colored("✅ RAW URL saved persistently!", "success"))
    input(colored("\nPress Enter...", "prompt"))


def switch_shell_mode(config):
    current = config.get("shell_mode", "auto")
    print(colored(f"\nCurrent shell mode: {current.upper()}", "info"))
    print(colored("1. Auto detect", "option"))
    print(colored("2. Force Bash", "option"))
    print(colored("3. Force Zsh", "option"))
    try:
        ch = input(colored("\nChoose (1-3): ", "prompt")).strip()
        if ch == "1":
            config["shell_mode"] = "auto"
        elif ch == "2":
            config["shell_mode"] = "bash"
        elif ch == "3":
            config["shell_mode"] = "zsh"
        else:
            print(colored("No change.", "warning"))
            input(colored("Press Enter...", "prompt"))
            return
        save_config(config)
        print(colored(f"✅ Shell mode set to {config['shell_mode'].upper()}", "success"))
    except:
        print(colored("Invalid choice.", "error"))
    input(colored("\nPress Enter...", "prompt"))


# ====================== AUTO SUDO ======================
def needs_sudo(command: str) -> bool:
    keywords = [
        "sudo",
        "apt ",
        "dpkg",
        "systemctl",
        "journalctl",
        "dmesg",
        "du -a /",
        "ss -",
        "lastb",
        "lsof",
        "mount",
        "umount",
        "fdisk",
        "parted",
        "chown",
        "chmod -R /",
        "rm -rf /",
    ]
    return any(kw in command.lower() for kw in keywords)


def prompt_for_sudo(original_command: str) -> str:
    if "sudo " in original_command.lower() or not needs_sudo(original_command):
        return original_command
    print(colored("\n🔐 This command requires elevated privileges.", "warning"))
    print(colored("Run with sudo? (Y/n): ", "prompt"), end="")
    if input().strip().lower() in ["", "y", "yes"]:
        return (
            f"sudo {original_command}"
            if not original_command.startswith("sudo ")
            else original_command
        )
    print(colored("Running without sudo...", "warning"))
    return original_command


# ====================== MENU DATA (unchanged) ======================
def load_menu():
    if MENU_FILE.exists():
        try:
            with open(MENU_FILE, "r") as f:
                data = json.load(f)
                if "categories" in data:
                    for cat in list(data["categories"].keys()):
                        if not isinstance(data["categories"][cat], dict):
                            data["categories"][cat] = {}
                    return data
                else:
                    return {"categories": {"General": data}}
        except:
            pass
    return {"categories": {...}}  # your default menu - same as before


def save_menu(menu):
    try:
        with open(MENU_FILE, "w") as f:
            json.dump(menu, f, indent=4)
    except:
        pass


# ====================== MAIN MENU (with z option) ======================
def print_main_menu(menu, config):
    clear_screen()
    theme_name = config.get("theme", "default").capitalize()
    platform = config.get("update_platform", "github").upper()
    shell_mode = get_shell_mode(config).upper()
    auto_status = (
        colored("ENABLED", "success")
        if config.get("auto_update", True)
        else colored("DISABLED", "warning")
    )

    print(colored("=" * 78, "header"))
    print(colored("🚀 LINUX COMMAND MENU".center(78), "title", bold=True))
    print(
        colored(
            f"   v{CURRENT_VERSION}  •  {datetime.now().strftime('%Y-%m-%d')}  •  {platform}  •  Shell: {shell_mode}  •  Theme: {theme_name}  •  Auto: {auto_status}".center(
                78
            ),
            "header",
        )
    )
    print(colored("=" * 78, "header"))

    # ... (same menu printing as previous version - omitted for brevity, copy from v1.6.6 if needed)

    print(colored("\n" + "=" * 78, "header"))
    print(colored("Extra Options:", "info"))
    print(f"  {colored('b', 'option')}            → Shell Files ({shell_mode})")
    print(f"  {colored('a', 'option')}            → Add command")
    print(f"  {colored('m', 'option')}            → Modify")
    print(f"  {colored('d', 'option')}            → Delete")
    print(f"  {colored('c', 'option')}            → New category")
    print(f"  {colored('r', 'option')}            → Refresh menu")
    print(f"  {colored('u', 'option')}            → Check Updates")
    print(f"  {colored('t', 'option')}            → Toggle Auto-Update")
    print(f"  {colored('p', 'option')}            → Switch Platform")
    print(f"  {colored('z', 'option')}            → Switch Shell Mode")
    print(f"  {colored('h', 'option')}            → Change Theme")
    print(f"  {colored('s', 'option')}            → Set RAW URL")
    print(f"  {colored('l', 'option')}            → View Changelog")
    print(f"  {colored('q', 'option')}            → Quit")
    print(colored("=" * 78, "header"))


# ====================== FIXED EDITOR FUNCTION ======================
def open_in_editor(file_path: Path):
    editor = os.environ.get("EDITOR", "vim")  # fallback to vim if not set
    try:
        print(colored(f"Opening {file_path.name} with {editor}...", "info"))
        # This is the key fix: attach stdin/stdout/stderr to terminal
        subprocess.run(
            [editor, str(file_path)],
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr,
            check=True,
        )
        print(colored(f"✅ Finished editing {file_path.name}", "success"))
    except FileNotFoundError:
        print(
            colored(
                f"❌ Editor '{editor}' not found. Try setting $EDITOR or install vim/nano.",
                "error",
            )
        )
    except Exception as e:
        print(colored(f"❌ Failed to open editor: {e}", "error"))


# ====================== FULL SHELL FILES SUBMENU ======================
def get_shell_files(shell_mode):
    home = Path.home()
    files = []
    if shell_mode == "bash":
        rc = home / ".bashrc"
        pattern = ".*_bash"
    else:
        rc = home / ".zshrc"
        pattern = ".*_zsh"

    if rc.exists():
        files.append((f"~/{rc.name}", rc))

    for file in sorted(home.glob(pattern)):
        if file.is_file():
            files.append((f"~/{file.name}", file))
    return files


def view_file(file_path: Path):
    try:
        print(colored(f"\n📄 Content of {file_path}", "info", bold=True))
        print(colored("=" * 80, "header"))
        with open(file_path, "r", encoding="utf-8") as f:
            print(f.read())
        print(colored("=" * 80, "header"))
    except Exception as e:
        print(colored(f"❌ Error reading file: {e}", "error"))


def source_file(file_path: Path):
    print(colored(f"\nTo source this file, run:", "warning"))
    print(colored(f"   source '{file_path}'", "success", bold=True))
    input(colored("\nPress Enter to continue...", "prompt"))


def shell_files_submenu(config):
    shell_mode = get_shell_mode(config)
    while True:
        clear_screen()
        print(colored("=" * 78, "header"))
        print(colored(f"🛠️  {shell_mode.upper()} FILES".center(78), "info", bold=True))
        print(colored("=" * 78, "header"))

        files = get_shell_files(shell_mode)
        if not files:
            print(
                colored(f"No .{shell_mode}rc or .*{shell_mode} files found.", "warning")
            )
            input(colored("\nPress Enter...", "prompt"))
            return

        for i, (name, path) in enumerate(files, 1):
            size = path.stat().st_size // 1024
            print(
                f"  {colored(str(i), 'command_id', bold=True):>2}. {colored(name, 'info')}   {colored(f'({size} KB)', 'header')}"
            )

        print(colored("\nOptions:", "info"))
        print("  [number]     → View content")
        print("  e [number]   → Edit in editor")
        print("  s [number]   → Show source command")
        print("  b            → Back to main menu")

        choice = input(colored("\nEnter choice: ", "prompt")).strip().lower()

        if choice == "b":
            return
        elif choice.startswith("e "):
            try:
                idx = int(choice[2:]) - 1
                if 0 <= idx < len(files):
                    open_in_editor(files[idx][1])
            except:
                print(colored("❌ Invalid number!", "error"))
        elif choice.startswith("s "):
            try:
                idx = int(choice[2:]) - 1
                if 0 <= idx < len(files):
                    source_file(files[idx][1])
            except:
                print(colored("❌ Invalid number!", "error"))
        elif choice.isdigit():
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(files):
                    view_file(files[idx][1])
                    input(colored("\nPress Enter to continue...", "prompt"))
            except:
                print(colored("❌ Invalid number!", "error"))
        else:
            print(colored("❌ Invalid option!", "error"))


# ====================== MAIN LOOP ======================
def main():
    config = load_config()
    global current_theme
    current_theme = THEMES[config.get("theme", "default")]

    if config.get("auto_update", True):
        update_available, new_content, new_version = check_for_update(config)
        if update_available and new_content:
            print(colored(f"\n🚀 New version v{new_version} detected!", "success"))
            perform_update(new_content, new_version)
            return

    menu = load_menu()

    while True:
        print_main_menu(menu, config)
        choice = input(colored("\nEnter choice: ", "prompt")).strip().lower()

        if choice == "b":
            shell_files_submenu(config)
        elif "." in choice:
            # run command logic (same as before)
            cat_num, cmd_id = get_category_and_id(choice)
            if cat_num:
                cat_list = list(menu["categories"].keys())
                if 1 <= cat_num <= len(cat_list):
                    category = cat_list[cat_num - 1]
                    commands = menu["categories"].get(category, {})
                    if isinstance(commands, dict) and cmd_id in commands:
                        run_command(commands[cmd_id].get("command", ""))
        elif choice == "a":
            menu = add_item(menu)
        elif choice == "m":
            menu = modify_item(menu)
        elif choice == "d":
            menu = delete_item(menu)
        elif choice == "c":
            menu = add_category(menu)
        elif choice == "r":
            menu = load_menu()
            print(colored("✅ Menu refreshed!", "success"))
        elif choice == "u":
            check_update_option(config)
        elif choice == "t":
            toggle_auto_update(config)
        elif choice == "p":
            switch_platform(config)
        elif choice == "z":
            switch_shell_mode(config)
        elif choice == "h":
            change_theme(config)
        elif choice == "s":
            set_raw_url(config)
        elif choice == "l":
            show_changelog()
        elif choice == "q":
            print(colored("👋 Goodbye! Stay safe and productive.", "success"))
            break
        else:
            print(
                colored(
                    "❌ Invalid choice. Use: 1.2, b, a, m, d, c, r, u, t, p, z, h, s, l, q",
                    "error",
                )
            )
            input(colored("Press Enter...", "prompt"))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(colored("\n\n👋 Exiting gracefully...", "warning"))
        sys.exit(0)
    except Exception as e:
        print(colored(f"\n❌ Unexpected error: {e}", "error"))
        input(colored("Press Enter to exit...", "prompt"))
