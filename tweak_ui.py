import ttkbootstrap as tb
from ttkbootstrap.constants import *
from registry_utils import read_value, write_value
import tkinter as tk
from tkinter import ttk
from power_utils import run_powercfg_commands, read_powercfg_value
from utils import show_info_dialog
import re
import webbrowser
import subprocess
from utils import refresh_desktop

def make_text_links_clickable(text_widget):
    import re
    import webbrowser

    content = text_widget.get("1.0", "end-1c")
    url_pattern = re.compile(r"(https?://[^\s)\]]+|www\.[^\s)\]]+)")

    for i, match in enumerate(url_pattern.finditer(content)):
        start, end = match.span()
        tag_name = f"link_{i}"

        start_idx = f"1.0 + {start} chars"
        end_idx = f"1.0 + {end} chars"
        text_widget.tag_add(tag_name, start_idx, end_idx)
        text_widget.tag_config(tag_name, foreground="blue", underline=True)

        url = match.group(0)
        if url.startswith("www."):
            url = "https://" + url

        def callback(e, url=url):  # avoid late binding bug
            webbrowser.open(url)

        text_widget.tag_bind(tag_name, "<Enter>", lambda e: text_widget.config(cursor="hand2"))
        text_widget.tag_bind(tag_name, "<Leave>", lambda e: text_widget.config(cursor="arrow"))
        text_widget.tag_bind(tag_name, "<Button-1>", callback)

# create_dropdown_for_global_tweaks
# This function creates a dropdown for global tweaks that are not powercfg specific.
def create_dropdown_tweak(parent, tweak, root):
    row = ttk.Frame(parent)
    row.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(5, 0))

    row.grid_columnconfigure(0, weight=0)
    row.grid_columnconfigure(1, weight=1)
    row.grid_columnconfigure(2, weight=0)

    label = ttk.Label(row, text=tweak["description"])
    label.grid(row=0, column=0, sticky="w")

    options_dict = tweak.get("options", {})
    display_options = list(options_dict.keys())
    

    if "read_current_value" in tweak:
        try:
            current_val = tweak["read_current_value"]()
            if current_val in display_options:
                default_display = current_val
            else:
                print(f"[SYNC WARNING] Unknown value '{current_val}' for {tweak['description']}")
                default_display = tweak.get("default", display_options[0])
        except Exception as e:
            print(f"[SYNC ERROR] Failed to read current value for {tweak['description']}: {e}")
            default_display = tweak.get("default", display_options[0])
    else:
        default_display = tweak.get("default", display_options[0] if display_options else "")

    current_value = tk.StringVar(value=default_display)

    dropdown = ttk.OptionMenu(row, current_value, default_display, *display_options)
    dropdown.grid(row=0, column=1, padx=(10, 10), sticky="e")

    icon = tb.Label(row, text="ⓘ", font=("Segoe UI Symbol", 12), cursor="question_arrow")
    icon.grid(row=0, column=2, padx=(0, 0), sticky="e")

    tooltip_win = None
    is_inside_icon = False
    is_inside_tooltip = False

    def destroy_tooltip():
        nonlocal tooltip_win
        if tooltip_win:
            tooltip_win.destroy()
            tooltip_win = None

    def check_and_destroy():
        if not is_inside_icon and not is_inside_tooltip:
            destroy_tooltip()

    def on_icon_enter(event):
        nonlocal is_inside_icon, tooltip_win
        is_inside_icon = True
        if tooltip_win is None:
            tooltip_win = tk.Toplevel(icon)
            tooltip_win.wm_overrideredirect(True)
            tooltip_win.attributes("-topmost", True)
            x = icon.winfo_rootx() + 20
            y = icon.winfo_rooty()
            tooltip_win.geometry(f"+{x}+{y}")

            text_box = tk.Text(tooltip_win, wrap="word", height=6, width=50, bg="#ffffe0", relief="solid", bd=1, cursor="xterm")
            text_box.insert("1.0", tweak.get("tooltip", "No description available."))
            make_text_links_clickable(text_box) # Make links clickable
            text_box.config(state="disabled")
            text_box.pack()

            def on_tooltip_enter(e):
                nonlocal is_inside_tooltip
                is_inside_tooltip = True

            def on_tooltip_leave(e):
                nonlocal is_inside_tooltip
                is_inside_tooltip = False
                tooltip_win.after(100, check_and_destroy)

            tooltip_win.bind("<Enter>", on_tooltip_enter)
            tooltip_win.bind("<Leave>", on_tooltip_leave)
            text_box.bind("<Enter>", on_tooltip_enter)
            text_box.bind("<Leave>", on_tooltip_leave)

    def on_icon_leave(event):
        nonlocal is_inside_icon
        is_inside_icon = False
        icon.after(100, check_and_destroy)

    icon.bind("<Enter>", on_icon_enter)
    icon.bind("<Leave>", on_icon_leave)

    def apply():
        selected = current_value.get()
        value = options_dict.get(selected)

        if "apply" not in tweak:
            print("[DROPDOWN ERROR] Missing 'apply' key")
            return False

        if value is None:
            print(f"[DROPDOWN ERROR] Selected value not mapped: {selected}")
            return False

        success = tweak["apply"](value)
        if success and "read_current_value" in tweak:
            try:
                synced_val = tweak["read_current_value"]()
                if synced_val in display_options:
                    current_value.set(synced_val)
                else:
                    print(f"[SYNC WARNING] Unexpected post-apply value: '{synced_val}' for {tweak['description']}")
            except Exception as e:
                print(f"[SYNC ERROR] Failed to re-sync value after apply for {tweak['description']}: {e}")
        return success
    return current_value, apply


