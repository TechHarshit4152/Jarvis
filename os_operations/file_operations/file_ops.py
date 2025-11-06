import os
from pathlib import Path
import json



# Friendly name mapping to system folders
SPECIAL_FOLDERS = {
    "desktop": str(Path.home() / "Desktop"),
    "documents": str(Path.home() / "Documents"),
    "downloads": str(Path.home() / "Downloads"),
    "music": str(Path.home() / "Music"),
    "pictures": str(Path.home() / "Pictures"),
    "videos": str(Path.home() / "Videos"),
}

def get_desktop_path():
    return str(Path.home() / "Desktop")

def normalize_path(path):
    return path.replace("\\", "/").strip()

def resolve_path(location):
    location = normalize_path(location.lower())

    # Check if the location starts with a special folder like "desktop/"
    for key, folder_path in SPECIAL_FOLDERS.items():
        if location == key:
            return folder_path
        elif location.startswith(key + "/"):
            sub_path = location[len(key) + 1:]  # skip "desktop/"
            return os.path.join(folder_path, sub_path)

    # Absolute path check
    if os.path.isabs(location) or ":" in location:
        return normalize_path(location)

    # Fallback: treat as relative to desktop
    return os.path.join(get_desktop_path(), location)





def complete_command(command):
    action = command.get("action")
    filename = command.get("filename", "newfile.txt")
    location = command.get("location", "desktop")

    full_path = os.path.join(resolve_path(location), filename)

    try:
        if action == "create":
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write("")
            res = f"✅ File created at: {full_path}"
            return res
        
        elif action == "delete":
            if os.path.exists(full_path):
                os.remove(full_path)
                res = f"🗑️ File deleted: {full_path}"
                return res
            else:
                res = f"⚠️ File not found: {full_path}"
                return res

        elif action == "move":
            target = command.get("target")
            if not target:
                res = "❌ Move operation needs 'target' field."
                return res
            destination = os.path.join(resolve_path(target), filename)
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            os.rename(full_path, destination)
            res = f"📁 Moved to: {destination}"
            return res

        elif action == "rename":
            newname = command.get("newname")
            if not newname:
                res = "❌ Rename operation needs 'newname' field."
                return res
            new_path = os.path.join(resolve_path(location), newname)
            os.rename(full_path, new_path)
            res = f"✏️ Renamed to: {new_path}"
            return res

        elif action == "copy":
            import shutil
            target = command.get("target")
            if not target:
                res = "❌ Copy operation needs 'target' field." 
                return res
            destination = os.path.join(resolve_path(target), filename)
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            shutil.copy2(full_path, destination)
            res = f"📄 Copied to: {destination}"
            return res

        elif action == "search":
            found = False
            for root, dirs, files in os.walk(resolve_path(location)):
                if filename in files:
                    res = f"🔍 Found: {os.path.join(root, filename)}"
                    return res
                    found = True
                    break
            if not found:
                res = "❌ File not found."
                return res

        elif action == "write":
            content = command.get("content", "")
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            # Normalize and define special append folder
            special_append_path = os.path.normpath(r"C:\Users\HP\Desktop\JARVIS 5.0\conscious_core\reflective_summaries\weekly\temp_week_summary")
            current_folder = os.path.normpath(os.path.dirname(full_path))

            # Decide mode based on folder
            mode = 'a' if current_folder == special_append_path else 'w'

            with open(full_path, mode, encoding='utf-8') as f:
                if mode == 'a':
                    f.write("\n" + content.strip())
                else:
                    f.write(content.strip())

            res = f"📝 {'Appended' if mode == 'a' else 'Written to'}: {full_path}"
            return res

        elif action == "read":
            if os.path.exists(full_path):
                with open(full_path, 'r', encoding='utf-8') as f:
                    data = f.read()
                res = f"\n📖 Content of {filename}:\n{data} \n tell sir what was in the file and if you want to tell something else about the file, than go on! Also dont print any category here"
                return res
            else:
                res = "❌ File not found to read."
                return res

        else:
            from os_command_brain.command_brain import execute_os_command
            response = execute_os_command(command)
            return response

    except Exception as e:
        res = f"❌ Error: {str(e)}"
        return res



def execute_command(message):
    from utils.cmd_strm import cmd_strm
    if isinstance(message, dict):
       cmd_strm(complete_command(message))
    elif isinstance(message, list):
        for cmd in message:
           cmd_strm(complete_command(cmd))
    elif isinstance(message, str):
        stripped = message.strip()
        if stripped.startswith("["):
            command_list = json.loads(message)
            for cmd in command_list:
               cmd_strm(complete_command(cmd))
        elif stripped.startswith("{"):
            command = json.loads(message)
            cmd_strm(complete_command(message))
        else:
            print("❌ Invalid command format")
    else:
        print("❌ Unsupported command type:", type(message))




