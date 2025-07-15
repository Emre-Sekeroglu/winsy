import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
from registry_utils import read_value, write_value
import tkinter as tk
from power_utils import run_powercfg_commands, read_powercfg_value

def build_tweak_ui(root, tweak):
    frame = tk.Frame(root)
    frame.pack(fill="x", padx=10, pady=4)

    label = tk.Label(frame, text=tweak["description"], anchor="w", width=50)
    label.grid(row=0, column=0, sticky="w")

    var = tb.BooleanVar()

    def toggle():
        if tweak.get("type") == "powercfg":
            cmds = tweak["on_cmds"] if var.get() else tweak["off_cmds"]
            success = run_powercfg_commands(cmds)
            print("[TOGGLE][powercfg]", "Success" if success else "Failed")
        else:
            new_val = tweak["on"] if var.get() else tweak["off"]
            success = write_value(tweak["path"], tweak["value"], new_val)
            print("[TOGGLE][registry]", "Success" if success else "Failed")

    switch = tb.Checkbutton(
        frame,
        variable=var,
        bootstyle="success-round-toggle",
        command=toggle
    )
    switch.grid(row=0, column=1, padx=10)

    icon = tb.Label(frame, text="ⓘ", font=("Segoe UI Symbol", 12), cursor="question_arrow")
    icon.grid(row=0, column=2, padx=(5, 0), pady=(2, 0))
    ToolTip(icon, tweak.get("tooltip", "No description available."))

    # --- Add sync logic here ---
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
