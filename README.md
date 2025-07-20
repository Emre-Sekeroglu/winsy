Winsy

⚠️ Disclaimer
Winsy modifies system-level settings. Use responsibly and only if you understand the implications of each tweak. Some actions require administrator privileges. All changes are reversible through the app or manually.

Overview

Winsy is a lightweight desktop application that simplifies common Windows system tweaks via a clean and modern interface. Whether you're optimizing performance or customizing your setup, Winsy gives you structured access to essential registry and power settings—no need to dig through regedit or the command line.

✨ Features

✅ Registry Tweaks

Toggle system behaviors like hiding shortcut arrows or disabling telemetry. Managed through registry_utils.py using the native winreg API.

⚡ Power Tweaks

Apply power-saving or performance enhancements via powercfg commands for AC/DC modes. Adjust CPU throttling, turbo boost, and more with one click (power_utils.py).

🔄 Live System Sync

Each toggle auto-syncs with your system's actual configuration at launch. See accurate status immediately—no guesswork.

🖥️ My PC Specs Panel

Displays:

OS Version and Edition

System Architecture

Motherboard Model and Serial

Quick copy buttons for serials
Includes Reboot into BIOS with confirmation.


🧩 Simple Collapsible UI

Modern, collapsible panes categorize tweaks under titles like:

Power Tweaks

Personalization

Network & Privacy (etc.)


🔧 Profile System

Load/save tweak profiles to .json

One-click Recommended Profile

Track unsaved changes and disable/enable Apply, Save, Discard intelligently


💡 Interactive Tooltips

Custom hover tooltips with:

Multi-line rich descriptions

Clickable URLs (cursor changes on link hover)

Auto-dismiss behavior on mouse leave


🛠️ How It Works

Registry Tweaks via winreg (see registry_utils.py)

Power Tweaks via powercfg (see power_utils.py)

All tweak definitions live in tweaks_config.py

State sync on app launch reflects real system values

Packaged with Python + ttkbootstrap for a clean theme


🧪 Tech Stack

Python 3.x

ttkbootstrap (GUI theming)

Native Windows APIs: winreg, powercfg, PowerShell (via subprocess)


🔐 Permissions

Some tweaks (especially under the Registry or Power categories) require administrator rights to take effect. Winsy detects permission issues and notifies users with clear error dialogs.

🚀 Getting Started

1. Clone or download this repo

2. Ensure Python 3.x and dependencies are installed

python main.py

3. To package as an .exe (with icon and version info):

pyinstaller --noconfirm --onefile --windowed --icon=winsy_icon.ico main.py

Or use the enhanced build script:

python build.py

> 📦 Automatically generates version.txt, builds the executable with metadata, and creates checksum files.



❗ Known Issue

Windows Defender may incorrectly flag the .exe as a Trojan although the exwcutable is sent to microsoft servers to be whitelisted. If Winfows Defender flags it as a false positive due to low reputation of unsigned executables, you may allow the exe and ignore the message. The source is open and licensed under GPLv3.