import time
import sys
import os
import shutil
from colorama import Fore, Style, init
from playsound import playsound
from datetime import datetime
from psutil import sensors_battery
from internet_connectivity_check.internet_check import is_online
import psutil
import socket
import platform

init(autoreset=True)

def center_text(text):
    columns = shutil.get_terminal_size().columns
    return text.center(columns)

def slow_type(text, delay=0.01):
    # First prepare and center full lines, then type char-by-char
    for line in text.split('\n'):
        centered_line = center_text(line)
        for char in centered_line:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

def print_centered(text, color=Fore.WHITE):
    for line in text.strip('\n').split('\n'):
        print(center_text(color + line + Style.RESET_ALL))

def progress_bar(task, duration=1.5):
    length = 30
    print(center_text(f"{Fore.LIGHTYELLOW_EX}{task}"))
    bar = "[" + " " * length + "]"
    print(center_text(bar), end='')
    sys.stdout.flush()
    sys.stdout.write("\b" * (length + 1))

    start = time.time()
    for _ in range(length):
        sys.stdout.write(Fore.CYAN + "█" + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(duration / length)
    end = time.time()

    elapsed = round(end - start, 2)
    print(Fore.CYAN + "]" + Style.RESET_ALL +
          Fore.GREEN + " [DONE]" + Style.RESET_ALL +
          Fore.LIGHTBLACK_EX + f"  [Time: {elapsed}s]" + Style.RESET_ALL)

def system_status():
    battery = psutil.sensors_battery()
    battery_percent = battery.percent
    charging = "Yes" if battery.power_plugged else "No"

    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    ssid = "N/A"
    if platform.system() == "Windows":
        try:
            import subprocess
            result = subprocess.check_output("netsh wlan show interfaces", shell=True).decode()
            for line in result.split('\n'):
                if "SSID" in line and "BSSID" not in line:
                    ssid = line.split(":")[1].strip()
        except:
            ssid = "Unable to retrieve"

    print()
    print(center_text("📊 " + Fore.LIGHTCYAN_EX + "System Status Report" + Style.RESET_ALL))
    print(center_text(f"🔋 Battery: {battery_percent}%  |  Charging: {charging}"))
    print(center_text(f"🧠 CPU Usage: {cpu}%  |  🧠 RAM Usage: {ram}%"))
    print(center_text(f"🛰️ Network: {ssid}  |  IP: {ip_address}"))
    # print(center_text(f"📌 Today's Priority: {Fore.YELLOW}Study Physics & Revision - 2 hrs{Style.RESET_ALL}"))


def boot_up():
    os.system('cls' if os.name == 'nt' else 'clear')

    ascii_logo = r"""
     
       _           _____ __      __ _____   _____ 
      | |   /\    |  __ \\ \    / /|_   _| / ____|
      | |  /  \   | |__) |\ \  / /   | |  | (___  
  _   | | / /\ \  |  _  /  \ \/ /    | |   \___ \ 
 | |__| |/ ____ \ | | \ \   \  /    _| |_  ____) |
  \____//_/    \_\|_|  \_\   \/    |_____||_____/ 
                                                  
                                                  

        Personal Assistant v4.0
    """
    print_centered(ascii_logo, Fore.LIGHTCYAN_EX)

    # try:
        # playsound("boot_sequence/startup.mp3")
    # except:
        # slow_type(f"{Fore.YELLOW}⚠️  Startup sound failed to play.{Style.RESET_ALL}", 0.002)


    print(center_text(Fore.LIGHTBLACK_EX + "=" * 60))
    slow_type(Fore.LIGHTCYAN_EX + "🔵 Initializing J.A.R.V.I.S. 4.0 Protocol...\n", 0.01)
    time.sleep(0.4)

    

    modules = [
        "🧠 Loading Core Intelligence Engine",
        "🎙️  Activating Voice Recognition System",
        "🌐 Linking Neural Net Interface",
        "📡 Connecting to Internet & OS Modules",
        "🔐 Enabling Command & Security Layers",
        "📈 Optimizing Performance Algorithms",
        "🎵 Syncing Music & Media Channels",
        "⚙️  Spinning up Intent Classifier",
    ]

    for mod in modules:
        progress_bar(mod, duration=1.1)
        time.sleep(0.2)

    print(center_text(Fore.LIGHTBLACK_EX + "=" * 60))
    slow_type(Fore.LIGHTGREEN_EX + "✅ All systems online. J.A.R.V.I.S. 4.0 is ready to serve.\n")

    system_status()

    if is_online():  
        slow_type(Fore.LIGHTBLUE_EX + "🛡️  Network secure. No vulnerabilities detected.\n", 0.01)

    
if __name__ == "__main__":
    boot_up()
