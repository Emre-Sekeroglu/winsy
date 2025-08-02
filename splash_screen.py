import tkinter as tk
from PIL import Image, ImageTk
from itertools import count
from utils import resource_path

class SplashScreen:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.overrideredirect(True)
        self.top.configure(bg="white")
        self.top.lift()  # bring to front
        self.top.attributes("-topmost", True)

        # Center the window
        self.top.update_idletasks()
        w, h = 400, 240
        ws = self.top.winfo_screenwidth()
        hs = self.top.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        self.top.geometry(f"{w}x{h}+{x}+{y}")

        self.frames = self._load_frames()
        self.label = tk.Label(self.top, bg="white")
        self.label.pack(pady=(30, 10))

        self.msg = tk.Label(
            self.top,
            text="Launching Winsy...",
            font=("Segoe UI", 12),
            bg="white"
        )
        self.msg.pack()

        self.animate()

    def _load_frames(self):
        img = Image.open(resource_path("winsy_loader.gif"))
        frames = []
        try:
            for i in count(0):
                frames.append(ImageTk.PhotoImage(img.copy()))
                img.seek(i + 1)
        except EOFError:
            pass
        return frames

    def animate(self, index=0):
        self.label.config(image=self.frames[index])
        self.top.after(100, self.animate, (index + 1) % len(self.frames))

    def show_for(self, milliseconds=2000):
        self.top.after(milliseconds, self.top.destroy)
