import os
from winotify import Notification, audio
from os import getcwd

def alert(Text):
    icon_path = r"C:\Users\Harshit\Desktop\JARVIS 4.0\logo.png"

    toast = Notification(
        app_id="🟢 J.A.R.V.I.S.",
        title=Text,
        duration="long",
        icon=icon_path
    )

    toast.set_audio(audio.Default, loop=False)


    toast.add_actions(label="Click me", launch="")
    toast.add_actions(label="Dismiss", launch="")


    toast.show()










