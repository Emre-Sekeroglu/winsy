import tkinter as tk
from tkinter import ttk

class CollapsiblePane(ttk.Frame):
    """A single-section collapsible pane with a header toggle."""

    def __init__(self, parent, text="", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.show_var = tk.BooleanVar(value=False)

        self.button = ttk.Checkbutton(
            self,
            text=text,
            variable=self.show_var,
            command=self._toggle,
            style="Toolbutton"
        )
        self.button.pack(fill="x")

        self.subframe = ttk.Frame(self)
        # Start hidden by default

    def _toggle(self):
        if self.show_var.get():
            self.subframe.pack(fill="x", padx=20, pady=5)
        else:
            self.subframe.pack_forget()
