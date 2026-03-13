import json
import uuid
from datetime import datetime

from task_scheduler.config import ACTIVE_TASK_FILE
from task_scheduler.task_utils.task_hash import generate_task_hash


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


# ---------------------------
# CREATE
# ---------------------------

def create_task(task, date, time):

    data = load_tasks()

    task_hash = generate_task_hash(task, date, time)

    # duplicate prevention
    for t in data["tasks"]:
        if t["task_hash"] == task_hash:
            return {
                "status": "error",
                "message": "Task already exists"
            }

    new_task = {
        "id": str(uuid.uuid4()),
        "task": task,
        "task_hash": task_hash,
        "created_at": datetime.now().isoformat(),
        "schedule": {
            "date": date,
            "time": time
        },
        "status": "pending",
        "triggered": False,
        "completed_at": None
    }

    data["tasks"].append(new_task)

    save_tasks(data)

    return {
        "status": "success",
        "action": "create_task",
        "task": new_task
    }


# ---------------------------
# READ
# ---------------------------

def list_tasks():

    data = load_tasks()

    return {
        "status": "success",
        "action": "read_all",
        "tasks": data["tasks"]
    }


def get_task(task_id):

    data = load_tasks()

    for task in data["tasks"]:
        if task["id"] == task_id:
            return {
                "status": "success",
                "action": "find_task",
                "task": task
            }

    return {
        "status": "error",
        "message": "Task not found"
    }


# ---------------------------
# UPDATE
# ---------------------------

def update_task(task_id, task=None, date=None, time=None):

    data = load_tasks()

    for t in data["tasks"]:

        if t["id"] == task_id:

            if task:
                t["task"] = task

            if date:
                t["schedule"]["date"] = date

            if time:
                t["schedule"]["time"] = time

            save_tasks(data)

            return {
                "status": "success",
                "action": "update",
                "task": t
            }

    return {
        "status": "error",
        "message": "Task not found"
    }


# ---------------------------
# DELETE
# ---------------------------

def delete_task(task_id):

    data = load_tasks()

    new_tasks = []

    deleted_task = None

    for task in data["tasks"]:

        if task["id"] == task_id:
            deleted_task = task
            continue

        new_tasks.append(task)

    if not deleted_task:
        return {
            "status": "error",
            "message": "Task not found"
        }

    data["tasks"] = new_tasks

    save_tasks(data)

    return {
        "status": "success",
        "action": "delete",
        "task": deleted_task
    }