import json
from datetime import datetime

from task_scheduler.config import ACTIVE_TASK_FILE, TASK_HISTORY_FILE
from task_scheduler.task_utils.time_utils import is_task_due


# ---------------------------
# File Operations
# ---------------------------

def load_tasks():

    try:
        with open(ACTIVE_TASK_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"tasks": []}


def save_tasks(data):

    with open(ACTIVE_TASK_FILE, "w") as f:
        json.dump(data, f, indent=4)


def load_history():

    try:
        with open(TASK_HISTORY_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"history": []}


def save_history(data):

    with open(TASK_HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ---------------------------
# Task Execution
# ---------------------------

def trigger_task(task):

    print(f"JARVIS REMINDER: {task['task']}")


# ---------------------------
# Scheduler Logic
# ---------------------------

def check_tasks():

    active_data = load_tasks()
    history_data = load_history()

    remaining_tasks = []
    completed_tasks = []

    for task in active_data["tasks"]:

        if task["status"] != "pending":
            remaining_tasks.append(task)
            continue

        date = task["schedule"]["date"]
        time = task["schedule"]["time"]

        if is_task_due(date, time):

            trigger_task(task)

            task["status"] = "completed"
            task["triggered"] = True
            task["completed_at"] = datetime.now().isoformat()

            completed_tasks.append(task)

        else:
            remaining_tasks.append(task)

    # Update active tasks
    active_data["tasks"] = remaining_tasks

    # Add completed tasks to history
    if completed_tasks:
        history_data["history"].extend(completed_tasks)

    save_tasks(active_data)
    save_history(history_data)