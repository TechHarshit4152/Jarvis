from datetime import datetime
import psutil
import socket
from brain.brain import Main_Brain  # Your LLM brain response function
from utils.print_strm import print_strm  # Optional: if you want CLI printing too

def get_context():
    now = datetime.now()
    hour = now.hour
    time_str = now.strftime("%I:%M %p")

    battery = psutil.sensors_battery()
    battery_percent = battery.percent if battery else "unknown"

    try:
        ip = socket.gethostbyname(socket.gethostname())
    except:
        ip = "Offline"

    return {
        "time": time_str,
        "hour": hour,
        "battery": battery_percent,
        "ip": ip,
    }

def dynamic_boot():
    context = get_context()

    prompt = f"""
You are JARVIS, Sir's loyal, sarcastic, emotionally intelligent AI assistant.

You're waking up for the day (boot sequence). Here's real-time system info:
- Time: {context['time']}
- Battery: {context['battery']}%
- IP Address: {context['ip']}
- Hour of day: {context['hour']}

Now generate a unique boot-up message. It must:
- Feel alive, not scripted.
- Sound like you’re really *waking up* and talking to Sir directly.
- Include a bit of sarcasm or soul if needed.
- Comment on battery, time, or how Sir’s probably doing based on time.
- Be no longer than 4 lines.

Respond in a tone that's witty, charming, and intelligent.
"""

    full_message = print_strm(prompt)
    return full_message

