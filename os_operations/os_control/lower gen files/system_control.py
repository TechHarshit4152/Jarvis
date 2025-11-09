from data.app_data_dlg import open_tasks, close_tasks
import os
import subprocess
import psutil

def open_application(app_name):
    
    if app_name in open_tasks:
        os.system(open_tasks[app_name])
        return f"Opening {app_name}..."
    else:
        return "Application not found."

def close_application(app_name):
    

    
    if app_name in close_tasks:
        process_name = close_tasks[app_name]
        for proc in psutil.process_iter(attrs=["pid", "name"]):
            if proc.info["name"].lower() == process_name.lower():
                psutil.Process(proc.info["pid"]).terminate()  # Forcefully terminate the process
                return f"Closed {app_name}."
        return f"{app_name} is not running."
    else:
        return "Application not found."


