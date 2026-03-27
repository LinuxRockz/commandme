#!/usr/bin/env python3
"""
🚀 LINUX COMMAND MENU - v2.2.0
Complete version with One-Click Self-Updater via GitHub Gist
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from datetime import datetime

# ==================== CONFIG ====================
VERSION = "2.2.0"
MENU_FILE = Path.home() / ".linux_command_menu.json"

# ==================== SELF-UPDATER CONFIG ====================
# INSTRUCTIONS:
# 1. Copy the FULL code of this script
# 2. Go to https://gist.github.com and create a NEW PUBLIC gist
# 3. Filename: commandme.py
# 4. Paste the entire code
# 5. Create gist
# 6. Click the "Raw" button on the file
# 7. Copy the URL from browser (it starts with https://gist.githubusercontent.com/)
# 8. Paste it below, replacing the placeholder
GIST_RAW_URL = "https://gist.githubusercontent.com/LinuxRockz/943cfd94340f8b8289edfbdda5f227c6/raw/b18daadcf1d4344ac435789ed110cd9657153167/commandme.py"

# ANSI Colors
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
}


def colored(text, color, bold=False):
    b = C["bold"] if bold else ""
    return f"{b}{C[color]}{text}{C['reset']}"


def show_version():
    print(
        colored(
            f"Linux Command Menu v{VERSION}  •  {datetime.now().strftime('%Y-%m-%d')}",
            "bright_cyan",
        )
    )


def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")


# ====================== REAL ONE-CLICK SELF-UPDATER ======================
def self_update():
    clear_screen()
    print(colored("═" * 78, "blue"))
    print(colored("🔄 ONE-CLICK SELF UPDATER".center(78), "bright_yellow", bold=True))
    print(colored("═" * 78, "blue"))

    if "YOUR_USERNAME" in GIST_RAW_URL or "YOUR_GIST_ID" in GIST_RAW_URL:
        print(colored("❌ Updater not configured!", "red"))
        print(colored("\nPlease follow these steps first:", "yellow"))
        print("1. Create a public GitHub Gist with this full script")
        print("2. Copy the RAW URL")
        print("3. Paste it into GIST_RAW_URL at the top of this file")
        print("4. Save and run again")
        input(colored("\nPress Enter to return...", "yellow"))
        return

    print(colored("→ Downloading latest version...", "cyan"))

    try:
        import requests
    except ImportError:
        print(colored("→ Installing 'requests' library (one-time only)...", "yellow"))
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "requests"],
                check=True,
                capture_output=True,
            )
            import requests

            print(colored("✅ requests installed", "bright_green"))
        except Exception as e:
            print(colored(f"❌ Could not install requests: {e}", "red"))
            print(colored("   Try: pip install requests  manually", "yellow"))
            input(colored("\nPress Enter...", "yellow"))
            return

    try:
        response = requests.get(GIST_RAW_URL, timeout=20)
        response.raise_for_status()
        new_code = response.text
    except Exception as e:
        print(colored(f"❌ Download failed: {e}", "red"))
        print(colored("   Check your internet or GIST_RAW_URL", "yellow"))
        input(colored("\nPress Enter...", "yellow"))
        return

    # Extract new version
    new_version = VERSION
    for line in new_code.splitlines():
        if line.strip().startswith('VERSION = "'):
            try:
                new_version = line.split('"')[1]
                break
            except:
                pass

    if new_version == VERSION:
        print(
            colored(
                f"✅ You already have the latest version (v{VERSION})", "bright_green"
            )
        )
        input(colored("\nPress Enter...", "yellow"))
        return

    print(colored(f"\nNew version available: v{new_version}", "bright_green"))
    print(colored(f"Your current version   : v{VERSION}", "yellow"))

    confirm = input(colored("\nUpdate now? (y/N): ", "bright_yellow")).strip().lower()
    if confirm != "y":
        print(colored("Update cancelled.", "yellow"))
        input(colored("Press Enter...", "yellow"))
        return

    # Backup current script
    script_path = Path(sys.argv[0]).resolve()
    backup_path = script_path.with_name(script_path.name + ".bak")
    try:
        backup_path.write_text(
            script_path.read_text(encoding="utf-8"), encoding="utf-8"
        )
        print(colored(f"→ Backup created → {backup_path.name}", "blue"))
    except Exception as e:
        print(colored(f"⚠️ Backup failed: {e}", "yellow"))

    # Apply update
    try:
        script_path.write_text(new_code, encoding="utf-8")
        print(colored(f"🎉 Successfully updated to v{new_version}!", "bright_green"))
        print(
            colored(
                "\nPlease restart the script for changes to take effect.", "bright_cyan"
            )
        )
    except Exception as e:
        print(colored(f"❌ Failed to save update: {e}", "red"))
        if backup_path.exists():
            try:
                script_path.write_text(
                    backup_path.read_text(encoding="utf-8"), encoding="utf-8"
                )
                print(colored("→ Restored from backup", "yellow"))
            except:
                pass

    input(colored("\nPress Enter to continue...", "yellow"))


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
    except:
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
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            print(f.read())
        print(colored("═" * 80, "blue"))
    except Exception as e:
        print(colored(f"❌ Error reading file: {e}", "red"))


def open_in_editor(file_path: Path):
    editor = os.environ.get("EDITOR")
    if not editor:
        for cand in ["vim", "vi", "nano"]:
            try:
                if subprocess.run(
                    ["which", cand], capture_output=True, text=True
                ).stdout.strip():
                    editor = cand
                    break
            except:
                pass
        editor = editor or "vi"

    print(colored(f"→ Opening {file_path.name} with {editor}...", "cyan"))
    try:
        subprocess.run([editor, str(file_path)])
        print(colored(f"✅ Editing finished for {file_path.name}", "bright_green"))
    except Exception as e:
        print(colored(f"❌ Failed to open editor: {e}", "red"))


def source_file(file_path: Path, shell_type="bash"):
    cmd = "." if shell_type == "zsh" else "source"
    print(colored(f"\nTo apply changes in {shell_type.upper()}:", "yellow"))
    print(colored(f"   {cmd} '{file_path}'", "bright_green", bold=True))
    input(colored("\nPress Enter...", "yellow"))


def shell_aliases_submenu():
    current_shell, shell_name = detect_current_shell()
    while True:
        clear_screen()
        print(colored("═" * 78, "blue"))
        print(
            colored(
                "🛠️  SHELL ALIASES & CONFIG FILES".center(78), "bright_blue", bold=True
            )
        )
        print(colored("═" * 78, "blue"))
        print(f"   Detected shell: {colored(shell_name, 'bright_green', bold=True)}")
        print(
            colored(
                "\n   [1] Bash   [2] Zsh   [d] Detected   [b] Back", "bright_yellow"
            )
        )

        choice = input(colored("\nSelect: ", "bright_yellow")).strip().lower()
        if choice == "b":
            return
        elif choice == "d":
            shell_type = current_shell
            title = f"{shell_name.upper()} FILES"
        elif choice == "1":
            shell_type = "bash"
            title = "BASH FILES"
        elif choice == "2":
            shell_type = "zsh"
            title = "ZSH FILES"
        else:
            print(colored("   ❌ Invalid choice", "red"))
            input("   Press Enter...")
            continue

        while True:
            clear_screen()
            print(colored("═" * 78, "blue"))
            print(colored(f"🛠️  {title}".center(78), "bright_blue", bold=True))
            print(colored("═" * 78, "blue"))
            print(f"   Current shell: {colored(shell_name, 'cyan')}")

            shell_files = get_shell_files(shell_type)
            if not shell_files:
                print(colored("\n   No config files found.", "yellow"))
                input("\n   Press Enter...")
                break

            print(colored("\n   Available Files:", "bright_cyan"))
            for i, (name, path) in enumerate(shell_files, 1):
                size = path.stat().st_size // 1024
                print(
                    f"   {colored(str(i),'bright_yellow',bold=True):>2}. {colored(name,'cyan'):<28} {colored(f'({size}KB)','blue')}"
                )

            print(colored("\n   Actions:", "magenta"))
            print("     [1-9] View    e[1-9] Edit    s[1-9] Source    b Back")
            sub = input(colored("\n   Choice: ", "bright_yellow")).strip().lower()
            if sub == "b":
                break
            elif sub.startswith("e"):
                try:
                    idx = int(sub.lstrip("e")) - 1
                    if 0 <= idx < len(shell_files):
                        open_in_editor(shell_files[idx][1])
                except:
                    print(colored("   ❌ Invalid number", "red"))
            elif sub.startswith("s"):
                try:
                    idx = int(sub.lstrip("s")) - 1
                    if 0 <= idx < len(shell_files):
                        source_file(shell_files[idx][1], shell_type)
                except:
                    print(colored("   ❌ Invalid number", "red"))
            elif sub.isdigit():
                try:
                    idx = int(sub) - 1
                    if 0 <= idx < len(shell_files):
                        view_file(shell_files[idx][1])
                        input(colored("\n   Press Enter...", "yellow"))
                except:
                    print(colored("   ❌ Invalid number", "red"))
            else:
                print(colored("   ❌ Invalid option", "red"))


# ====================== Main Menu ======================
def print_main_menu(menu):
    clear_screen()
    print(colored("═" * 78, "blue"))
    print(colored("🚀 LINUX COMMAND MENU".center(78), "bright_green", bold=True))
    show_version()
    print(colored("═" * 78, "blue"))

    cat_list = list(menu["categories"].keys())
    for i, category in enumerate(cat_list, 1):
        print(
            f"\n{colored(f'[{i}]', 'bright_yellow', bold=True)} {colored(category.upper(), 'bright_cyan', bold=True)}"
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
                f"    {colored(key, 'yellow', bold=True):<4} {colored(item['name'], 'green'):<35} → {colored(preview, 'reset')}"
            )

    print(colored("\n" + "═" * 78, "blue"))
    print(colored("Extra Options:", "magenta"))
    print(f"  {colored('s','bright_yellow')} → Shell Aliases (Bash/Zsh)")
    print(f"  {colored('a','bright_yellow')} → Add new command")
    print(f"  {colored('m','bright_yellow')} → Modify command")
    print(f"  {colored('d','bright_yellow')} → Delete command")
    print(f"  {colored('c','bright_yellow')} → Add new category")
    print(f"  {colored('r','bright_yellow')} → Refresh menu")
    print(f"  {colored('u','bright_yellow')} → Self Update (One-Click via Gist)")
    print(f"  {colored('q','bright_yellow')} → Quit")
    print(colored("═" * 78, "blue"))


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
    except subprocess.CalledProcessError as e:
        print(colored(f"❌ Failed (code {e.returncode})", "red"))
        if e.stderr:
            print(e.stderr.strip())
    except Exception as e:
        print(colored(f"❌ Error: {e}", "red"))
    input(colored("\nPress Enter to continue...", "yellow"))


def get_category_and_id(choice):
    if "." in choice:
        try:
            cat_num, cmd_id = choice.split(".")
            return int(cat_num), cmd_id.strip()
        except:
            return None, None
    return None, choice.strip()


# ====================== CRUD Functions ======================
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

    # Rich default menu
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
        print(colored(f"✅ Menu saved to {MENU_FILE}", "bright_green"))
    except Exception as e:
        print(colored(f"❌ Error saving menu: {e}", "red"))


def add_item(menu):
    print(colored("\nAvailable Categories:", "cyan"))
    cat_list = list(menu["categories"].keys())
    for i, cat in enumerate(cat_list, 1):
        print(f"  {i}. {cat}")
    try:
        cat_choice = int(input(colored("\nChoose category number: ", "yellow"))) - 1
        category = cat_list[cat_choice]
    except:
        print(colored("❌ Invalid category!", "red"))
        return menu
    name = input(colored("Command name: ", "yellow")).strip()
    command = input(colored("Linux command: ", "yellow")).strip()
    if not name or not command:
        return menu
    commands = menu["categories"][category]
    existing = [int(k) for k in commands if k.isdigit()]
    next_id = str(max(existing) + 1 if existing else 1)
    commands[next_id] = {"name": name, "command": command}
    print(colored(f"✅ Added '{name}' (ID: {next_id})", "bright_green"))
    save_menu(menu)
    return menu


def add_category(menu):
    name = input(colored("\nNew category name: ", "yellow")).strip()
    if not name:
        print(colored("❌ Name cannot be empty!", "red"))
        return menu
    if name in menu["categories"]:
        print(colored("❌ Category already exists!", "red"))
        return menu
    menu["categories"][name] = {}
    print(colored(f"✅ New category '{name}' created!", "bright_green"))
    save_menu(menu)
    return menu


def modify_item(menu):
    choice = input(colored("\nEnter category.command (e.g. 1.2): ", "yellow")).strip()
    cat_num, cmd_id = get_category_and_id(choice)
    if cat_num is None:
        print(colored("❌ Use format category.command", "red"))
        return menu
    cat_list = list(menu["categories"].keys())
    if not (1 <= cat_num <= len(cat_list)):
        print(colored("❌ Invalid category number!", "red"))
        return menu
    category = cat_list[cat_num - 1]
    if cmd_id not in menu["categories"][category]:
        print(colored("❌ Command ID not found!", "red"))
        return menu
    item = menu["categories"][category][cmd_id]
    new_name = input(colored(f"New name (current: {item['name']}): ", "yellow")).strip()
    if new_name:
        item["name"] = new_name
    new_cmd = input(
        colored(f"New command (current: {item['command']}): ", "yellow")
    ).strip()
    if new_cmd:
        item["command"] = new_cmd
    print(colored("✅ Command updated!", "bright_green"))
    save_menu(menu)
    return menu


def delete_item(menu):
    choice = (
        input(colored("\nDelete (c)ommand or (cat)egory? ", "yellow")).strip().lower()
    )
    if choice.startswith("cat"):
        cat_list = list(menu["categories"].keys())
        for i, cat in enumerate(cat_list, 1):
            print(f"  {i}. {cat}")
        try:
            num = int(input(colored("\nCategory number: ", "yellow"))) - 1
            if 0 <= num < len(cat_list):
                cat_name = cat_list[num]
                if (
                    input(colored(f"Delete '{cat_name}'? (y/n): ", "red")).lower()
                    == "y"
                ):
                    del menu["categories"][cat_name]
                    print(colored(f"✅ Category deleted!", "bright_green"))
                    save_menu(menu)
        except:
            print(colored("❌ Invalid input!", "red"))
    else:
        choice = input(colored("Enter category.command (e.g. 1.3): ", "yellow")).strip()
        cat_num, cmd_id = get_category_and_id(choice)
        if cat_num is None:
            print(colored("❌ Use format category.command", "red"))
            return menu
        cat_list = list(menu["categories"].keys())
        if not (1 <= cat_num <= len(cat_list)):
            print(colored("❌ Invalid category!", "red"))
            return menu
        category = cat_list[cat_num - 1]
        if cmd_id in menu["categories"][category]:
            name = menu["categories"][category][cmd_id]["name"]
            if input(colored(f"Delete '{name}'? (y/n): ", "red")).lower() == "y":
                del menu["categories"][category][cmd_id]
                print(colored("✅ Command deleted!", "bright_green"))
                if not menu["categories"][category]:
                    del menu["categories"][category]
                save_menu(menu)
    return menu


# ====================== Main Loop ======================
def main():
    menu = load_menu()
    while True:
        print_main_menu(menu)
        choice = (
            input(colored("\nEnter your choice: ", "bright_yellow")).strip().lower()
        )

        if choice == "s":
            shell_aliases_submenu()
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
            print(colored("✅ Menu refreshed!", "bright_green"))
        elif "." in choice:
            cat_num, cmd_id = get_category_and_id(choice)
            if cat_num:
                cat_list = list(menu["categories"].keys())
                if 1 <= cat_num <= len(cat_list):
                    category = cat_list[cat_num - 1]
                    if cmd_id in menu["categories"][category]:
                        run_command(menu["categories"][category][cmd_id]["command"])
        elif choice == "q":
            print(colored("👋 Goodbye! Stay safe and productive.", "bright_green"))
            break
        else:
            print(colored("❌ Invalid choice. Use e.g. 1.2 or 'u' for update.", "red"))
            input(colored("Press Enter...", "yellow"))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(colored("\n\n👋 Exiting gracefully...", "yellow"))
        sys.exit(0)
