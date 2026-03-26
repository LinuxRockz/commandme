```markdown
# 🚀 commandme - Linux Command Menu

**A beautiful, colorized, self-updating Linux command menu with categories, auto-sudo prompts, bash aliases viewer, and support for both GitHub and Gitea.**

## ✨ Features

- **Clean CLI Menu Interface** with categories and color highlighting
- **Auto-Sudo Detection** – intelligently prompts before running privileged commands
- **Self-Updating** – automatically checks for new versions on startup (can be disabled)
- **Dual Platform Support** – works with **GitHub** and **Gitea** (self-hosted)
- **Persistent Configuration** – remembers auto-update preference and update platform
- **Bash Aliases Submenu** – easily view, edit, and source your `.bashrc` and custom bash files
- **Full CRUD Support** – add, modify, delete commands and categories
- **Version Changelog** – built-in changelog viewer
- **Smart Version Bumping** – new versions are automatically detected and displayed
- **Modern System Info** – uses **fastfetch** (fallback to neofetch) for system information

### Menu Options
- `1.2` → Run command (category.command format)
- `b` → Bash Aliases & Sourced Files
- `a` → Add new command
- `m` → Modify command
- `d` → Delete command/category
- `c` → Add new category
- `r` → Refresh menu
- `u` → Check for updates
- `t` → Toggle auto-update (ON/OFF)
- `p` → Switch update platform (GitHub ↔ Gitea)
- `l` → View Changelog
- `q` → Quit


## 📥 Installation

### 1. Download the script
```

```bash
curl -L -o ~/.local/bin/commandme \
  https://raw.githubusercontent.com/LinuxRockz/commandme/main/commandme.py

```

### 2. Make it executable

```bash
chmod +x ~/.local/bin/commandme
```

### 3. Add to PATH (if not already)

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### 4. First run

```bash
commandme
```

The script will create `~/.linux_command_menu.json` (menu data) and `~/.linux_command_menu_config.json` (settings).

---

## ⚙️ Configuration

Edit the top of the script to set your update source:

```python
# Choose your platform
UPDATE_PLATFORM = "github"        # or "gitea"

GITHUB_RAW_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/commandme.py"
GITEA_RAW_URL  = "https://git.yourdomain.com/YOUR_USERNAME/YOUR_REPO/raw/branch/main/commandme.py"
```

**Tip:** Use option `p` inside the menu to switch between GitHub and Gitea without editing the script.

---

## 📋 Changelog

**v1.5** (Latest)
- Added full Gitea support
- Platform switching (`p` option)
- Platform name shown in header
- Updated System Information to use **fastfetch** (with neofetch fallback)

**v1.4**
- Version display in title
- Built-in changelog viewer (`l`)

**v1.3**
- Auto-update toggle

**v1.2**
- Self-updating engine + intelligent auto-sudo

---

## 🛠️ Recommended Setup for GitHub / Gitea

1. Create a repository (e.g. `linux-command-menu`)
2. Upload `commandme.py` to the `main` branch
3. Update the raw URLs in the script
4. (Optional) Make a release so users can easily track versions

---

## 📝 Notes

- Works best on Debian/Ubuntu-based systems (apt commands are pre-configured)
- **System Information** now prefers `fastfetch` (modern replacement for neofetch)
- All changes are saved automatically
- Uses only standard Python libraries + `curl` for updates
- Graceful handling of missing tools (e.g. `fastfetch`, `tree`, `htop`)

---

## 🚀 Quick Start

After installation, just type:

```bash
commandme
```

Enjoy a faster, safer, and more organized way to run your favorite Linux commands!

---

**Made with ❤️ for Linux power users**

*Star the repo if you find it useful!*
```