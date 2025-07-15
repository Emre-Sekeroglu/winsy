
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

# ========== Main App ==========
root = tb.Window(themename="flatly")
root.iconbitmap(resource_path("winsy_icon.ico"))  # << This fixes your error
root.title("WINSY - Windows Is Now Setup Your-way")
root.geometry("700x520")

build_specs_section(root)

for cat, tweaks in categories.items():
    pane = CollapsiblePane(root, text=cat)
    pane.pack(fill="x", padx=20, pady=5)
    for tweak in tweaks:
        build_tweak_ui(pane.subframe, tweak)

root.mainloop()
