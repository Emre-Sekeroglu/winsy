import tkinter as tk
from tkinter import ttk

class CollapsiblePane(ttk.Frame):
    def __init__(self, parent, text="", compact=False, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.compact = compact
        self.show_var = tk.BooleanVar(value=False)

        self.subframe = ttk.Frame(self)

        if compact:
            self.label_text = text
            self.button = tk.Label(
                self,
                text=f"> {self.label_text}",
                anchor="w",
                cursor="hand2",
                font=("Segoe UI", 10, "underline"),
                fg="black"
            )
            self.button.pack(fill="x", padx=10, pady=(5, 2))
            self.button.bind("<Button-1>", lambda e: self.toggle_compact())
            self.button.bind("<Enter>", lambda e: self.button.config(fg="#2C3E50"))
            self.button.bind("<Leave>", lambda e: self.button.config(fg="black"))
            self._update_arrow()
        else:
            self.label_text = text
            self.button = ttk.Checkbutton(
                self,
                text=text,  # no prefix!
                variable=self.show_var,
                command=self._toggle,
                style="Toolbutton"
            )
            self.button.pack(fill="x", padx=0, pady=5)
            self.show_var.trace_add("write", self._update_arrow)
            self._update_arrow()

    def toggle_compact(self):
        current = self.show_var.get()
        self.show_var.set(not current)
        self._toggle()
        self._update_arrow()

    def _update_arrow(self, *_):
        if self.compact:
            arrow = "˅" if self.show_var.get() else "˃"
            self.button.config(text=f"{self.label_text} {arrow}")
    
    def _toggle(self):
        if self.show_var.get():
            self.subframe.pack(fill="x", padx=0, pady=(0, 5))
        else:
            self.subframe.pack_forget()
