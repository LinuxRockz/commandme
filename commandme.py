#!/usr/bin/env python3
"""
🚀 LINUX COMMAND MENU - v2.3.5
Ruff-compliant + Dracula theme + Fixed Gist version check
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
        except Exception:
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

        url = f"{GIST_RAW_URL}?_={int(time.time())}"
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        for line in r.text.splitlines():
            if line.strip().startswith('VERSION = "'):
                return line.split('"')[1]
    except Exception:
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


# ====================== Shell Aliases Submenu ======================
def detect_current_shell():
    shell_path = os.environ.get("SHELL", "/bin/bash").lower()
    if "zsh" in shell_path:
        return "zsh", "Zsh"
    if "bash" in shell_path:
        return "bash", "Bash"
    try:
        proc = subprocess.run(
            ["ps", "-p", str(os.getppid())], capture_output=True, text=True
        )
        if "zsh" in proc.stdout.lower():
            return "zsh", "Zsh"
        if "bash" in proc.stdout.lower():
            return "bash", "Bash"
    except Exception:
        pass
    return "bash", "Bash"


def get_shell_files(shell_type="bash"):
    home = Path.home()
    files = []
    if shell_type == "bash":
        candidates = [".bashrc", ".bash_aliases", ".bash_profile", ".profile"]
        for name in candidates:
            p = home / name
            if p.exists() and p.is_file():
                files.append((f"~/{name}", p))
        for f in sorted(home.glob(".*_bash")):
            if f.is_file():
                files.append((f"~/{f.name}", f))
    else:
        candidates = [".zshrc", ".zprofile", ".zsh_aliases", ".zlogin", ".profile"]
        for name in candidates:
            p = home / name
            if p.exists() and p.is_file():
                files.append((f"~/{name}", p))
        for f in sorted(home.glob(".*_zsh")):
            if f.is_file():
                files.append((f"~/{f.name}", f))
    return files


def view_file(file_path: Path):
    try:
        print(colored(f"\n📄 {file_path.name} CONTENT", "bright_cyan", bold=True))
        print(colored("═" * 80, "blue"))
        print(file_path.read_text(encoding="utf-8", errors="replace"))
        print(colored("═" * 80, "blue"))
    except Exception as e:
        print(colored(f"❌ Error: {e}", "red"))


def open_in_editor(file_path: Path):
    editor = os.environ.get("EDITOR") or "vim"
    print(colored(f"→ Opening {file_path.name} with {editor}...", "cyan"))
    try:
        subprocess.run([editor, str(file_path)])
        print(colored("✅ Editing finished", "bright_green"))
    except Exception as e:
        print(colored(f"❌ Failed: {e}", "red"))


def source_file(file_path: Path, shell_type="bash"):
    cmd = "." if shell_type == "zsh" else "source"
    print(colored(f"\nTo apply: {cmd} '{file_path}'", "bright_green", bold=True))
    input(colored("\nPress Enter...", "prompt"))


def shell_aliases_submenu():
    current_shell, shell_name = detect_current_shell()
    while True:
        clear_screen()
        print(colored("═" * 78, "header"))
        print(
            colored(
                "🛠️  SHELL ALIASES & CONFIG FILES".center(78), "bright_blue", bold=True
            )
        )
        print(colored("═" * 78, "header"))
        print(f"   Detected: {colored(shell_name, 'bright_green', bold=True)}")
        print(colored("\n   [1] Bash   [2] Zsh   [d] Detected   [b] Back", "prompt"))
        choice = input(colored("\nSelect: ", "prompt")).strip().lower()
        if choice == "b":
            return
        elif choice == "d":
            st, title = current_shell, f"{shell_name.upper()} FILES"
        elif choice == "1":
            st, title = "bash", "BASH FILES"
        elif choice == "2":
            st, title = "zsh", "ZSH FILES"
        else:
            continue

        while True:
            clear_screen()
            print(colored("═" * 78, "header"))
            print(colored(f"🛠️  {title}".center(78), "bright_blue", bold=True))
            print(colored("═" * 78, "header"))

            files = get_shell_files(st)
            if not files:
                print(colored("\n   No files found.", "yellow"))
                input("\n   Press Enter...")
                break

            print(colored("\n   Files:", "bright_cyan"))
            for i, (name, path) in enumerate(files, 1):
                size = path.stat().st_size // 1024
                print(
                    f"   {colored(str(i),'id',bold=True):>2}. {colored(name,'name'):<28} {colored(f'({size}KB)','reset')}"
                )

            print(
                colored(
                    "\n   [1-9] View   e[1-9] Edit   s[1-9] Source   b Back", "extra"
                )
            )
            sub = input(colored("\n   Choice: ", "prompt")).strip().lower()
            if sub == "b":
                break
            elif sub.startswith("e"):
                try:
                    idx = int(sub.lstrip("e")) - 1
                    if 0 <= idx < len(files):
                        open_in_editor(files[idx][1])
                except Exception:
                    print(colored("   ❌ Invalid number", "red"))
            elif sub.startswith("s"):
                try:
                    idx = int(sub.lstrip("s")) - 1
                    if 0 <= idx < len(files):
                        source_file(files[idx][1], st)
                except Exception:
                    print(colored("   ❌ Invalid number", "red"))
            elif sub.isdigit():
                try:
                    idx = int(sub) - 1
                    if 0 <= idx < len(files):
                        view_file(files[idx][1])
                        input(colored("\n   Press Enter...", "prompt"))
                except Exception:
                    print(colored("   ❌ Invalid number", "red"))


def themes_submenu():
    while True:
        clear_screen()
        print(colored("═" * 78, "header"))
        print(colored("🎨 THEMES".center(78), "bright_yellow", bold=True))
        print(colored("═" * 78, "header"))
        print(
            colored("Current theme:", "cyan"),
            colored(load_theme()["name"], "bright_green", bold=True),
        )
        print()

        for i, (key, t) in enumerate(AVAILABLE_THEMES.items(), 1):
            print(
                f"   {colored(str(i), 'id', bold=True)}. {colored(t['name'], 'name')}"
            )

        print(colored("\n   [number] Select & Preview    [b] Back", "extra"))
        ch = input(colored("\n   Choice: ", "prompt")).strip().lower()

        if ch == "b":
            return
        try:
            idx = int(ch) - 1
            theme_key = list(AVAILABLE_THEMES.keys())[idx]
            show_theme_preview(theme_key)
            confirm = (
                input(colored("\nApply this theme? (y/N): ", "prompt")).strip().lower()
            )
            if confirm == "y":
                save_theme(theme_key)
                print(colored("✅ Theme applied!", "bright_green"))
            input(colored("\nPress Enter to continue...", "prompt"))
        except Exception:
            print(colored("   ❌ Invalid choice", "red"))
            input("   Press Enter...")


def print_main_menu(menu):
    clear_screen()
    latest = get_gist_version()
    print(colored("═" * 78, "header"))
    print(colored("🚀 LINUX COMMAND MENU".center(78), "header", bold=True))
    show_version(latest)
    print(colored("═" * 78, "header"))

    cat_list = list(menu["categories"].keys())
    for i, category in enumerate(cat_list, 1):
        print(
            f"\n{colored(f'[{i}]', 'id', bold=True)} {colored(category.upper(), 'category', bold=True)}"
        )
        print(colored("─" * 65, "blue"))
        commands = menu["categories"][category]
        for key in sorted(
            commands.keys(), key=lambda x: int(x) if x.isdigit() else 999
        ):
            item = commands[key]
            preview = (
                (item["command"][:50] + "...")
                if len(item["command"]) > 50
                else item["command"]
            )
            print(
                f"    {colored(key, 'id', bold=True):<4} {colored(item['name'], 'name'):<35} → {colored(preview, 'command')}"
            )

    print(colored("\n" + "═" * 78, "header"))
    print(colored("Extra Options:", "extra"))
    print(f"  {colored('s','prompt')} → Shell Aliases")
    print(f"  {colored('t','prompt')} → Change Theme")
    print(f"  {colored('a','prompt')} → Add command")
    print(f"  {colored('m','prompt')} → Modify")
    print(f"  {colored('d','prompt')} → Delete")
    print(f"  {colored('c','prompt')} → New category")
    print(f"  {colored('r','prompt')} → Refresh")
    print(f"  {colored('u','prompt')} → Self Update")
    print(f"  {colored('q','prompt')} → Quit")
    print(colored("═" * 78, "header"))


def run_command(command):
    print(colored(f"\n🔄 Running: {command}", "bright_green"))
    print(colored("─" * 70, "blue"))
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        print(result.stdout)
        if result.stderr:
            print(colored("Warnings:\n" + result.stderr.strip(), "yellow"))
    except Exception as e:
        print(colored(f"❌ Error: {e}", "red"))
    input(colored("\nPress Enter...", "prompt"))


def get_category_and_id(choice):
    if "." in choice:
        try:
            cat_num, cmd_id = choice.split(".")
            return int(cat_num), cmd_id.strip()
        except Exception:
            return None, None
    return None, choice.strip()


def load_menu():
    if MENU_FILE.exists():
        try:
            with open(MENU_FILE, "r") as f:
                data = json.load(f)
                return (
                    data if "categories" in data else {"categories": {"General": data}}
                )
        except Exception:
            pass
    return {
        "categories": {
            "System Update & Maintenance": {
                "1": {
                    "name": "Update & Upgrade",
                    "command": "sudo apt update && sudo apt upgrade -y",
                },
                "2": {
                    "name": "Full System Cleanup",
                    "command": "sudo apt autoremove -y && sudo apt clean && sudo journalctl --vacuum-time=2weeks",
                },
                "3": {"name": "Update Flatpak", "command": "flatpak update -y"},
            },
            "System Information": {
                "1": {
                    "name": "Quick System Info",
                    "command": "neofetch || uname -a && cat /etc/os-release",
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
                },
                "4": {"name": "Find Files by Name", "command": "find . -name "},
            },
            "Networking": {
                "1": {"name": "Show IP & Interfaces", "command": "ip addr show"},
                "2": {"name": "Listening Ports", "command": "sudo ss -tuln"},
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
                },
            },
            "Security & Permissions": {
                "1": {"name": "Check Failed Logins", "command": "sudo lastb | head"},
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
                },
                "3": {"name": "Disk Errors", "command": "sudo dmesg | grep -i error"},
            },
        }
    }


def save_menu(menu):
    try:
        with open(MENU_FILE, "w") as f:
            json.dump(menu, f, indent=4)
        print(colored(f"✅ Menu saved", "bright_green"))
    except Exception as e:
        print(colored(f"❌ Save error: {e}", "red"))


def add_item(menu):
    print(colored("\nAvailable Categories:", "cyan"))
    cat_list = list(menu["categories"].keys())
    for i, cat in enumerate(cat_list, 1):
        print(f"  {i}. {cat}")
    try:
        cat_choice = int(input(colored("\nCategory number: ", "prompt"))) - 1
        category = cat_list[cat_choice]
        name = input(colored("Command name: ", "prompt")).strip()
        command = input(colored("Command: ", "prompt")).strip()
        if not name or not command:
            return menu
        commands = menu["categories"][category]
        next_id = str(max([int(k) for k in commands if k.isdigit()] or [0]) + 1)
        commands[next_id] = {"name": name, "command": command}
        print(colored(f"✅ Added '{name}'", "bright_green"))
        save_menu(menu)
    except Exception:
        print(colored("❌ Invalid input", "red"))
    return menu


def add_category(menu):
    name = input(colored("\nNew category name: ", "prompt")).strip()
    if name and name not in menu["categories"]:
        menu["categories"][name] = {}
        print(colored(f"✅ Category '{name}' created", "bright_green"))
        save_menu(menu)
    return menu


def modify_item(menu):
    choice = input(colored("\ncategory.command (e.g. 1.2): ", "prompt")).strip()
    cat_num, cmd_id = get_category_and_id(choice)
    if cat_num is None:
        return menu
    cat_list = list(menu["categories"].keys())
    if not (1 <= cat_num <= len(cat_list)):
        return menu
    category = cat_list[cat_num - 1]
    if cmd_id not in menu["categories"][category]:
        return menu
    item = menu["categories"][category][cmd_id]
    new_name = input(colored(f"New name ({item['name']}): ", "prompt")).strip()
    if new_name:
        item["name"] = new_name
    new_cmd = input(colored(f"New command: ", "prompt")).strip()
    if new_cmd:
        item["command"] = new_cmd
    print(colored("✅ Updated", "bright_green"))
    save_menu(menu)
    return menu


def delete_item(menu):
    choice = (
        input(colored("\nDelete (c)ommand or (cat)egory? ", "prompt")).strip().lower()
    )
    if choice.startswith("cat"):
        cat_list = list(menu["categories"].keys())
        for i, cat in enumerate(cat_list, 1):
            print(f"  {i}. {cat}")
        try:
            num = int(input(colored("\nCategory number: ", "prompt"))) - 1
            if 0 <= num < len(cat_list):
                cat_name = cat_list[num]
                if (
                    input(colored(f"Delete '{cat_name}'? (y/n): ", "red")).lower()
                    == "y"
                ):
                    del menu["categories"][cat_name]
                    print(colored("✅ Category deleted", "bright_green"))
                    save_menu(menu)
        except Exception:
            print(colored("❌ Invalid", "red"))
    else:
        choice = input(colored("Enter category.command: ", "prompt")).strip()
        cat_num, cmd_id = get_category_and_id(choice)
        if cat_num is None:
            return menu
        cat_list = list(menu["categories"].keys())
        if not (1 <= cat_num <= len(cat_list)):
            return menu
        category = cat_list[cat_num - 1]
        if cmd_id in menu["categories"][category]:
            name = menu["categories"][category][cmd_id]["name"]
            if input(colored(f"Delete '{name}'? (y/n): ", "red")).lower() == "y":
                del menu["categories"][category][cmd_id]
                print(colored("✅ Command deleted", "bright_green"))
                if not menu["categories"][category]:
                    del menu["categories"][category]
                save_menu(menu)
    return menu


# ====================== Main Loop ======================
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
            print(colored("✅ Menu refreshed", "bright_green"))
        elif "." in choice:
            cat_num, cmd_id = get_category_and_id(choice)
            if cat_num:
                cat_list = list(menu["categories"].keys())
                if 1 <= cat_num <= len(cat_list):
                    category = cat_list[cat_num - 1]
                    if cmd_id in menu["categories"][category]:
                        run_command(menu["categories"][category][cmd_id]["command"])
        elif choice == "q":
            print(colored("👋 Goodbye!", "bright_green"))
            break
        else:
            print(colored("❌ Invalid choice", "red"))
            input(colored("Press Enter...", "prompt"))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(colored("\n👋 Exiting gracefully...", "yellow"))
        sys.exit(0)
