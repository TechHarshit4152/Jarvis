from utils.print_strm import print_strm
import json
from datetime import datetime
import os


def get_today_str():
    return datetime.now().strftime("%Y-%m-%d")


def handle_exit_procedure():
    memory_dir = r"C:\Users\HP\Desktop\JARVIS 5.0\conscious_core\memory_data"
    today = get_today_str()
    last_session_path = os.path.join(memory_dir, "last_session.txt")
    summary_path = os.path.join(memory_dir, f"{today}.txt")

    # Read last session date
    if os.path.exists(last_session_path):
        with open(last_session_path, "r", encoding="utf-8") as f:
            last_session_date = f.read().strip()
    else:
        last_session_date = None

    # CASE 1: New session today
    if last_session_date != today:
        with open(last_session_path, "w", encoding="utf-8") as f:
            f.write(today)

        print_strm("Hii, I am Jarvis's system (your system). Ask sir that have he wrote today's summary, and then do whatever sir says.")

        # 👇 Let Sir respond before exiting
        followup = input("JARVIS is awaiting your reply before closing: ")
        print_strm(f"{followup}")  # Handle your input one last time

    # CASE 2: Same day, but summary not written
    elif not os.path.exists(summary_path):
        print_strm("Hii, I am Jarvis's system (your system). Ask sir that have he wrote today's summary, and then do whatever sir says.")

        followup = input("JARVIS is awaiting your reply before closing: ")
        print_strm(f"{followup}")


