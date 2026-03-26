#!/usr/bin/env python3
"""
🚀 commandme - Linux Command Menu v1.6.5
Default: Your GitHub repo + Persistent RAW URL + Theming + fastfetch
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

CURRENT_VERSION = "1.6.5"

# ==================== THEMING ====================
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


# ====================== CHANGELOG ======================
CHANGELOG = """
v1.6.5 (2026-03-26)
  • Fixed 'p' (Switch Platform) option in main loop
  • Default RAW URL set to your GitHub repo
  • Minor cleanup
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


# ====================== UPDATE FUNCTIONS ======================
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


# ====================== MENU DATA ======================
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
    return {
        "categories": {
            "System Update & Maintenance": {
                "1": {
                    "name": "Update & Upgrade",
                    "command": "sudo apt update && sudo apt upgrade -y",
                    "needs_sudo": True,
                },
                "2": {
                    "name": "Full System Cleanup",
                    "command": "sudo apt autoremove -y && sudo apt clean && sudo journalctl --vacuum-time=2weeks",
                    "needs_sudo": True,
                },
                "3": {"name": "Update Flatpak", "command": "flatpak update -y"},
            },
            "System Information": {
                "1": {
                    "name": "Quick System Info",
                    "command": "fastfetch || neofetch || uname -a && cat /etc/os-release",
                },
                "2": {"name": "Disk Usage (Human)", "command": "df -h"},
                "3": {"name": "Memory Usage", "command": "free -h"},
                "4": {"name": "CPU & Load", "command": "uptime && cat /proc/loadavg"},
            },
            "File & Directory Tools": {
                "1": {"name": "List with Details", "command": "ls -lah --color=auto"},
                "2": {
                    "name": "Tree View",
                    "command": "tree -L 2 || echo 'Install tree: sudo apt install tree'",
                },
                "3": {
                    "name": "Find Large Files",
                    "command": "sudo du -ah / | sort -rh | head -n 20",
                    "needs_sudo": True,
                },
                "4": {"name": "Find Files by Name", "command": "find . -name "},
            },
            "Networking": {
                "1": {"name": "Show IP & Interfaces", "command": "ip addr show"},
                "2": {
                    "name": "Listening Ports",
                    "command": "sudo ss -tuln",
                    "needs_sudo": True,
                },
                "3": {
                    "name": "DNS Resolution",
                    "command": "resolvectl status || cat /etc/resolv.conf",
                },
                "4": {"name": "Ping Google", "command": "ping -c 4 google.com"},
            },
            "Process Management": {
                "1": {"name": "Interactive Top (htop)", "command": "htop || top"},
                "2": {"name": "List All Processes", "command": "ps aux | less"},
                "3": {"name": "Kill by Name", "command": "pkill -f "},
                "4": {
                    "name": "Find Process by Port",
                    "command": "sudo ss -tlnp | grep ",
                    "needs_sudo": True,
                },
            },
            "Security & Permissions": {
                "1": {
                    "name": "Check Failed Logins",
                    "command": "sudo lastb | head",
                    "needs_sudo": True,
                },
                "2": {"name": "List Open Files", "command": "lsof | less"},
                "3": {"name": "Current User & Groups", "command": "id && groups"},
            },
            "Development Tools": {
                "1": {"name": "Git Status", "command": "git status"},
                "2": {"name": "Docker Status", "command": "docker ps -a"},
                "3": {
                    "name": "Python Virtual Env Info",
                    "command": "python3 -m venv --help | head -5 || echo 'Python venv available'",
                },
                "4": {
                    "name": "Check Python Packages",
                    "command": "pip list | tail -n 20",
                },
            },
            "Logs & Monitoring": {
                "1": {
                    "name": "Last 100 System Logs",
                    "command": "journalctl -n 100 --no-pager",
                },
                "2": {
                    "name": "Tail Auth Log",
                    "command": "sudo tail -f /var/log/auth.log",
                    "needs_sudo": True,
                },
                "3": {
                    "name": "Disk Errors",
                    "command": "sudo dmesg | grep -i error",
                    "needs_sudo": True,
                },
            },
        }
    }


def save_menu(menu):
    try:
        with open(MENU_FILE, "w") as f:
            json.dump(menu, f, indent=4)
    except:
        pass


