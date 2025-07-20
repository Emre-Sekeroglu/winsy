import ttkbootstrap as tb
from ttkbootstrap.constants import *
from registry_utils import read_value, write_value
import tkinter as tk
from power_utils import run_powercfg_commands, read_powercfg_value
from utils import show_info_dialog
import re
import webbrowser

def build_tweak_ui(parent, tweak, root):
    frame = tk.Frame(parent)
    frame.pack(fill="x", padx=10, pady=4)

    label = tk.Label(frame, text=tweak["description"], anchor="w", width=50)
    label.grid(row=0, column=0, sticky="w")

    var = tb.BooleanVar()

    def toggle():
        if tweak.get("type") == "powercfg":
            cmds = tweak["on_cmds"] if var.get() else tweak["off_cmds"]
            success = run_powercfg_commands(cmds)
            print("[TOGGLE][powercfg]", "Success" if success else "Failed")
            return success
        else:
            new_val = tweak["on"] if var.get() else tweak["off"]
            success = write_value(tweak["path"], tweak["value"], new_val)
            print("[TOGGLE][registry]", "Success" if success else "Failed")
            return success

    switch = tb.Checkbutton(
        frame,
        variable=var,
        bootstyle="Custom,round-toggle",
    )
    switch.grid(row=0, column=1, padx=10)

    # Custom Tooltip
    icon = tb.Label(frame, text="ⓘ", font=("Segoe UI Symbol", 12), cursor="question_arrow")
    icon.grid(row=0, column=2, padx=(5, 0), pady=(2, 0))

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
            y = icon.winfo_rooty() + 20
            tooltip_win.geometry(f"+{x}+{y}")

            text_box = tk.Text(
                tooltip_win,
                wrap="word",
                height=6,
                width=50,
                bg="#ffffe0",
                relief="solid",
                bd=1,
                cursor="xterm"
            )
            tooltip_text = tweak.get("tooltip", "No description available.")
            text_box.insert("1.0", tooltip_text)

            # Apply link style for URLs
            url_pattern = r"(https?://[^\s]+)"
            for match in re.finditer(url_pattern, tooltip_text):
                start_idx = f"1.0 + {match.start()} chars"
                end_idx = f"1.0 + {match.end()} chars"
                text_box.tag_add("link", start_idx, end_idx)

            def open_link(event):
                idx = text_box.index(f"@{event.x},{event.y}")
                tags = text_box.tag_names(idx)
                if "link" in tags:
                    url = text_box.get(f"{idx} wordstart", f"{idx} wordend")
                    webbrowser.open(url)

            def on_motion(event):
                idx = text_box.index(f"@{event.x},{event.y}")
                if "link" in text_box.tag_names(idx):
                    text_box.config(cursor="hand2")
                else:
                    text_box.config(cursor="xterm")

            text_box.tag_config("link", foreground="blue", underline=True)
            text_box.bind("<Button-1>", open_link)
            text_box.bind("<Motion>", on_motion)

            # Prevent editing but allow selection
            def ignore_edit(event): return "break"
            text_box.bind("<Key>", ignore_edit)
            text_box.bind("<Control-v>", ignore_edit)
            text_box.bind("<Button-3>", ignore_edit)
            text_box.config(state="normal")
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

        # Sync Logic
    def sync():
        if tweak.get("type") == "powercfg":
            min_ac = read_powercfg_value("ac", "SUB_PROCESSOR", "PROCTHROTTLEMIN")
            min_dc = read_powercfg_value("dc", "SUB_PROCESSOR", "PROCTHROTTLEMIN")
            max_ac = read_powercfg_value("ac", "SUB_PROCESSOR", "PROCTHROTTLEMAX")
            max_dc = read_powercfg_value("dc", "SUB_PROCESSOR", "PROCTHROTTLEMAX")
            boost_ac = read_powercfg_value("ac", "SUB_PROCESSOR", "be337238-0d82-4146-a960-4f3749d470c7")
            boost_dc = read_powercfg_value("dc", "SUB_PROCESSOR", "be337238-0d82-4146-a960-4f3749d470c7")

            print("[SYNC][powercfg] AC min =", min_ac, "| DC min =", min_dc)
            print("[SYNC][powercfg] AC max =", max_ac, "| DC max =", max_dc)
            print("[SYNC][powercfg] AC boost =", boost_ac, "| DC boost =", boost_dc)

            var.set(
                min_ac == 5 and min_dc == 5 and
                max_ac == 100 and max_dc == 100 and
                boost_ac == 0 and boost_dc == 0
            )
        else:
            val = read_value(tweak["path"], tweak["value"])
            print("[SYNC][registry] Value =", val)
            var.set(val == tweak["on"])

    sync()
    
    return (var, toggle)