def build_tweak_ui(parent, tweak, root):
    frame = ttk.Frame(parent)
    frame.pack(fill="x", pady=5)
    frame.grid_columnconfigure(0, weight=1)  # label column expands
    frame.grid_columnconfigure(1, weight=0)  # toggle
    frame.grid_columnconfigure(2, weight=0)  # tooltip

    if tweak.get("type") == "powercfg_dropdown":
        return create_dropdown_tweak(frame, tweak, root)

    var = tb.BooleanVar()
    label = ttk.Label(frame, text=tweak["description"])
    label.grid(row=0, column=0, sticky="w")

    switch = tb.Checkbutton(frame, variable=var, bootstyle="Custom,round-toggle")
    switch.grid(row=0, column=1, padx=(0, 0), sticky="e")

    icon = tb.Label(frame, text="ⓘ", font=("Segoe UI Symbol", 12), cursor="question_arrow")
    icon.grid(row=0, column=2, padx=(0, 0), sticky="e")

    tooltip_win = None
    is_inside_icon = False
    is_inside_tooltip = False

    def destroy_tooltip():
        nonlocal tooltip_win
        if tooltip_win:
            tooltip_win.destroy()
            tooltip_win = None

    def check_and_destroy():
        if not is_inside_icon and not is_inside_tooltip:
            destroy_tooltip()

    def on_icon_enter(event):
        nonlocal is_inside_icon, tooltip_win
        is_inside_icon = True
        if tooltip_win is None:
            tooltip_win = tk.Toplevel(icon)
            tooltip_win.wm_overrideredirect(True)
            tooltip_win.attributes("-topmost", True)
            x = icon.winfo_rootx() + 20
            y = icon.winfo_rooty()
            tooltip_win.geometry(f"+{x}+{y}")

            tooltip_text = tweak.get("tooltip", "No description available.")
            # Create a text box for the tooltip
            text_box = tk.Text(
                tooltip_win,
                wrap="word",
                height=6,
                width=50,
                bg="#ffffe0",
                relief="solid",
                bd=1,
                cursor="arrow"
            )
            text_box.insert("1.0", tooltip_text)
            make_text_links_clickable(text_box) 
            text_box.config(state="disabled")
            text_box.pack()
            def on_tooltip_enter(e): nonlocal is_inside_tooltip; is_inside_tooltip = True
            def on_tooltip_leave(e): nonlocal is_inside_tooltip; is_inside_tooltip = False; tooltip_win.after(100, check_and_destroy)

            tooltip_win.bind("<Enter>", on_tooltip_enter)
            tooltip_win.bind("<Leave>", on_tooltip_leave)
            text_box.bind("<Enter>", on_tooltip_enter)
            text_box.bind("<Leave>", on_tooltip_leave)

    def on_icon_leave(event):
        nonlocal is_inside_icon
        is_inside_icon = False
        icon.after(100, check_and_destroy)

    icon.bind("<Enter>", on_icon_enter)
    icon.bind("<Leave>", on_icon_leave)

    def toggle():
        if tweak.get("type") == "powercfg":
            cmds = tweak["on_cmds"] if var.get() else tweak["off_cmds"]
            return run_powercfg_commands(cmds)
        else:
            new_val = tweak["on"] if var.get() else tweak["off"]
            success = write_value(
                tweak["path"],
                tweak["value"],
                new_val,
                tweak.get("root", "HKEY_LOCAL_MACHINE"),
                create_if_missing=tweak.get("create_if_missing", False)
            )
            if success and tweak.get("refresh_desktop"):
                refresh_desktop()
            return success

    def sync():
        if tweak.get("type") == "powercfg":
            min_ac = read_powercfg_value("ac", "SUB_PROCESSOR", "PROCTHROTTLEMIN")
            min_dc = read_powercfg_value("dc", "SUB_PROCESSOR", "PROCTHROTTLEMIN")
            max_ac = read_powercfg_value("ac", "SUB_PROCESSOR", "PROCTHROTTLEMAX")
            max_dc = read_powercfg_value("dc", "SUB_PROCESSOR", "PROCTHROTTLEMAX")
            var.set(min_ac == 5 and min_dc == 5 and max_ac == 100 and max_dc == 100)
        else:
            val = read_value(tweak["path"], tweak["value"], tweak.get("root", "HKEY_LOCAL_MACHINE"))
            var.set(tweak["on"] == int(val) if val is not None else False)

    sync()
    return var, toggle