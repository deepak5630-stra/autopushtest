import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

DEBOUNCE_SECONDS = 2

last_change = time.time()


class ChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        global last_change

        if event.is_directory:
            return

        # Ignore Git folder
        if ".git" in event.src_path:
            return

        last_change = time.time()


def git_has_changes():
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True
    )
    return result.stdout.strip() != ""


def auto_push():
    print("Changes detected → Committing & Pushing...")

    subprocess.run(["git", "add", "."])

    subprocess.run([
        "git",
        "commit",
        "-m",
        f"Auto Update {time.strftime('%Y-%m-%d %H:%M:%S')}"
    ])

    subprocess.run(["git", "push"])


observer = Observer()
observer.schedule(ChangeHandler(), ".", recursive=True)
observer.start()

print("Watching project... Press Ctrl+C to stop.")

try:
    while True:
        time.sleep(1)

        if time.time() - last_change >= DEBOUNCE_SECONDS:
            if git_has_changes():
                auto_push()
                last_change = time.time() + 999999

except KeyboardInterrupt:
    observer.stop()

observer.join()