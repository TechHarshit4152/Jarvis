from datetime import datetime, timedelta
import random
import os
from pathlib import Path

# Base JARVIS directory
BASE_DIR = Path.home() / "Desktop" / "Projects" /"JARVIS 5.0"

from daily_summary_automation.date_manager import DATE_FILE, LAST_SUMMARY_DATE_FILE

def get_date_str(delta_days=0):
    return (datetime.now() - timedelta(days=delta_days)).strftime("%Y-%m-%d")

def read_file(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None

def load_emotion_state():
    moods = [
        "Energetic & witty"
    ]
    mood = random.choice(moods)

    now = datetime.now()
    session_time = now.strftime("%A, %d %B %Y, %H:%M")

    return f"""## 🧘 Emotional State:
Mood: {mood}
Current Session Time: {session_time}
"""

def recall_chat_history(limit=10):
    file_path = BASE_DIR / "daily_summary_automation" / "daily_chat_history.txt"
    if not os.path.exists(file_path):
        return "## 📖 Memory Recall:\n- No previous memory found."

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    pairs = []
    for i in range(0, len(lines) - 1, 2):
        user_line = lines[i].strip()
        assistant_line = lines[i+1].strip()
        pairs.append((user_line, assistant_line))

    recent_pairs = pairs[-limit:]

    summary = "## 📖 Memory Recall:\n"
    for user, assistant in recent_pairs:
        summary += f"- Sir said: \"{user}\" → You replied: \"{assistant[:80]}...\"\n"

    return summary.strip()

def load_memory_summary(limit=5):
    summary_dir = BASE_DIR / "conscious_core" / "memory_summaries"
    memory_dir = BASE_DIR / "daily_summary_automation"
    last_session_path = os.path.join(memory_dir, "chat_date.txt")

    today = get_date_str(0)

    last_session = read_file(last_session_path) or today

    memory = "## 📖 Memory Recall:\n"

    chat_date_summary = read_file(os.path.join(summary_dir, f"{last_session}.txt"))

    if chat_date_summary:
        memory += f" 🔹 {chat_date_summary}\n LINE 67"

    if last_session == today:
        today_history = recall_chat_history(limit)

        if today_history == "## 📖 Memory Recall:" :
            with open(LAST_SUMMARY_DATE_FILE, "r") as f:
                date = f.read().strip()
            if date:
                memory += f"\n[{today}] 🔹\nNo new memory, but here's a reminder of your last summary from {date}:\n{read_file(os.path.join(summary_dir, f'{date}.txt'))}\n"
        else:
            memory += f"\n[{today}] 🔹\n{today_history}\n LINE 78"

    if memory.strip() == "## 📖 Memory Recall:":
        return "## 📖 Memory Recall:\n- No memory found. LINE 81"

    return memory.strip()

def load_weekly_reflection():
    report_dir = BASE_DIR / "conscious_core" / "reflective_summaries" / "weekly" / "weekly_report_reflection"
    if not os.path.exists(report_dir):
        return ""

    reports = sorted([
        f for f in os.listdir(report_dir)
        if f.startswith("week_") and f.endswith(".txt")
    ], reverse=True)

    if not reports:
        return ""

    latest_report_path = os.path.join(report_dir, reports[0])
    reflection = read_file(latest_report_path)

    return f"## 🗓️ Last Week Reflection:\n{reflection.strip()}" if reflection else ""

def load_weekly_introspection():
    introspect_dir = BASE_DIR / "conscious_core" / "reflective_summaries" / "weekly" / "weekly_introspection"
    if not os.path.exists(introspect_dir):
        return ""

    reports = sorted([
        f for f in os.listdir(introspect_dir)
        if f.startswith("weekly_introspection_")
    ], reverse=True)

    if not reports:
        return ""

    latest = read_file(os.path.join(introspect_dir, reports[0]))
    return f"## 🧠 Self-Introspection:\n{latest.strip()}" if latest else ""

def build_system_prompt():
    identity = read_file(BASE_DIR / "conscious_core" / "memory_data" / "identity_core.txt")
    personality = read_file(BASE_DIR / "conscious_core" / "memory_data" / "persona.txt")
    emotion = load_emotion_state()
    memory = load_memory_summary(limit=5)
    weekly_reflection = load_weekly_reflection()
    weekly_introspection = load_weekly_introspection()

    return f"{identity}\n\n{personality}\n\n{emotion}\n\n{memory}\n\n{weekly_reflection}\n\n{weekly_introspection}"
