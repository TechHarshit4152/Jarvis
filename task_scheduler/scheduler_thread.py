import threading
import time

from task_scheduler.config import CHECK_INTERVAL
from task_scheduler.task_checker import check_tasks


def scheduler_loop():

    while True:

        try:
            check_tasks()
        except Exception as e:
            print("Scheduler error:", e)

        time.sleep(CHECK_INTERVAL)


def start_scheduler():

    thread = threading.Thread(target=scheduler_loop)

    thread.daemon = True

    thread.start()

    print("Scheduler started")