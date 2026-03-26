#!/usr/bin/env python3
"""
Fully Colorized Linux Command Menu with Categories + Bash Aliases + AUTO-SUDO
Self-Updating Version with AUTO-UPDATE DISABLE, VERSION CHANGELOG & AUTO BUMP
Now supports BOTH GitHub and Gitea for updates!
"""

import json
import os
import subprocess
import sys
import hashlib
from pathlib import Path
from datetime import datetime

# ==================== CONFIG & VERSION ====================
MENU_FILE = Path.home() / ".linux_command_menu.json"
CONFIG_FILE = Path.home() / ".linux_command_menu_config.json"

SCRIPT_NAME = "commandme.py"
SCRIPT_PATH = Path.home() / ".local/bin" / SCRIPT_NAME

# ==================== UPDATE SOURCE CONFIG ====================
# Choose your platform: "github" or "gitea"
UPDATE_PLATFORM = "github"   # Change to "gitea" if using self-hosted Gitea

# GitHub example:
# GITHUB_RAW_URL = "https://raw.githubusercontent.com/yourusername/linux-command-menu/main/commandme.py"

# Gitea example (self-hosted):
# GITEA_RAW_URL  = "https://git.landshark.net/Development/CommandMe/raw/branch/main/CommandMe.py"

GITHUB_RAW_URL = "https://raw.githubusercontent.com/yourusername/linux-command-menu/main/commandme.py"
GITEA_RAW_URL  = "https://git.example.com/yourusername/linux-command-menu/raw/branch/main/commandme.py"

CURRENT_VERSION = "1.5"   # ← Auto-bumped on new releases

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

def load_config():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"auto_update": True, "last_update_check": None, "update_platform": UPDATE_PLATFORM}

def save_config(config):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
    except:
        pass

def get_raw_url(config):
    """Return the correct raw URL based on selected platform"""
    platform = config.get("update_platform", UPDATE_PLATFORM).lower()
    if platform == "gitea":
        return GITEA_RAW_URL
    return GITHUB_RAW_URL

