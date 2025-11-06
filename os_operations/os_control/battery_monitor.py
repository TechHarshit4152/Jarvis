# battery_monitor.py
import psutil
import time
import threading
from voices.speak import speak
from alert.alert import alert
from brain.brain import Main_Brain

def battery_alert_loop():
    already_warned = {
        100: False,
        80: False,
        20: False,
        10: False,
        5: False
    }

    while True:
        battery = psutil.sensors_battery()
        percent = int(battery.percent)
        plugged = battery.power_plugged

        # FULLY CHARGED
        if percent == 100 and plugged and not already_warned[100]:
            speak("100% charged. Please unplug it.")
            alert("Battery full")
            already_warned = {k: False for k in already_warned}
            already_warned[100] = True

        # ABOVE 80
        elif percent >= 80 and plugged and not already_warned[80]:
            speak("Battery is over 80 percent. Please unplug the charger.")
            alert("Unplug Charger")
            already_warned = {k: False for k in already_warned}
            already_warned[80] = True

        # BELOW 20
        elif percent <= 20 and not plugged and not already_warned[20]:
            speak("Battery is low, please plug in the charger.")
            alert("Battery Low")
            already_warned = {k: False for k in already_warned}
            already_warned[20] = True

        # BELOW 10
        elif percent <= 10 and not plugged and not already_warned[10]:
            speak("Warning! Battery is very low.")
            alert("Battery Very Low")
            already_warned = {k: False for k in already_warned}
            already_warned[10] = True

        # BELOW 5
        elif percent <= 5 and not plugged and not already_warned[5]:
            speak("Critical battery level! Charge now.")
            alert("Critical Battery")
            already_warned = {k: False for k in already_warned}
            already_warned[5] = True

        time.sleep(15)

        

def plug_monitor_loop():
    """Detect when charger is plugged/unplugged."""
    prev_state = psutil.sensors_battery().power_plugged
    while True:
        battery = psutil.sensors_battery()
        current_state = battery.power_plugged

        if current_state != prev_state:
            if current_state:
                speak("Charging started.")
                alert("Charging Started")
            else:
                speak("Charging stopped.")
                alert("Charging Stopped")
            prev_state = current_state

        time.sleep(5)


def manual_battery_check():
    battery = psutil.sensors_battery()
    percent = int(battery.percent)
    plugged = battery.power_plugged

    state = "plugged in" if plugged else "not plugged in"
    message = f"The battery is at {percent} percent and the charger is {state}."
    # speak(message)
    return message



