
# Winsy - Windows Tweaking Tool
# Copyright (C) 2025 Winsy.uk
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from winsy_version import __version__
import os
import sys
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
from ui_components import CollapsiblePane
from tweaks_config import TWEAKS
from tweak_ui import build_tweak_ui
from pc_specs import get_pc_specs
import tkinter as tk
from tkinter import ttk
from collections import defaultdict

# ========== Add this function ==========
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# ========== Categorize tweaks ==========
categories = defaultdict(list)
for tweak in TWEAKS:
    categories[tweak["category"]].append(tweak)

# ========== Clipboard utility ==========
def copy_to_clipboard(root, text):
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()

# ========== Specs section using CollapsingFrame ==========
def build_specs_section(root):
    specs = get_pc_specs()
    pane = CollapsiblePane(root, text="My PC Specs")
    pane.pack(fill="x", padx=20, pady=(10, 5))

    for key, value in specs.items():
        row = ttk.Frame(pane.subframe)
        row.pack(fill="x", pady=2)
        ttk.Label(row, text=f"{key}:", width=22, anchor="w").pack(side="left")
        ttk.Label(row, text=value, anchor="w").pack(side="left", padx=(0,10))
        if "Serial" in key:
            ttk.Button(row, text="Copy", width=8,
                       command=lambda v=value: copy_to_clipboard(root, v)).pack(side="right")

# ==== Boot into the bios ====
    import subprocess

    def show_error_dialog(message):
        error_win = tk.Toplevel(root)
        error_win.title("Error")
        error_win.iconbitmap(resource_path("winsy_icon.ico"))
        error_win.grab_set()
        error_win.resizable(False, False)

        tk.Label(error_win, text=message, padx=20, pady=15, fg="red", wraplength=300).pack()
        ttk.Button(error_win, text="OK", command=error_win.destroy).pack(pady=(0, 15))

        error_win.after(0, lambda: center(error_win))

    def center(win):
        win.update_idletasks()
        w = win.winfo_width()
        h = win.winfo_height()
        ws = win.winfo_screenwidth()
        hs = win.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        win.geometry(f"+{x}+{y}")


    def reboot_to_bios():
        confirm_win = tk.Toplevel(root)
        confirm_win.title("Confirmation")
        confirm_win.iconbitmap(resource_path("winsy_icon.ico"))
        confirm_win.grab_set()  # Make modal
        confirm_win.resizable(False, False)

        tk.Label(confirm_win, text="Are you sure you want to reboot into BIOS?", padx=20, pady=15).pack()

        btn_frame = ttk.Frame(confirm_win)
        btn_frame.pack(pady=10)

        def on_yes():
            confirm_win.destroy()
            try:
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                subprocess.run("shutdown /r /fw /t 0", shell=True, check=True, startupinfo=startupinfo, creationflags=subprocess.CREATE_NO_WINDOW)
            except subprocess.CalledProcessError:
                show_error_dialog("Failed to reboot into BIOS.\nYou must run the application as Administrator.")


        def on_no():
            confirm_win.destroy()

        ttk.Button(btn_frame, text="Yes", command=on_yes).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="No", command=on_no).pack(side="left", padx=10)

        confirm_win.after(0, lambda: center(confirm_win))


# ===== Center the window on the screen =====
        confirm_win.update_idletasks()
        w = confirm_win.winfo_width()
        h = confirm_win.winfo_height()
        ws = confirm_win.winfo_screenwidth()
        hs = confirm_win.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        confirm_win.geometry(f"+{x}+{y}")

    bios_frame = ttk.Frame(pane.subframe)
    bios_frame.pack(fill="x", pady=(10, 2))
    ttk.Label(bios_frame, text="Boot into the BIOS", width=22, anchor="w").pack(side="left")
    ttk.Button(bios_frame, text="Reboot", command=reboot_to_bios).pack(side="left", padx=(0, 10))
    

# === Main App ===
root = tb.Window(themename="flatly")
root.iconbitmap(resource_path("winsy_icon.ico"))  # << This fixes your error
root.title(f"Winsy v-{__version__}")
root.geometry("700x520")

build_specs_section(root)

for cat, tweaks in categories.items():
    pane = CollapsiblePane(root, text=cat)
    pane.pack(fill="x", padx=20, pady=5)
    for tweak in tweaks:
        build_tweak_ui(pane.subframe, tweak)

# === About ===
about_frame = ttk.Frame(root)
about_frame.pack(fill="x", padx=20, pady=10)

about_text = (
    f"Winsy v{__version__} by Emre Sekeroglu | "
    f"Licensed under GPLv3 | Support: https://winsy.uk/support"
)
label = ttk.Label(about_frame, text=about_text, font=("Segoe UI", 8), anchor="center")
label.pack(fill="x")

root.mainloop()
