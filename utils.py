import os
import sys
import tkinter as tk
from tkinter import ttk
import ctypes

def refresh_desktop():
    """Forces Windows to refresh the desktop icons."""
    SHCNE_ASSOCCHANGED = 0x08000000
    SHCNF_IDLIST = 0x0000

    ctypes.windll.shell32.SHChangeNotify(
        SHCNE_ASSOCCHANGED, SHCNF_IDLIST, None, None
    )

def resource_path(relative_path):
    """Get absolute path to resource (handles PyInstaller bundling)."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Show info dialogue
def show_info_dialog(parent, title, message):
    dialog = tk.Toplevel(parent)
    dialog.title(title)
    dialog.iconbitmap(resource_path("winsy_icon.ico"))
    dialog.grab_set()
    dialog.resizable(False, False)

    tk.Label(
        dialog,
        text=message,
        padx=20,
        pady=15,
        wraplength=300,
        fg="red" if title.lower() == "error" else "black"
    ).pack()

    ttk.Button(dialog, text="OK", command=dialog.destroy).pack(pady=(0, 15))

    # Center the dialog
    dialog.update_idletasks()
    w = dialog.winfo_width()
    h = dialog.winfo_height()
    ws = dialog.winfo_screenwidth()
    hs = dialog.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    dialog.geometry(f"+{x}+{y}")