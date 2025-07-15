# Winsy

⚠️ **Disclaimer** ⚠️  
Winsy modifies system-level settings. Use responsibly and only if you understand the implications of each tweak. All changes are reversible through the app interface or manually.

---

Winsy is a lightweight desktop application that helps users quickly apply common Windows system tweaks through a modern and minimal GUI.

Whether you're setting up a fresh install, optimizing performance, or decluttering your desktop, Winsy provides essential toggles and power settings to streamline your configuration without digging through the Registry Editor or command line.

---

##  Features

### Registry Tweaks  
Easily toggle options like hiding unnecessary desktop icons or revealing hidden system settings.

### Power Tweaks  
Adjust CPU behavior on AC/DC power modes using the built-in `powercfg` commands. Tweak performance and energy efficiency with one click.

### Live System Sync  
Each toggle automatically syncs with your current system settings to reflect real-time status on startup.

### My PC Specs Panel  
View basic PC details including Windows version, edition, system architecture, motherboard model, and serial number. Includes easy copy-to-clipboard buttons.

### Simple UI with Collapse Support  
A clean, collapsible pane layout categorizes tweaks under Power Tweaks, Personalization, etc.

---

##  How It Works

- Registry Tweaks are handled using the `winreg` module via `registry_utils.py`.
- Power Tweaks are configured via `powercfg` commands (e.g., CPU throttle limits, boost states) defined in `power_utils.py`.
- Tweaks are listed in a centralized config file: `tweaks_config.py`.
- The app auto-detects your current system values and syncs toggle states accordingly on launch.

---

##  Tech Stack

- Python 3.x  
- [ttkbootstrap](https://ttkbootstrap.readthedocs.io/) for themed GUI  
- Native Windows APIs (`winreg`, `powercfg`, `WMI` via PowerShell)

---

##  Permissions

Some features (especially registry or power tweaks) require **administrator privileges** to apply changes successfully. Run the app as Administrator when needed.

---

##  Getting Started

1. Clone this repo or download the latest release.
2. Ensure Python 3 and required dependencies are installed.
3. Run:

```bash
python main.py
```

4. For packaging to `.exe`, use PyInstaller with icon embedding:

```bash
pyinstaller --noconfirm --onefile --windowed --icon=winsy_icon.ico main.py
```

⚠️ **Note:** Windows Defender will flag the package as a **Trojan**, which is a **false positive**.
