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
from ui_components import CollapsiblePane
from tweaks_config import TWEAKS
from tweak_ui import build_tweak_ui
from pc_specs import get_pc_specs
import tkinter as tk
from tkinter import ttk
from collections import defaultdict
import json
from tkinter import filedialog
import subprocess
from utils import resource_path, show_info_dialog
import webbrowser

# Categorize tweaks
categories = defaultdict(list)
for tweak in TWEAKS:
    categories[tweak["category"]].append(tweak)


# Clipboard utility
def copy_to_clipboard(root, text):
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()


#  Specs section using CollapsingFrame
def build_specs_section(root):
    specs = get_pc_specs()
    pane = CollapsiblePane(root, text="My PC Specs")
    pane.pack(fill="x", padx=20, pady=(10, 5))
    pane.show_var.set(True)
    pane._toggle()

    for key, value in specs.items():
        row = ttk.Frame(pane.subframe)
        row.pack(fill="x", pady=2)
        ttk.Label(row, text=f"{key}:", width=22, anchor="w").pack(side="left")
        ttk.Label(row, text=value, anchor="w").pack(side="left", padx=(0, 10))
        if "Serial" in key:
            ttk.Button(
                row,
                text="Copy",
                width=8,
                command=lambda v=value: copy_to_clipboard(root, v),
            ).pack(side="right")

    # boot into the bios
    def reboot_to_bios():
        confirm_win = tk.Toplevel(root)
        confirm_win.title("Confirmation")
        confirm_win.iconbitmap(resource_path("winsy_icon.ico"))
        confirm_win.grab_set()  # Make modal
        confirm_win.resizable(False, False)

        tk.Label(
            confirm_win,
            text="Are you sure you want to reboot into BIOS?",
            padx=20,
            pady=15,
        ).pack()

        btn_frame = ttk.Frame(confirm_win)
        btn_frame.pack(pady=10)

        def on_yes():
            confirm_win.destroy()
            try:
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                subprocess.run(
                    "shutdown /r /fw /t 0",
                    shell=True,
                    check=True,
                    startupinfo=startupinfo,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                )
            except subprocess.CalledProcessError:
                show_info_dialog(
                    root,
                    "Error",
                    "Failed to reboot into BIOS.\nYou must run the application as Administrator.",
                )

        def on_no():
            confirm_win.destroy()

        ttk.Button(btn_frame, text="Yes", command=on_yes).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="No", command=on_no).pack(side="left", padx=10)

        # Center the window on the screen
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
    ttk.Label(bios_frame, text="Boot into the BIOS", width=22, anchor="w").pack(
        side="left"
    )
    ttk.Button(bios_frame, text="Reboot", command=reboot_to_bios).pack(
        side="left", padx=(0, 10)
    )


# Main App
root = tb.Window(themename="flatly")
# Custom toggle colour
style = tb.Style()

style.configure(
    "Custom.Roundtoggle.Toolbutton",
    background="#2C3E50",
    foreground="white",
    focuscolor="#2C3E50",
)

style.map(
    "Custom.Roundtoggle.Toolbutton",
    background=[("selected", "#2C3E50"), ("!selected", "#ffffff")],
    foreground=[("selected", "white"), ("!selected", "#2C3E50")],
)
root.iconbitmap(resource_path("winsy_icon.ico"))
root.title(f"Winsy v-{__version__}")
root.geometry("720x800")
root.minsize(720, 400)
root.maxsize(720, root.winfo_screenheight())

root.grid_rowconfigure(0, weight=1)  # scrollable expands
root.grid_rowconfigure(1, weight=0)  # footer stays fixed

# Use grid layout
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Scrollable middle section
middle_frame = ttk.Frame(root)
middle_frame.grid(row=0, column=0, sticky="nsew")

canvas = tk.Canvas(middle_frame, highlightthickness=0)
vsb = ttk.Scrollbar(middle_frame, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=vsb.set)

canvas.pack(side="left", fill="both", expand=True)
vsb.pack(side="right", fill="y")

scroll_frame = ttk.Frame(canvas)

# Create window to hold scrollable content
window_id = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")


def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


scroll_frame.bind("<Configure>", on_configure)


# Force canvas width to match container
def resize_canvas(event):
    canvas.itemconfig(window_id, width=event.width)


canvas.bind("<Configure>", resize_canvas)


# Scroll handler that blocks upward scrolling past top
def _on_mousewheel(event):
    if sys.platform == "darwin":
        delta = event.delta
    else:
        delta = int(event.delta / 120)

    # Only block upward scroll at top
    if delta > 0 and canvas.yview()[0] <= 0.0:
        return

    canvas.yview_scroll(-1 * delta, "units")


# Bind scroll globally only when mouse is over canvas
def enable_scroll_behavior():
    def bind_mousewheel(_):
        root.bind_all("<MouseWheel>", _on_mousewheel)

    def unbind_mousewheel(_):
        root.unbind_all("<MouseWheel>")

    canvas.bind("<Enter>", bind_mousewheel)
    canvas.bind("<Leave>", unbind_mousewheel)


# Build content
build_specs_section(scroll_frame)

apply_controls = []

desktop_icon_tweaks = [t for t in TWEAKS if t.get("is_desktop_icon_toggle") is True]
icon_descriptions = {t["description"] for t in desktop_icon_tweaks}


