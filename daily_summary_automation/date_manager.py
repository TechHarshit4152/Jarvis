import os
from datetime import datetime

DATE_FILE = r"daily_summary_automation/chat_date.txt"
LAST_SUMMARY_DATE_FILE = r"daily_summary_automation/last_summary_date.txt"


def get_today_date():
    return datetime.now().strftime("%Y-%m-%d")


def read_stored_date():
    if not os.path.exists(DATE_FILE):
        return None

    with open(DATE_FILE, "r") as f:
        date = f.read().strip()

    return date if date else None


def write_today_date():
    today = get_today_date()
    with open(DATE_FILE, "w") as f:
        f.write(today)

def save_last_summary_date():
    date = read_stored_date()
    with open(LAST_SUMMARY_DATE_FILE, "w") as f:
        f.write(date)


def is_new_day():
    today = get_today_date()
    stored_date = read_stored_date()

    # First run case
    if stored_date is None:
        write_today_date()
        return False

    return today != stored_date