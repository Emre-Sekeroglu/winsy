Winsy v0.7 – 2025-08-03
⚠️ Disclaimer: Winsy modifies system-level settings. Use responsibly and only if you understand the implications of each tweak. Some actions require administrator privileges. All changes are reversible through the app or manually.

🧪 Tested only on Windows 11 24H2.

🧭 Overview
Winsy is a lightweight desktop application that simplifies common Windows system tweaks through a clean and modern UI. Whether you're optimizing performance or personalizing your system, Winsy gives you structured, categorized access to critical registry and power settings—no need to mess with regedit, powercfg, or terminal commands.

✨ Features
✅ Registry Tweaks
Toggle system behaviors like shortcut arrows, telemetry, or desktop icons. Handled via winreg in registry_utils.py.

⚡ Power Tweaks
Manage CPU performance, turbo boost, and throttling profiles through powercfg. Supports dropdowns and toggle switches. Defined in power_utils.py.

🔄 Live System Sync
Each tweak reflects the current system state on launch—no guesswork. What you see is what’s configured.

🖥️ My PC Specs Panel
OS version and edition

Architecture

Motherboard model and serial number

Reboot to BIOS with confirmation

Copy buttons for serials

🧩 Simple Collapsible UI
All tweaks are organized into collapsible sections like:

Power Tweaks

Personalization

Network & Privacy

Supports new compact collapsible panes for cleaner layout.

🔧 Profile System
Save/load your tweak profiles as .json

One-click Recommended Profile

Apply/Discard buttons activate intelligently on unsaved changes

💡 Interactive Tooltips
Rich, multiline descriptions

Clickable URLs

Auto-dismiss on hover-out

Cursor changes on link hover

🛠️ How It Works
Registry tweaks: winreg via registry_utils.py

Power tweaks: powercfg via power_utils.py

All tweak definitions in tweaks_config.py

State sync at launch

Packaged with Python + ttkbootstrap

🧪 Tech Stack
Python 3.x

ttkbootstrap (for theming)

Native Windows APIs: winreg, powercfg, subprocess

PyInstaller-based build script

🔐 Permissions
Some tweaks require administrator rights. Winsy checks for admin access at startup and relaunches with elevation if needed. Any failure to apply tweaks will be clearly indicated via an error dialog.

🚀 Getting Started

git clone https://github.com/yourname/winsy
cd winsy
python main.py

📦 To Package as .exe
Basic:
pyinstaller --noconfirm --onefile --windowed --icon=winsy_icon.ico main.py

Enhanced:
python build.py

✅ This auto-generates version.txt, builds with metadata, embeds the icon and loader GIF, and exports checksum files.

🆕 What’s New in v0.7 – 2025-08-03
Save and Load tweak profiles in JSON format
Load Recommended Preset in one click
Apply/Discard buttons now activate on unsaved changes
New Compact Collapsible Panes UI
Tooltips now support clickable URLs
New splash screen and centered startup
Tooltip window styling refinements

Added new tweaks:
Show Advanced Power Settings in Control Panel
CPU Boost Mode dropdown (5 performance options)
Toggle visibility of Computer, User’s Files, Recycle Bin, Network, and Control Panel desktop icons
Improved CPU optimization toggle (5%/100% AC+DC)
Admin elevation check on launch
Cleaned up layout, icon styling, and change tracking system

❗ Known Issues
False Positive Warning: Some antivirus programs (e.g. Windows Defender) may incorrectly flag the .exe as a threat due to being unsigned.

The binary is sent to Microsoft for reputation improvement.

You may safely allow the app if you downloaded it from a trusted source.