for cat, tweaks in categories.items():
    pane = CollapsiblePane(scroll_frame, text=cat)
    pane.pack(fill="x", padx=20, pady=5)

    if cat == "Personalization" and desktop_icon_tweaks:
        icon_group = CollapsiblePane(
            pane.subframe, text="Show/Hide Desktop Icons", compact=True
        )
        icon_group.pack(fill="x", padx=0, pady=(0, 5))

        for tweak in desktop_icon_tweaks:
            result = build_tweak_ui(icon_group.subframe, tweak, root)
            if result:
                var, apply_fn = result
                apply_controls.append(
                    {
                        "tweak": tweak,
                        "var": var,
                        "apply": apply_fn,
                        "initial": var.get(),
                    }
                )

    for tweak in tweaks:
        if tweak["description"] in icon_descriptions:
            continue
        result = build_tweak_ui(pane.subframe, tweak, root)
        if result:
            var, apply_fn = result
            apply_controls.append(
                {"tweak": tweak, "var": var, "apply": apply_fn, "initial": var.get()}
            )


enable_scroll_behavior()

# Footer Buttons


def check_for_changes():
    changed = any(ctrl["var"].get() != ctrl["initial"] for ctrl in apply_controls)
    state = "normal" if changed else "disabled"
    apply_btn.config(state=state)
    discard_btn.config(state=state)


def apply():
    any_failed = False

    for ctrl in apply_controls:
        result = ctrl["apply"]()
        if result is False:
            any_failed = True

        ctrl["initial"] = ctrl["var"].get()

    check_for_changes()

    if any_failed:
        show_info_dialog(
            root,
            "Administrator Required",
            "Some settings could not be applied.\nPlease run Winsy as Administrator.",
        )


def discard_changes():
    for ctrl in apply_controls:
        ctrl["var"].set(ctrl["initial"])
    check_for_changes()


def apply_recommended():
    try:
        path = resource_path("profiles/recommended.json")
        with open(path, "r") as f:
            data = json.load(f)
        for ctrl in apply_controls:
            name = ctrl["tweak"]["description"]
            if name in data:
                ctrl["var"].set(data[name])
        check_for_changes()

        show_info_dialog(
            root,
            "Recommended Settings",
            "Recommended settings loaded.\nPress Apply to save changes.",
        )
    except Exception as e:
        print("[RECOMMENDED ERROR]", e)


def load_profile():
    path = filedialog.askopenfilename(
        title="Load Profile", filetypes=[("JSON Files", "*.json")]
    )
    if not path:
        return
    try:
        with open(path, "r") as f:
            data = json.load(f)
        for ctrl in apply_controls:
            name = ctrl["tweak"]["description"]
            if name in data:
                value = data[name]
                if isinstance(ctrl["var"], tk.BooleanVar):
                    ctrl["var"].set(bool(value))
                elif isinstance(ctrl["var"], tk.StringVar):
                    ctrl["var"].set(str(value))
        check_for_changes()
    except Exception as e:
        print("[LOAD ERROR]", e)


def save_profile():
    path = filedialog.asksaveasfilename(
        title="Save Profile As",
        defaultextension=".json",
        filetypes=[("JSON Files", "*.json")],
    )
    if not path:
        return
    try:
        result = {
            ctrl["tweak"]["description"]: ctrl["var"].get() for ctrl in apply_controls
        }
        with open(path, "w") as f:
            json.dump(result, f, indent=2)
        print("[SAVED]", path)
    except Exception as e:
        print("[SAVE ERROR]", e)


# Footer (fixed)
footer = ttk.Frame(root)
footer.grid(row=1, column=0, sticky="ew")

# Left tooltip icon
info_icon = ttk.Label(footer, text="ⓘ", font=("Segoe UI Symbol", 12), cursor="hand2")
info_icon.pack(side="left", padx=(10, 0), pady=8)


def show_about_popup():
    popup = tk.Toplevel(root)
    popup.title("About Winsy")
    popup.iconbitmap(resource_path("winsy_icon.ico"))
    popup.geometry("400x200")
    popup.resizable(False, False)
    popup.grab_set()

    ttk.Label(popup, text=f"Winsy v{__version__}", font=("Segoe UI", 12, "bold")).pack(
        pady=(20, 5)
    )
    ttk.Label(popup, text="Licensed under GNU GPL v3").pack()

    link = ttk.Label(
        popup, text="Visit Support Page", foreground="blue", cursor="hand2"
    )
    link.pack(pady=10)
    link.bind("<Button-1>", lambda e: webbrowser.open("https://winsy.uk/support"))

    ttk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)


info_icon.bind("<Button-1>", lambda e: show_about_popup())

# Right-aligned buttons in correct order
apply_btn = ttk.Button(footer, text="Apply", command=apply)
apply_btn.pack(side="right", padx=(5, 10), pady=8)

discard_btn = ttk.Button(footer, text="Discard", command=discard_changes)
discard_btn.pack(side="right", padx=5, pady=8)

load_btn = ttk.Button(footer, text="Load", command=load_profile)
load_btn.pack(side="right", padx=5, pady=8)

save_btn = ttk.Button(footer, text="Save", command=save_profile)
save_btn.pack(side="right", padx=5, pady=8)

recommended_btn = ttk.Button(footer, text="Recommended", command=apply_recommended)
recommended_btn.pack(side="right", padx=(5, 0), pady=8)

# Initially disable Save, Discard, Apply
save_btn.config(state="disabled")
discard_btn.config(state="disabled")
apply_btn.config(state="disabled")

# Attach change tracking
for ctrl in apply_controls:
    ctrl["var"].trace_add("write", lambda *_, c=ctrl: check_for_changes())


def open_support_link(event):
    import webbrowser

    webbrowser.open("https://winsy.uk/support")


root.mainloop()
