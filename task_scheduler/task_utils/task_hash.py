import hashlib


def generate_task_hash(task, date, time):

    raw = f"{task}_{date}_{time}"

    return hashlib.md5(raw.encode()).hexdigest()