from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAT_FILE = os.path.join(BASE_DIR,"memory_data", "chat_history.txt")


def get_timestamp():
    return datetime.now().strftime("[%Y-%m-%d %H:%M]")


def append_to_chat_file(user, assistant):
    with open(CHAT_FILE, "a", encoding="utf-8") as f:
        f.write(f"{get_timestamp()} User: {user}\n")
        f.write(f"{get_timestamp()} JARVIS: {assistant}\n")


def load_memory(limit=10):
    if not os.path.exists(CHAT_FILE):
        return []

    with open(CHAT_FILE, "r", encoding="utf-8") as f:
        lines = f.read().strip().split("\n")

    messages = []
    for line in lines[-limit * 2:]:  # Each convo = 2 lines
        if "User: " in line:
            content = line.split("User: ", 1)[-1]
            timestamp = line.split("]")[0] + "]"
            messages.append({"role": "user", "content": f"{timestamp} {content}"})
        elif "JARVIS: " in line:
            content = line.split("JARVIS: ", 1)[-1]
            timestamp = line.split("]")[0] + "]"
            messages.append({"role": "assistant", "content": f"{timestamp} {content}"})

    return messages
