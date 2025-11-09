from os_operations.file_operations.file_ops import execute_command
from os_operations.file_operations.jarvis_command_parser import extract_command
from os_operations.os_control.battery_monitor import manual_battery_check
from os_operations.music_player.music_player import play_music
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
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
