#!/usr/bin/env python3
"""
🚀 LINUX COMMAND MENU - v2.2.0
With REAL One-Click Self-Updater from GitHub Gist
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

# === ONE-CLICK UPDATER CONFIG ===
# Create a public GitHub Gist with the full script content and put the RAW URL here:
GIST_RAW_URL = (
    "https://gist.githubusercontent.com/YOUR_USERNAME/YOUR_GIST_ID/raw/commandme.py"
)

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


# ====================== REAL SELF-UPDATER ======================
def self_update():
    clear_screen()
    print(colored("═" * 78, "blue"))
    print(colored("🔄 SELF UPDATER".center(78), "bright_yellow", bold=True))
    print(colored("═" * 78, "blue"))

    if (
        GIST_RAW_URL
        == "https://gist.githubusercontent.com/YOUR_USERNAME/YOUR_GIST_ID/raw/commandme.py"
    ):
        print(colored("❌ Updater not configured yet!", "red"))
        print(colored("\nYou need to:", "yellow"))
        print("1. Copy the full code of this script")
        print("2. Create a new **Public** GitHub Gist named commandme.py")
        print("3. Replace the GIST_RAW_URL above with the Raw URL")
        print("4. Save this file again and run 'u' again")
        input(colored("\nPress Enter...", "yellow"))
        return

    print(colored("→ Checking for newer version...", "cyan"))

    try:
        import requests
    except ImportError:
        print(colored("→ Installing requests (one-time)...", "yellow"))
        subprocess.run([sys.executable, "-m", "pip", "install", "requests"], check=True)
        import requests

    try:
        response = requests.get(GIST_RAW_URL, timeout=15)
        response.raise_for_status()
        new_code = response.text
    except Exception as e:
        print(colored(f"❌ Download failed: {e}", "red"))
        input(colored("\nPress Enter...", "yellow"))
        return

    # Simple version check (look for VERSION = "x.y.z")
    try:
        for line in new_code.splitlines():
            if line.strip().startswith('VERSION = "'):
                new_version = line.split('"')[1]
                break
        else:
            new_version = "unknown"
    except:
        new_version = "unknown"

    if new_version == VERSION:
        print(
            colored(
                f"✅ You are already on the latest version (v{VERSION})", "bright_green"
            )
        )
        input(colored("\nPress Enter...", "yellow"))
        return

    print(colored(f"New version found: v{new_version}", "bright_green"))
    print(colored(f"Current version     : v{VERSION}", "yellow"))

    if input(colored("\nUpdate now? (y/n): ", "bright_yellow")).strip().lower() != "y":
        return

    # Backup current script
    script_path = Path(sys.argv[0]).resolve()
    backup_path = script_path.with_suffix(".py.bak")
    try:
        backup_path.write_text(script_path.read_text())
        print(colored(f"→ Backup created: {backup_path.name}", "blue"))
    except Exception as e:
        print(colored(f"⚠️  Backup failed: {e}", "yellow"))

    # Write new version
    try:
        script_path.write_text(new_code)
        print(colored(f"✅ Successfully updated to v{new_version}", "bright_green"))
        print(colored("\nRestart the script to use the new version.", "bright_cyan"))
    except Exception as e:
        print(colored(f"❌ Failed to write update: {e}", "red"))
        print("Restoring backup...")
        try:
            script_path.write_text(backup_path.read_text())
        except:
            pass

    input(colored("\nPress Enter to continue...", "yellow"))


# ====================== Shell Detection & Aliases Submenu (kept clean) ======================
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
        print(colored(f"❌ Error: {e}", "red"))


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
        print(colored(f"✅ Editing finished", "bright_green"))
    except Exception as e:
        print(colored(f"❌ Failed: {e}", "red"))


def source_file(file_path: Path, shell_type="bash"):
    cmd = "." if shell_type == "zsh" else "source"
    print(
        colored(f"\nTo apply changes: {cmd} '{file_path}'", "bright_green", bold=True)
    )
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
        print(f"   Detected: {colored(shell_name, 'bright_green', bold=True)}")
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
            continue

        while True:
            clear_screen()
            print(colored("═" * 78, "blue"))
            print(colored(f"🛠️  {title}".center(78), "bright_blue", bold=True))
            print(colored("═" * 78, "blue"))

            shell_files = get_shell_files(shell_type)
            if not shell_files:
                print(colored("\n   No files found.", "yellow"))
                input("\n   Press Enter...")
                break

            print(colored("\n   Files:", "bright_cyan"))
            for i, (name, path) in enumerate(shell_files, 1):
                size = path.stat().st_size // 1024
                print(
                    f"   {colored(str(i),'bright_yellow',bold=True):>2}. {colored(name,'cyan'):<28} {colored(f'({size}KB)','blue')}"
                )

            print(
                colored(
                    "\n   [1-9] View   e[1-9] Edit   s[1-9] Source   b Back", "magenta"
                )
            )
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


# ====================== Main Menu ======================
def print_main_menu(menu):
    clear_screen()
    print(colored("═" * 78, "blue"))
    print(colored("🚀 LINUX COMMAND MENU".center(78), "bright_green", bold=True))
    show_version()
    print(colored("═" * 78, "blue"))

    # Categories and commands...
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
    print(f"  {colored('a','bright_yellow')} → Add command")
    print(f"  {colored('m','bright_yellow')} → Modify")
    print(f"  {colored('d','bright_yellow')} → Delete")
    print(f"  {colored('c','bright_yellow')} → New category")
    print(f"  {colored('r','bright_yellow')} → Refresh menu")
    print(f"  {colored('u','bright_yellow')} → Self Update (One-Click)")
    print(f"  {colored('q','bright_yellow')} → Quit")
    print(colored("═" * 78, "blue"))


# ====================== Load / Save / Run / CRUD (same as before) ======================
def load_menu():
    if MENU_FILE.exists():
        try:
            with open(MENU_FILE, "r") as f:
                data = json.load(f)
                return (
                    data if "categories" in data else {"categories": {"General": data}}
                )
        except:
            pass
    # Default menu (same rich categories as previous versions)
    return {"categories": {...}}  # paste your full default menu here if needed


def save_menu(menu):
    try:
        with open(MENU_FILE, "w") as f:
            json.dump(menu, f, indent=4)
        print(colored(f"✅ Saved to {MENU_FILE}", "bright_green"))
    except Exception as e:
        print(colored(f"❌ Save error: {e}", "red"))


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
            print(colored(result.stderr.strip(), "yellow"))
    except Exception as e:
        print(colored(f"❌ Error: {e}", "red"))
    input(colored("\nPress Enter...", "yellow"))


# ... (add_item, add_category, modify_item, delete_item, get_category_and_id)
# Keep the same logic from previous full versions


def main():
    menu = load_menu()
    while True:
        print_main_menu(menu)
        choice = input(colored("\nEnter choice: ", "bright_yellow")).strip().lower()

        if choice == "s":
            shell_aliases_submenu()
        elif choice == "u":
            self_update()
        elif choice == "q":
            print(colored("👋 Goodbye!", "bright_green"))
            break
        # ... handle other choices (a, m, d, c, r, numbered commands)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(colored("\n👋 Exiting...", "yellow"))
        sys.exit(0)
