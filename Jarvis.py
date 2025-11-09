from co_brain import jarvis_loop
from alert.alert import alert
from data.data_dlg import online_dlg, offline_dlg
from voices.speak import speak
from internet_connectivity_check.internet_check import is_online
from os_control.battery_monitor import battery_alert_loop, plug_monitor_loop
from brain.brain import Main_Brain
import threading
import random


def get_greeting():
    """Returns a random greeting based on internet status."""
    if is_online():
        return random.choice(online_dlg)  # ✅ Added return statement
    else:
        return random.choice(offline_dlg)  # ✅ Added return statement

greeting = get_greeting()

def greet():
    """Prints a greeting from get_greeting()."""
    print(f"\n🔵 JARVIS: {greeting}")
    speak(greeting)


def jarvis():
    """Handles greeting and alerting."""
    t1 = threading.Thread(target=greet)
    t2 = threading.Thread(target=lambda: alert(greeting))
    t3 = threading.Thread(target=battery_alert_loop)
    t4 = threading.Thread(target=plug_monitor_loop)

    t3.daemon = True
    t4.daemon = True

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()

if __name__ == "__main__":
    jarvis()
    jarvis_loop()
