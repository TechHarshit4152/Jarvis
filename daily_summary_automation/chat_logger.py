import os
from datetime import datetime
from daily_summary_automation.date_manager import write_today_date, read_stored_date, save_last_summary_date
from utils.print_strm import print_strm


CHAT_FILE = "daily_summary_automation/daily_chat_history.txt"


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M")

def save_summary(summary):
    date = read_stored_date()
    summary_file = f"C:\\Users\\Harshit\\Desktop\\JARVIS 5.0\\conscious_core\\memory_summaries\\{date}.txt"
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(summary)


def reset_chat_file():
    open(CHAT_FILE, "w", encoding="utf-8").close()


def append_log(line: str):
    with open(CHAT_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def log_chat(user_input: str, jarvis_output: str):
    """
    Logs conversation in required format
    """

 

    timestamp = get_timestamp()

    if user_input.strip():
        append_log(f"[{timestamp}] User: {user_input}")

    if jarvis_output.strip():
        append_log(f"[{timestamp}] JARVIS: {jarvis_output}")


def handle_new_day():
    print("⚡ New Day Detected → Processing Summary...")

    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r", encoding="utf-8") as f:
            chat_history = f.read()

        if chat_history.strip():
            summary = process_summary(chat_history)
            save_summary(summary)
            save_last_summary_date()
            
    reset_chat_file()
    write_today_date()


def process_summary(chat_history: str):
    """
    Placeholder — will connect to JARVIS next
    """
    print("🧠 Generating daily summary...")
    date = read_stored_date()

    prompt = f"""
Analyze the conversation and extract structured insights from your perspective.

Chat:
{chat_history}

And provide a concise daily summary in the following format:

Format:

DATE: {date}

TASKS:
- task (status)

EVENTS:
- key events

LEARNINGS:
- things learned

EMOTIONS:
- user emotional state

INSIGHTS:
- important observations


"""
    
    summary = print_strm(prompt)

    return summary


