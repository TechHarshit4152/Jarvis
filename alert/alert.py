import os
import platform
import subprocess

# Base directory (works on Linux + Windows)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Icon path
ICON_PATH = os.path.join(BASE_DIR, "logo.png")


def alert(text):
    system = platform.system()

    # -------------------------
    # Windows Notification
    # -------------------------
    if system == "Windows":
        try:
            from winotify import Notification, audio

            toast = Notification(
                app_id="🟢 J.A.R.V.I.S.",
                title="Jarvis Started",
                msg=text[:350],
                duration="long",
                icon=ICON_PATH,
            )

            toast.set_audio(audio.Default, loop=False)

            toast.add_actions(
                label="Dismiss",
                launch=""
            )

            toast.show()

        except ImportError:
            print("winotify not installed.")

    # -------------------------
    # Linux Notification
    # -------------------------
    elif system == "Linux":
        try:
            subprocess.run([
                "notify-send",
                "🟢 J.A.R.V.I.S.",
                text[:350],
                "--icon",
                ICON_PATH
            ])

        except Exception as e:
            print("Linux notification failed:", e)

    else:
        print("Unsupported OS for notifications.")