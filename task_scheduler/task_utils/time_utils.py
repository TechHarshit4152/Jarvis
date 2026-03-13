from datetime import datetime


def get_current_datetime():

    return datetime.now()


def is_task_due(task_date, task_time):

    now = datetime.now()

    task_datetime = datetime.strptime(
        f"{task_date} {task_time}", "%Y-%m-%d %H:%M"
    )

    return now >= task_datetime