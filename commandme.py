#!/usr/bin/env python3
"""
Fully Colorized Linux Command Menu with Categories + Optimized Bash/Zsh Aliases Submenu
Auto shell detection + FIXED editor launching
"""

import json
import os
import subprocess
import sys
from pathlib import Path

# Storage file
MENU_FILE = Path.home() / ".linux_command_menu.json"

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


<<<<<<< HEAD
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
        print(
            colored(f"✅ Shell mode set to {config['shell_mode'].upper()}", "success")
        )
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
=======
>>>>>>> 0730dc3 (Menu Fixes)
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
        print(colored(f"✅ Menu saved to {MENU_FILE}", "bright_green"))
    except Exception as e:
        print(colored(f"❌ Error saving menu: {e}", "red"))


def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")


# ====================== Automatic Shell Detection ======================
def detect_current_shell():
    shell_path = os.environ.get("SHELL", "/bin/bash").lower()
    if "zsh" in shell_path:
        return "zsh", "Zsh"
    elif "bash" in shell_path:
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


# ====================== Optimized + FIXED Shell Aliases Submenu ======================
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
    else:  # zsh
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


<<<<<<< HEAD
def source_file(file_path: Path):
    print(colored("\nTo source this file, run:", "warning"))
    print(colored(f"   source '{file_path}'", "success", bold=True))
    input(colored("\nPress Enter to continue...", "prompt"))
=======
def open_in_editor(file_path: Path):
    # FIXED: Better editor detection and handling
    editor = os.environ.get("EDITOR")
    if not editor:
        # Fallback order - most systems have at least one
        for candidate in ["vim", "vi", "nano", "emacs", "micro"]:
            try:
                if subprocess.run(
                    ["which", candidate], capture_output=True, text=True
                ).stdout.strip():
                    editor = candidate
                    break
            except:
                pass
        if not editor:
            editor = "vi"  # absolute last resort

    print(colored(f"→ Opening {file_path.name} with {editor}...", "cyan"))

    try:
        # Use check=False so we don't raise on non-zero exit (some editors do that)
        result = subprocess.run([editor, str(file_path)], check=False)

        if result.returncode == 0:
            print(colored(f"✅ Finished editing {file_path.name}", "bright_green"))
        else:
            print(
                colored(
                    f"→ Editor exited with code {result.returncode} (normal for some editors)",
                    "yellow",
                )
            )

    except FileNotFoundError:
        print(
            colored(f"❌ Editor '{editor}' not found. Install it or set $EDITOR.", "red")
        )
        print(
            colored(f"   Try: sudo apt install vim   or   export EDITOR=vim", "yellow")
        )
    except Exception as e:
        print(colored(f"❌ Failed to launch editor: {e}", "red"))
>>>>>>> 0730dc3 (Menu Fixes)


def source_file(file_path: Path, shell_type="bash"):
    cmd = "." if shell_type == "zsh" else "source"
    print(colored(f"\nTo load changes in {shell_type.upper()}:", "yellow"))
    print(colored(f"   {cmd} '{file_path}'", "bright_green", bold=True))
    print(colored("   (or restart your terminal)", "blue"))
    input(colored("\nPress Enter to continue...", "yellow"))


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

        print(f"   Detected shell → {colored(shell_name, 'bright_green', bold=True)}")
        print()

        print(
            colored("   [1] Bash     [2] Zsh     [d] Detected Shell", "bright_yellow")
        )
        print(colored("   [b] Back to Main Menu", "magenta"))

        choice = input(colored("\nSelect shell: ", "bright_yellow")).strip().lower()

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
            input(colored("   Press Enter...", "yellow"))
            continue

        while True:
            clear_screen()
            print(colored("═" * 78, "blue"))
            print(colored(f"🛠️  {title}".center(78), "bright_blue", bold=True))
            print(colored("═" * 78, "blue"))
            print(f"   Current shell: {colored(shell_name, 'cyan')}")

            shell_files = get_shell_files(shell_type)

            if not shell_files:
                print(colored(f"\n   No {shell_type} config files found.", "yellow"))
                input(colored("\n   Press Enter to go back...", "yellow"))
                break

            print(colored("\n   Available Files:", "bright_cyan"))
            for i, (name, path) in enumerate(shell_files, 1):
                size = path.stat().st_size // 1024
                print(
                    f"   {colored(str(i), 'bright_yellow', bold=True):>2}. "
                    f"{colored(name, 'cyan'):<28} "
                    f"{colored(f'({size} KB)', 'blue')}"
                )

            print(colored("\n   Actions:", "magenta"))
            print("     [1-9]   View file")
            print("     e[1-9]  Edit file     ← Fixed in this version")
            print("     s[1-9]  Show source command")
            print("     b       Back")

            sub = input(colored("\n   Enter choice: ", "bright_yellow")).strip().lower()

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
                        input(colored("\n   Press Enter to continue...", "yellow"))
                except:
                    print(colored("   ❌ Invalid number", "red"))
            else:
                print(colored("   ❌ Invalid option", "red"))


# ====================== Main Menu (unchanged) ======================
def print_main_menu(menu):
    clear_screen()
    print(colored("═" * 78, "blue"))
    print(colored("🚀 LINUX COMMAND MENU".center(78), "bright_green", bold=True))
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
    print(
        f"  {colored('s', 'bright_yellow')}            → Shell Aliases (Auto-detect Bash/Zsh)"
    )
    print(f"  {colored('a', 'bright_yellow')}            → Add new command")
    print(f"  {colored('m', 'bright_yellow')}            → Modify command")
    print(f"  {colored('d', 'bright_yellow')}            → Delete command")
    print(f"  {colored('c', 'bright_yellow')}            → Add new category")
    print(f"  {colored('r', 'bright_yellow')}            → Refresh menu")
    print(f"  {colored('q', 'bright_yellow')}            → Quit")
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
        print(colored(f"❌ Failed with exit code {e.returncode}", "red"))
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


def add_item(menu):
    ...  # (same as before - omitted for brevity)


def add_category(menu):
    ...


def modify_item(menu):
    ...


def delete_item(menu):
    ...


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
            continue
        elif "." in choice:
            cat_num, cmd_id = get_category_and_id(choice)
            if cat_num:
                cat_list = list(menu["categories"].keys())
                if 1 <= cat_num <= len(cat_list):
                    category = cat_list[cat_num - 1]
                    if cmd_id in menu["categories"][category]:
                        run_command(menu["categories"][category][cmd_id]["command"])
                        continue
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
        elif choice == "q":
            print(colored("👋 Goodbye! Stay safe and productive.", "bright_green"))
            break
        else:
            print(
                colored(
                    "❌ Invalid choice. Use e.g. 1.2 or 's' for shell aliases.", "red"
                )
            )
            input(colored("Press Enter...", "yellow"))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(colored("\n\n👋 Exiting gracefully...", "yellow"))
        sys.exit(0)
