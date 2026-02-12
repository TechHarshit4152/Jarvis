from datetime import datetime, timedelta
import os
from utils.print_strm import print_strm

<<<<<<< HEAD
WEEK_START_PATH = r"C:\Users\Harshit\Desktop\JARVIS 5.0\conscious_core\reflective_summaries\weekly\week_start.txt"
SUMMARY_FOLDER = r"C:\Users\Harshit\Desktop\JARVIS 5.0\conscious_core\memory_summaries"
WEEKLY_REPORT_FOLDER = r"C:\Users\Harshit\Desktop\JARVIS 5.0\conscious_core\reflective_summaries\weekly\weekly_report_reflection"
INTROSPECTION_FOLDER = r"C:\Users\Harshit\Desktop\JARVIS 5.0\conscious_core\reflective_summaries\weekly\weekly_introspection"
=======
WEEK_START_PATH = r"C:\Users\HP\Desktop\JARVIS 5.0\conscious_core\reflective_summaries\weekly\week_start.txt"
SUMMARY_FOLDER = r"C:\Users\HP\Desktop\JARVIS 5.0\conscious_core\memory_summaries"
WEEKLY_REPORT_FOLDER = r"C:\Users\HP\Desktop\JARVIS 5.0\conscious_core\reflective_summaries\weekly\weekly_report_reflection"
INTROSPECTION_FOLDER = r"C:\Users\HP\Desktop\JARVIS 5.0\conscious_core\reflective_summaries\weekly\weekly_introspection"
>>>>>>> 56a924c9a96ff7f8380a601313a1dc1ec2febae1


def read_week_start():
    if not os.path.exists(WEEK_START_PATH) or os.stat(WEEK_START_PATH).st_size == 0:
        today = datetime.today().strftime("%Y-%m-%d")
        with open(WEEK_START_PATH, "w") as f:
            f.write(today)
        return today
    else:
        with open(WEEK_START_PATH, "r") as f:
            return f.read().strip()

def get_week_dates(start_date_str):
    start = datetime.strptime(start_date_str, "%Y-%m-%d")
    return [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

def gather_summaries(week_dates):
    summaries = []
    for date in week_dates:
        path = os.path.join(SUMMARY_FOLDER, f"{date}.txt")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                summaries.append(f"--- {date} ---\n" + f.read())
    return "\n\n".join(summaries)

def save_text(folder, filename, content):
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(os.path.join(folder, filename), "w", encoding="utf-8") as f:
        f.write(content.strip())

def run_weekly_reflection():
    start_date = read_week_start()
    week_dates = get_week_dates(start_date)
    summaries_text = gather_summaries(week_dates)

    if summaries_text.strip() == "":
        return  # No summaries yet for this week

    # Weekly Reflection Prompt
    prompt = (
        "Summarize the following daily reflections into a structured weekly report.\n"
        "- Extract major accomplishments.\n"
        "- Analyze emotional trends.\n"
        "- Identify productivity highs/lows.\n"
        "- Keep tone warm and personalized to Sir.\n"
        "- Use markdown formatting with headings.\n\n"
        f"{summaries_text}\n\n"
        "...End with a positive reflection or motivational closing statement, as if speaking to Sir directly."
    )

    weekly_summary = print_strm(prompt)
    filename = f"week_{start_date}_to_{week_dates[-1]}.txt"
    save_text(WEEKLY_REPORT_FOLDER, filename, weekly_summary)

    # Self-Introspection Prompt
    introspect_prompt = (
        f"As JARVIS, reflect on your own behavior during the past week. Based on this weekly summary:\n"
        "- What did you do well as an assistant?\n"
        "- Where could you improve emotionally or behaviorally?\n"
        "- Were you proactive enough in helping Sir?\n"
        "- Did your responses align with Sir’s values and emotions?\n"
        "- Set one personal goal for yourself for next week.\n\n"
        f"Weekly Summary:\n{weekly_summary}"
    )

    introspective_response = print_strm(introspect_prompt)
    introspect_filename = f"weekly_introspection_{start_date}_to_{week_dates[-1]}.txt"
    save_text(INTROSPECTION_FOLDER, introspect_filename, introspective_response)

    # Reset week_start.txt for new week
    with open(WEEK_START_PATH, "w") as f:
        f.write(datetime.today().strftime("%Y-%m-%d"))



