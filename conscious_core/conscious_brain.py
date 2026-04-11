from datetime import datetime, timedelta
from conscious_core.reflective_summaries.weekly.weekly_reflection import run_weekly_reflection
import os
import subprocess
from pathlib import Path

# Base JARVIS directory
BASE_DIR = Path.home() / "Desktop" / "Projects" /"JARVIS 5.0"

def read_week_start_date():
    path = BASE_DIR / "conscious_core" / "reflective_summaries"/"weekly" /"week_start.txt"
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def check_if_week_completed():
    start_date_str = read_week_start_date()
    if not start_date_str:
        return False

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    today = datetime.now()
    return (today - start_date).days >= 7



def conscious_check():
    if check_if_week_completed():
        run_weekly_reflection()
        print("✅ Weekly reflection generated.")
    else:
        print("ℹ️ Not yet 7 days. No reflection needed.")