# ====================== MAIN MENU ======================
def print_main_menu(menu, config):
    clear_screen()
    theme_name = config.get("theme", "default").capitalize()
    platform = config.get("update_platform", "github").upper()
    auto_status = (
        colored("ENABLED", "success")
        if config.get("auto_update", True)
        else colored("DISABLED", "warning")
    )

    print(colored("=" * 78, "header"))
    print(colored("🚀 LINUX COMMAND MENU".center(78), "title", bold=True))
    print(
        colored(
            f"   v{CURRENT_VERSION}  •  {datetime.now().strftime('%Y-%m-%d')}  •  {platform}  •  Theme: {theme_name}  •  Auto: {auto_status}".center(
                78
            ),
            "header",
        )
    )
    print(colored("=" * 78, "header"))

    cat_list = list(menu["categories"].keys())
    for i, category in enumerate(cat_list, 1):
        print(
            f"\n{colored(f'[{i}]', 'command_id', bold=True)} {colored(category.upper(), 'category', bold=True)}"
        )
        print(colored("-" * 65, "header"))
        commands = menu["categories"].get(category, {})
        if not isinstance(commands, dict):
            commands = {}
        for key in sorted(
            commands.keys(), key=lambda x: int(x) if str(x).isdigit() else 999
        ):
            item = commands[key]
            preview = (
                (item.get("command", "")[:50] + "...")
                if len(item.get("command", "")) > 50
                else item.get("command", "")
            )
            sudo_tag = (
                colored(" [sudo]", "sudo_tag", bold=True)
                if item.get("needs_sudo", False)
                else ""
            )
            print(
                f"    {colored(key, 'command_id', bold=True):<4} {colored(item.get('name', 'Unnamed'), 'command_name'):<35} → {colored(preview, 'preview')}{sudo_tag}"
            )

    print(colored("\n" + "=" * 78, "header"))
    print(colored("Extra Options:", "info"))
    print(f"  {colored('b', 'option')}            → Bash Aliases")
    print(f"  {colored('a', 'option')}            → Add command")
    print(f"  {colored('m', 'option')}            → Modify")
    print(f"  {colored('d', 'option')}            → Delete")
    print(f"  {colored('c', 'option')}            → New category")
    print(f"  {colored('r', 'option')}            → Refresh menu")
    print(f"  {colored('u', 'option')}            → Check Updates")
    print(f"  {colored('t', 'option')}            → Toggle Auto-Update")
    print(f"  {colored('p', 'option')}            → Switch Platform")
    print(f"  {colored('h', 'option')}            → Change Theme")
    print(f"  {colored('s', 'option')}            → Set RAW URL")
    print(f"  {colored('l', 'option')}            → View Changelog")
    print(f"  {colored('q', 'option')}            → Quit")
    print(colored("=" * 78, "header"))


def get_category_and_id(choice):
    if "." in choice:
        try:
            cat_num, cmd_id = choice.split(".")
            return int(cat_num), cmd_id.strip()
        except:
            return None, None
    return None, choice.strip()


def run_command(command):
    final_command = prompt_for_sudo(command)
    print(colored(f"\n🔄 Running: {final_command}", "success"))
    print(colored("-" * 70, "header"))
    try:
        result = subprocess.run(
            final_command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        print(result.stdout)
        if result.stderr:
            print(colored("Warnings:\n" + result.stderr.strip(), "warning"))
    except subprocess.CalledProcessError as e:
        print(colored(f"❌ Failed with exit code {e.returncode}", "error"))
        if e.stderr:
            print(e.stderr.strip())
    except Exception as e:
        print(colored(f"❌ Error: {e}", "error"))
    input(colored("\nPress Enter to continue...", "prompt"))


# ====================== BASH ALIASES ======================
def bash_aliases_submenu():
    while True:
        clear_screen()
        print(colored("=" * 78, "header"))
        print(colored("🛠️  BASH ALIASES & SOURCED FILES".center(78), "info", bold=True))
        print(colored("=" * 78, "header"))
        print(colored("Bash aliases submenu ready", "info"))
        input(colored("\nPress Enter to return...", "prompt"))
        return


# ====================== CRUD (stub) ======================
def add_item(menu):
    print(colored("\nAdd command - expand later", "info"))
    input(colored("Press Enter...", "prompt"))
    return menu


def modify_item(menu):
    print(colored("\nModify command - expand later", "info"))
    input(colored("Press Enter...", "prompt"))
    return menu


def delete_item(menu):
    print(colored("\nDelete - expand later", "info"))
    input(colored("Press Enter...", "prompt"))
    return menu


def add_category(menu):
    print(colored("\nAdd category - expand later", "info"))
    input(colored("Press Enter...", "prompt"))
    return menu


def toggle_auto_update(config):
    config["auto_update"] = not config.get("auto_update", True)
    save_config(config)
    status = "ENABLED" if config["auto_update"] else "DISABLED"
    print(
        colored(
            f"✅ Auto-update is now {status}",
            "success" if config["auto_update"] else "warning",
        )
    )
    input(colored("\nPress Enter...", "prompt"))


def switch_platform(config):
    current = config.get("update_platform", "github").lower()
    new_platform = "gitea" if current == "github" else "github"
    config["update_platform"] = new_platform
    save_config(config)
    print(colored(f"✅ Platform switched to {new_platform.upper()}", "success"))
    input(colored("\nPress Enter...", "prompt"))


def change_theme(config):
    print(colored("\nAvailable Themes:", "info"))
    for i, t in enumerate(THEMES.keys(), 1):
        print(f"  {i}. {t.capitalize()}")
    try:
        choice = int(input(colored("\nChoose number: ", "prompt"))) - 1
        new_theme = list(THEMES.keys())[choice]
        config["theme"] = new_theme
        global current_theme
        current_theme = THEMES[new_theme]
        save_config(config)
        print(colored(f"✅ Theme changed to {new_theme.capitalize()}!", "success"))
    except:
        print(colored("❌ Invalid choice!", "error"))
    input(colored("\nPress Enter...", "prompt"))


def check_update_option(config):
    update_available, new_content, new_version = check_for_update(config)
    if update_available and new_content:
        if input(
            colored(f"\nUpdate to v{new_version}? (Y/n): ", "success")
        ).strip().lower() in ["", "y", "yes"]:
            perform_update(new_content, new_version)
    else:
        print(colored("✅ You are running the latest version.", "success"))
        input(colored("\nPress Enter...", "prompt"))


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
            bash_aliases_submenu()
        elif "." in choice:
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
            switch_platform(config)  # ← FIXED
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
                    "❌ Invalid choice. Use: 1.2, b, a, m, d, c, r, u, t, p, h, s, l, q",
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
