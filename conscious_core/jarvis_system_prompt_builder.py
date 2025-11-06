from datetime import datetime, timedelta
import random
import os

def get_date_str(delta_days=0):
    return (datetime.now() - timedelta(days=delta_days)).strftime("%Y-%m-%d")

def read_file(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None

def load_emotion_state():
    moods = [
        "Focused & inspired", "Reflective & calm", "Energetic & witty", 
        "Playful & sharp", "Caring & alert", "Grounded & loyal"
    ]
    mood = random.choice(moods)

    now = datetime.now()
    session_time = now.strftime("%A, %d %B %Y, %H:%M")

    return f"""## 🧘 Emotional State:
Mood: {mood}
Current Session Time: {session_time}
"""

def recall_chat_history(limit=10):
    file_path = r"C:\Users\Harshit\Desktop\JARVIS 5.0\conscious_core\memory_data\chat_history.txt"
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
    summary_dir = r"C:\Users\Harshit\Desktop\JARVIS 5.0\conscious_core\memory_summaries"
    memory_dir = r"C:\Users\Harshit\Desktop\JARVIS 5.0\conscious_core\memory_data"
    last_session_path = os.path.join(memory_dir, "last_session.txt")

    today = get_date_str(0)
    yesterday = get_date_str(1)

    last_session = read_file(last_session_path) or today

    memory = "## 📖 Memory Recall:\n"

    yesterday_summary = read_file(os.path.join(summary_dir, f"{yesterday}.txt"))
    if yesterday_summary:
        memory += f"[{yesterday}] 🔹 {yesterday_summary}\n"

    if last_session == today:
        today_history = recall_chat_history(limit)
        memory += f"\n[{today}] 🔹\n{today_history}\n"

    if memory.strip() == "## 📖 Memory Recall:":
        return "## 📖 Memory Recall:\n- No memory found."

    return memory.strip()

def load_weekly_reflection():
    report_dir = r"C:\Users\Harshit\Desktop\JARVIS 5.0\conscious_core\reflective_summaries\weekly\weekly_report_reflection"
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
    introspect_dir = r"C:\Users\Harshit\Desktop\JARVIS 5.0\conscious_core\reflective_summaries\weekly\weekly_introspection"
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
    identity = read_file(r"C:\Users\Harshit\Desktop\JARVIS 5.0\conscious_core\memory_data\identity_core.txt")
    personality = read_file(r"C:\Users\Harshit\Desktop\JARVIS 5.0\conscious_core\memory_data\persona.txt")
    emotion = load_emotion_state()
    memory = load_memory_summary(limit=5)
    weekly_reflection = load_weekly_reflection()
    weekly_introspection = load_weekly_introspection()

    return f"{identity}\n\n{personality}\n\n{emotion}\n\n{memory}\n\n{weekly_reflection}\n\n{weekly_introspection}"
