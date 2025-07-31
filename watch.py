from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import time
import os

class ReloadHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.restart()

    def restart(self):
        if self.process:
            self.process.kill()
        self.process = subprocess.Popen(["python", "main.py"])

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"🔄 {event.src_path} modified. Reloading...")
            self.restart()

observer = Observer()
handler = ReloadHandler()
observer.schedule(handler, path=".", recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
