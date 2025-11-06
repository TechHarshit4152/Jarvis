from datetime import datetime


now = datetime.now()


def check_time():
    current_time = now.strftime("%H:%M:%S")
    return  current_time