def get_local_hash():
    try:
        with open(__file__, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    except:
        return None

# ====================== CHANGELOG ======================
CHANGELOG = """
v1.5  (2026-03-26)
  • Added support for Gitea (self-hosted) in addition to GitHub
  • Configurable update platform (github / gitea)
  • Platform choice saved in config
  • Minor UI improvements

v1.4
  • Version changelog display
  • Automatic version bumping on update
  • Version shown in menu title

v1.3
  • Toggle auto-update ('t')

v1.2
  • Self-updating + auto-sudo
"""

def show_changelog():
    clear_screen()
    print(colored("="*78, "blue"))
    print(colored("📋 COMMANDME CHANGELOG".center(78), "bright_cyan", bold=True))
    print(colored("="*78, "blue"))
    print(CHANGELOG)
    print(colored("="*78, "blue"))
    input(colored("\nPress Enter to return...", "yellow"))

# ====================== UPDATE FUNCTIONS ======================
def check_for_update(config):
    raw_url = get_raw_url(config)
    if not raw_url or "yourusername" in raw_url or "example.com" in raw_url:
        print(colored("⚠️  Update URL not configured yet.", "yellow"))
        return False, None, None
    
    print(colored(f"🔄 Checking for updates via {config.get('update_platform', UPDATE_PLATFORM).upper()}...", "bright_yellow"))
    try:
        result = subprocess.run(
            ["curl", "-s", "-L", "-f", raw_url],
            capture_output=True, text=True, timeout=12
        )
        
        if result.returncode != 0 or not result.stdout.strip():
            return False, None, None
            
        remote_content = result.stdout
        remote_hash = hashlib.sha256(remote_content.encode()).hexdigest()
        local_hash = get_local_hash()
        
        if remote_hash != local_hash:
            new_version = CURRENT_VERSION
            for line in remote_content.splitlines():
                if "CURRENT_VERSION =" in line:
                    try:
                        new_version = line.split("=")[1].strip().strip('"\'')
                        break
                    except:
                        pass
            print(colored(f"✅ New version v{new_version} available!", "bright_green"))
            return True, remote_content, new_version
    except Exception as e:
        print(colored(f"Update check failed: {e}", "yellow"))
    
    return False, None, None

def perform_update(new_content, new_version):
    try:
        SCRIPT_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        backup_path = SCRIPT_PATH.with_suffix('.py.bak')
        if SCRIPT_PATH.exists():
            SCRIPT_PATH.rename(backup_path)
            print(colored(f"✅ Backup: {backup_path}", "blue"))
        
        with open(SCRIPT_PATH, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        SCRIPT_PATH.chmod(0o755)
        
        print(colored(f"🎉 Updated to version {new_version}!", "bright_green"))
        print(colored(f"📍 {SCRIPT_PATH}", "cyan"))
        print(colored("\nRestarting in 3 seconds...", "yellow"))
        import time
        time.sleep(3)
        
        os.execv(sys.executable, [sys.executable, str(SCRIPT_PATH)] + sys.argv[1:])
        
    except Exception as e:
        print(colored(f"❌ Update failed: {e}", "red"))
        input(colored("\nPress Enter...", "yellow"))

def load_menu():
    if MENU_FILE.exists():
        try:
            with open(MENU_FILE, 'r') as f:
                data = json.load(f)
                return data if "categories" in data else {"categories": {"General": data}}
        except:
            pass
    # Default menu remains unchanged
    return {
        "categories": {
            "System Update & Maintenance": {
                "1": {"name": "Update & Upgrade", "command": "sudo apt update && sudo apt upgrade -y", "needs_sudo": True},
                "2": {"name": "Full System Cleanup", "command": "sudo apt autoremove -y && sudo apt clean && sudo journalctl --vacuum-time=2weeks", "needs_sudo": True},
                "3": {"name": "Update Flatpak", "command": "flatpak update -y"}
            },
            "System Information": {
                "1": {"name": "Quick System Info", "command": "fastfetch || uname -a && cat /etc/os-release"},
                "2": {"name": "Disk Usage (Human)", "command": "df -h"},
                "3": {"name": "Memory Usage", "command": "free -h"},
                "4": {"name": "CPU & Load", "command": "uptime && cat /proc/loadavg"}
            },
            "File & Directory Tools": {
                "1": {"name": "List with Details", "command": "ls -lah --color=auto"},
                "2": {"name": "Tree View", "command": "tree -L 2 || echo 'Install tree: sudo apt install tree'"},
                "3": {"name": "Find Large Files", "command": "sudo du -ah / | sort -rh | head -n 20", "needs_sudo": True},
                "4": {"name": "Find Files by Name", "command": "find . -name "}
            },
            "Networking": {
                "1": {"name": "Show IP & Interfaces", "command": "ip addr show"},
                "2": {"name": "Listening Ports", "command": "sudo ss -tuln", "needs_sudo": True},
                "3": {"name": "DNS Resolution", "command": "resolvectl status || cat /etc/resolv.conf"},
                "4": {"name": "Ping Google", "command": "ping -c 4 google.com"}
            },
            "Process Management": {
                "1": {"name": "Interactive Top (htop)", "command": "htop || top"},
                "2": {"name": "List All Processes", "command": "ps aux | less"},
                "3": {"name": "Kill by Name", "command": "pkill -f "},
                "4": {"name": "Find Process by Port", "command": "sudo ss -tlnp | grep ", "needs_sudo": True}
            },
            "Security & Permissions": {
                "1": {"name": "Check Failed Logins", "command": "sudo lastb | head", "needs_sudo": True},
                "2": {"name": "List Open Files", "command": "lsof | less"},
                "3": {"name": "Current User & Groups", "command": "id && groups"}
            },
            "Development Tools": {
                "1": {"name": "Git Status", "command": "git status"},
                "2": {"name": "Docker Status", "command": "docker ps -a"},
                "3": {"name": "Python Virtual Env Info", "command": "python3 -m venv --help | head -5 || echo 'Python venv available'"},
                "4": {"name": "Check Python Packages", "command": "pip list | tail -n 20"}
            },
            "Logs & Monitoring": {
                "1": {"name": "Last 100 System Logs", "command": "journalctl -n 100 --no-pager"},
                "2": {"name": "Tail Auth Log", "command": "sudo tail -f /var/log/auth.log", "needs_sudo": True},
                "3": {"name": "Disk Errors", "command": "sudo dmesg | grep -i error", "needs_sudo": True}
            }
        }
    }

def save_menu(menu):
    try:
        with open(MENU_FILE, 'w') as f:
            json.dump(menu, f, indent=4)
        print(colored(f"✅ Menu saved to {MENU_FILE}", "bright_green"))
    except Exception as e:
        print(colored(f"❌ Error saving: {e}", "red"))

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

# ====================== AUTO SUDO ======================
def needs_sudo(command: str) -> bool:
    sudo_keywords = ['sudo', 'apt ', 'dpkg', 'systemctl', 'journalctl', 'dmesg', 
                     'du -a /', 'ss -', 'lastb', 'lsof', 'mount', 'umount', 
                     'fdisk', 'parted', 'chown', 'chmod -R /', 'rm -rf /']
    return any(kw in command.lower() for kw in sudo_keywords)

def prompt_for_sudo(original_command: str) -> str:
    if 'sudo ' in original_command.lower():
        return original_command
    if not needs_sudo(original_command):
        return original_command
    print(colored("\n🔐 Command requires elevated privileges.", "bright_yellow"))
    print(colored("Run with sudo? (Y/n): ", "yellow"), end='')
    if input().strip().lower() in ['', 'y', 'yes']:
        return f"sudo {original_command}" if not original_command.startswith('sudo ') else original_command
    print(colored("Running without sudo...", "yellow"))
    return original_command

# ====================== Bash Aliases (unchanged) ======================
def get_bash_files():
    home = Path.home()
    bash_files = []
    bashrc = home / ".bashrc"
    if bashrc.exists():
        bash_files.append(("~/.bashrc", bashrc))
    for file in sorted(home.glob(".*_bash")):
        if file.is_file():
            bash_files.append((f"~/{file.name}", file))
    return bash_files

def view_file(file_path: Path):
    try:
        print(colored(f"\n📄 Content of {file_path}", "bright_cyan", bold=True))
        print(colored("="*80, "blue"))
        with open(file_path, 'r', encoding='utf-8') as f:
            print(f.read())
        print(colored("="*80, "blue"))
    except Exception as e:
        print(colored(f"❌ Error: {e}", "red"))

def open_in_editor(file_path: Path):
    editor = os.environ.get('EDITOR', 'nano')
    try:
        subprocess.run([editor, str(file_path)])
        print(colored(f"✅ Opened in {editor}", "bright_green"))
    except Exception as e:
        print(colored(f"❌ Editor failed: {e}", "red"))

def source_file(file_path: Path):
    print(colored(f"\nTo source:", "yellow"))
    print(colored(f"   source '{file_path}'", "bright_green", bold=True))
    input(colored("\nPress Enter...", "yellow"))

def bash_aliases_submenu():
    while True:
        clear_screen()
        print(colored("="*78, "blue"))
        print(colored("🛠️  BASH ALIASES & SOURCED FILES".center(78), "bright_blue", bold=True))
        print(colored("="*78, "blue"))
        bash_files = get_bash_files()
        if not bash_files:
            print(colored("No bash files found.", "yellow"))
            input(colored("\nPress Enter...", "yellow"))
            return
        for i, (name, path) in enumerate(bash_files, 1):
            size = path.stat().st_size // 1024
            print(f"  {colored(str(i), 'bright_yellow', bold=True):>2}. {colored(name, 'cyan')}   {colored(f'({size} KB)', 'blue')}")
        print(colored("\nOptions:", "magenta"))
        print("  [number]     → View")
        print("  e [number]   → Edit")
        print("  s [number]   → Source command")
        print("  b            → Back")
        choice = input(colored("\nEnter choice: ", "bright_yellow")).strip().lower()
        if choice == 'b':
            return
        elif choice.startswith('e '):
            try:
                idx = int(choice[2:]) - 1
                open_in_editor(bash_files[idx][1])
            except:
                print(colored("❌ Invalid!", "red"))
        elif choice.startswith('s '):
            try:
                idx = int(choice[2:]) - 1
                source_file(bash_files[idx][1])
            except:
                print(colored("❌ Invalid!", "red"))
        elif choice.isdigit():
            try:
                idx = int(choice) - 1
                view_file(bash_files[idx][1])
                input(colored("\nPress Enter...", "yellow"))
            except:
                print(colored("❌ Invalid!", "red"))
        else:
            print(colored("❌ Invalid option!", "red"))

# ====================== Main Menu ======================
def print_main_menu(menu, config):
    clear_screen()
    platform = config.get("update_platform", UPDATE_PLATFORM).upper()
    auto_status = colored("ENABLED", "bright_green") if config.get("auto_update", True) else colored("DISABLED", "yellow")
    
    print(colored("="*78, "blue"))
    print(colored("🚀 LINUX COMMAND MENU".center(78), "bright_green", bold=True))
    print(colored(f"   Version {CURRENT_VERSION}  •  {datetime.now().strftime('%Y-%m-%d')}  •  {platform}  •  Auto: {auto_status}".center(78), "blue"))
    print(colored("="*78, "blue"))
    
    cat_list = list(menu["categories"].keys())
    for i, category in enumerate(cat_list, 1):
        print(f"\n{colored(f'[{i}]', 'bright_yellow', bold=True)} {colored(category.upper(), 'bright_cyan', bold=True)}")
        print(colored("-" * 65, "blue"))
        commands = menu["categories"][category]
        for key in sorted(commands.keys(), key=lambda x: int(x) if x.isdigit() else 999):
            item = commands[key]
            preview = (item["command"][:50] + "...") if len(item["command"]) > 50 else item["command"]
            sudo_tag = colored(" [sudo]", "red", bold=True) if item.get("needs_sudo", False) else ""
            print(f"    {colored(key, 'yellow', bold=True):<4} {colored(item['name'], 'green'):<35} → {colored(preview, 'reset')}{sudo_tag}")
    
    print(colored("\n" + "="*78, "blue"))
    print(colored("Extra Options:", "magenta"))
    print(f"  {colored('b', 'bright_yellow')}            → Bash Aliases")
    print(f"  {colored('a', 'bright_yellow')}            → Add command")
    print(f"  {colored('m', 'bright_yellow')}            → Modify")
    print(f"  {colored('d', 'bright_yellow')}            → Delete")
    print(f"  {colored('c', 'bright_yellow')}            → New category")
    print(f"  {colored('r', 'bright_yellow')}            → Refresh menu")
    print(f"  {colored('u', 'bright_yellow')}            → Check for Updates")
    print(f"  {colored('t', 'bright_yellow')}            → Toggle Auto-Update")
    print(f"  {colored('p', 'bright_yellow')}            → Switch Platform (GitHub/Gitea)")
    print(f"  {colored('l', 'bright_yellow')}            → View Changelog")
    print(f"  {colored('q', 'bright_yellow')}            → Quit")
    print(colored("="*78, "blue"))

# ====================== Run & CRUD (mostly unchanged) ======================
def run_command(command):
    final_command = prompt_for_sudo(command)
    print(colored(f"\n🔄 Running: {final_command}", "bright_green"))
    print(colored("-" * 70, "blue"))
    try:
        result = subprocess.run(final_command, shell=True, check=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result.stdout)
        if result.stderr:
            print(colored("Warnings:\n" + result.stderr.strip(), "yellow"))
    except subprocess.CalledProcessError as e:
        print(colored(f"❌ Exit code {e.returncode}", "red"))
        if e.stderr: print(e.stderr.strip())
    except Exception as e:
        print(colored(f"❌ Error: {e}", "red"))
    input(colored("\nPress Enter...", "yellow"))

def get_category_and_id(choice):
    if '.' in choice:
        try:
            cat_num, cmd_id = choice.split('.')
            return int(cat_num), cmd_id.strip()
        except:
            return None, None
    return None, choice.strip()

# Add, Modify, Delete, Category functions (kept compact - same logic as v1.4)
def add_item(menu):
    print(colored("\nAvailable Categories:", "cyan"))
    cat_list = list(menu["categories"].keys())
    for i, cat in enumerate(cat_list, 1):
        print(f"  {i}. {cat}")
    try:
        cat_choice = int(input(colored("\nCategory number: ", "yellow"))) - 1
        category = cat_list[cat_choice]
    except:
        print(colored("❌ Invalid!", "red"))
        return menu
    name = input(colored("Command name: ", "yellow")).strip()
    command = input(colored("Linux command: ", "yellow")).strip()
    if not name or not command:
        print(colored("❌ Cannot be empty!", "red"))
        return menu
    commands = menu["categories"][category]
    existing = [int(k) for k in commands if k.isdigit()]
    next_id = str(max(existing) + 1 if existing else 1)
    needs = needs_sudo(command)
    commands[next_id] = {"name": name, "command": command, "needs_sudo": needs}
    sudo_note = colored(" (auto-sudo)", "bright_yellow") if needs else ""
    print(colored(f"✅ Added {name} (ID: {next_id}){sudo_note}", "bright_green"))
    save_menu(menu)
    return menu

def add_category(menu):
    name = input(colored("\nNew category: ", "yellow")).strip()
    if not name or name in menu["categories"]:
        print(colored("❌ Invalid/duplicate!", "red"))
        return menu
    menu["categories"][name] = {}
    print(colored(f"✅ Category '{name}' created!", "bright_green"))
    save_menu(menu)
    return menu

def modify_item(menu):
    choice = input(colored("\ncategory.command (e.g. 1.3): ", "yellow")).strip()
    cat_num, cmd_id = get_category_and_id(choice)
    if cat_num is None:
        print(colored("❌ Wrong format!", "red"))
        return menu
    cat_list = list(menu["categories"].keys())
    if not (1 <= cat_num <= len(cat_list)):
        print(colored("❌ Bad category!", "red"))
        return menu
    category = cat_list[cat_num - 1]
    commands = menu["categories"][category]
    if cmd_id not in commands:
        print(colored("❌ ID not found!", "red"))
        return menu
    item = commands[cmd_id]
    new_name = input(colored(f"New name [{item['name']}]: ", "yellow")).strip()
    if new_name: item['name'] = new_name
    new_cmd = input(colored(f"New command: ", "yellow")).strip()
    if new_cmd:
        item['command'] = new_cmd
        item['needs_sudo'] = needs_sudo(new_cmd)
    print(colored("✅ Updated!", "bright_green"))
    save_menu(menu)
    return menu

def delete_item(menu):
    choice = input(colored("\nDelete (c)ommand or (cat)egory? ", "yellow")).strip().lower()
    if choice.startswith('cat'):
        cat_list = list(menu["categories"].keys())
        for i, cat in enumerate(cat_list, 1):
            print(f"  {i}. {cat}")
        try:
            num = int(input(colored("\nCategory #: ", "yellow"))) - 1
            cat_name = cat_list[num]
            if input(colored(f"Delete '{cat_name}'? (y/n): ", "red")).lower() == 'y':
                del menu["categories"][cat_name]
                print(colored("✅ Category deleted!", "bright_green"))
                save_menu(menu)
        except:
            print(colored("❌ Invalid!", "red"))
    else:
        choice = input(colored("category.command to delete: ", "yellow")).strip()
        cat_num, cmd_id = get_category_and_id(choice)
        if cat_num:
            cat_list = list(menu["categories"].keys())
            if 1 <= cat_num <= len(cat_list):
                category = cat_list[cat_num-1]
                if cmd_id in menu["categories"][category]:
                    name = menu["categories"][category][cmd_id]["name"]
                    if input(colored(f"Delete '{name}'? (y/n): ", "red")).lower() == 'y':
                        del menu["categories"][category][cmd_id]
                        if not menu["categories"][category]:
                            del menu["categories"][category]
                        print(colored("✅ Deleted!", "bright_green"))
                        save_menu(menu)
    return menu

def toggle_auto_update(config):
    config["auto_update"] = not config.get("auto_update", True)
    save_config(config)
    status = "ENABLED" if config["auto_update"] else "DISABLED"
    print(colored(f"✅ Auto-update now {status}", "bright_green" if config["auto_update"] else "yellow"))
    input(colored("\nPress Enter...", "yellow"))

def switch_platform(config):
    current = config.get("update_platform", UPDATE_PLATFORM).lower()
    new_platform = "gitea" if current == "github" else "github"
    config["update_platform"] = new_platform
    save_config(config)
    print(colored(f"✅ Update platform switched to {new_platform.upper()}", "bright_green"))
    print(colored("Make sure the corresponding RAW_URL is set correctly in the script!", "yellow"))
    input(colored("\nPress Enter...", "yellow"))

def check_update_option(config):
    if not config.get("auto_update", True):
        if input(colored("Auto-update disabled. Check anyway? (y/N): ", "yellow")).strip().lower() != 'y':
            return
    update_available, new_content, new_version = check_for_update(config)
    if update_available and new_content:
        if input(colored(f"\nUpdate to v{new_version}? (Y/n): ", "bright_green")).strip().lower() in ['', 'y', 'yes']:
            perform_update(new_content, new_version)
    else:
        print(colored("✅ Latest version.", "bright_green"))
        input(colored("\nPress Enter...", "yellow"))

# ====================== MAIN ======================
def main():
    config = load_config()
    
    if config.get("auto_update", True):
        update_available, new_content, new_version = check_for_update(config)
        if update_available and new_content:
            print(colored(f"\n🚀 New version v{new_version} available via {config.get('update_platform','github').upper()}!", "bright_green"))
            perform_update(new_content, new_version)
            return
    
    menu = load_menu()
    
    while True:
        print_main_menu(menu, config)
        choice = input(colored("\nEnter choice: ", "bright_yellow")).strip().lower()
        
        if choice == 'b':
            bash_aliases_submenu()
        elif '.' in choice:
            cat_num, cmd_id = get_category_and_id(choice)
            if cat_num:
                cat_list = list(menu["categories"].keys())
                if 1 <= cat_num <= len(cat_list):
                    category = cat_list[cat_num - 1]
                    if cmd_id in menu["categories"][category]:
                        run_command(menu["categories"][category][cmd_id]["command"])
        elif choice == 'a':
            menu = add_item(menu)
        elif choice == 'm':
            menu = modify_item(menu)
        elif choice == 'd':
            menu = delete_item(menu)
        elif choice == 'c':
            menu = add_category(menu)
        elif choice == 'r':
            menu = load_menu()
            print(colored("✅ Refreshed!", "bright_green"))
        elif choice == 'u':
            check_update_option(config)
        elif choice == 't':
            toggle_auto_update(config)
        elif choice == 'p':
            switch_platform(config)
        elif choice == 'l':
            show_changelog()
        elif choice == 'q':
            print(colored("👋 Goodbye!", "bright_green"))
            break
        else:
            print(colored("❌ Invalid. Use 1.2, u, t, p, l, q", "red"))
            input(colored("Press Enter...", "yellow"))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(colored("\n\n👋 Exiting gracefully...", "yellow"))
        sys.exit(0)
