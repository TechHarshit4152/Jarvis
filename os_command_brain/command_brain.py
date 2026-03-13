from os_operations.file_operations.file_ops import execute_command
from os_operations.file_operations.jarvis_command_parser import extract_command
from os_operations.os_control.battery_monitor import manual_battery_check
from os_operations.music_player.music_player import play_music
from task_scheduler.task_manager import create_task, delete_task, list_tasks, get_task, update_task
from datetime import datetime
from brain.brain import Main_Brain

 
def check_command(response):
    command = extract_command(response)

    if command==None:
        pass
    else:
        execute_command(command)


def execute_os_command(command):
    action = command.get("action")
    

    try:
        if action == "check_battery_level":
            message = manual_battery_check()
            return message
        

        elif action == "play_song" :
            songname = command.get("songname")
            message = play_music(songname)
            return message
        

        elif action == "create_task":
            task_name = command.get("taskname")
            date = command.get("date")
            time = command.get("time")

            try:

                if task_name:
                    res = create_task(task_name, date, time)
                    return res
                else:
                    return {
                            "status": "error",
                            "action": action,
                            "date": date,
                            "time": time,
                            "message": "create_task operation needs 'taskname' field"
                        }
            except Exception as e:
                return {
                        "status": "error",
                        "action": action,
                        "taskname": task_name,
                        "date": date,
                        "time": time,
                        "message": str(e)
                    }
            
        elif action == "delete_task":
            task_id = command.get("id")

            try:

                if task_id:
                    res = delete_task(task_id)
                    return res
                else:
                    return {
                            "status": "error",
                            "action": action,
                            "date": date,
                            "time": time,
                            "message": "delete_task operation needs 'id' field"
                        }
            except Exception as e:
                return {
                        "status": "error",
                        "action": action,
                        "taskname": task_name,
                        "date": date,
                        "time": time,
                        "message": str(e)
                    }
            
        elif action == "list_tasks":

            try:
                tasks = list_tasks()
                return tasks
            except Exception as e:
                return {
                        "status": "error",
                        "action": action,
                        "message": str(e)
                    }
            
        elif action == "get_task":
            task_id = command.get("id")

            try:
                if task_id:
                    res = get_task(task_id)
                    return res
                else:
                    return {
                            "status": "error",
                            "action": action,
                            "id": task_id,
                            "message": "get_task operation needs 'id' field"
                        }
            except Exception as e:
                return {
                        "status": "error",
                        "action": action,
                        "id": task_id,
                        "message": str(e)
                    }
        elif action == "update_task":
            task_id = command.get("id")

            try:
                if task_id:
                    res = update_task(task_id)
                    return res
                else:
                    return {
                            "status": "error",
                            "action": action,
                            "id": task_id,
                            "message": "update_task operation needs 'id' field"
                        }
            except Exception as e:
                return {
                        "status": "error",
                        "action": action,
                        "id": task_id,
                        "message": str(e)
                    }

    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
