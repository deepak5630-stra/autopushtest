import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Handler(FileSystemEventHandler):
    last_time = 0

    def on_modified(self, event):
        if event.is_directory:
            return

        if time.time() - self.last_time < 5:
            return

        self.last_time = time.time()

        print("Change detected... Pushing to GitHub")

        subprocess.run("git add .", shell=True)
        subprocess.run('git commit -m "Auto Update"', shell=True)
        subprocess.run("git push", shell=True)

observer = Observer()
observer.schedule(Handler(), path=".", recursive=True)
observer.start()

print("Watching project... Press Ctrl+C to stop.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()