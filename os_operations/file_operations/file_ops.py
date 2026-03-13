import os
from pathlib import Path
import json
import shutil



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
    if not path:
        return ""
    return os.path.normpath(path).replace("\\", "/").strip()

def resolve_path(location):
    location = normalize_path(location.lower())

    for key, folder_path in SPECIAL_FOLDERS.items():
        if location == key:
            return folder_path
        elif location.startswith(key + "/"):
            sub_path = location[len(key) + 1:] 
            return os.path.join(folder_path, sub_path)

    if os.path.isabs(location):
        return normalize_path(location)

    return os.path.join(get_desktop_path(), location)





def complete_command(command):
    action = command.get("action")
    filename = command.get("filename", "newfile.txt")
    location = command.get("location", "desktop")

    full_path = os.path.join(resolve_path(location), filename)

    try:
        if action == "create_file":
            try:
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write("")
                return {"status":"success", "action":action, "filename":filename, "location":full_path, "message":"File created successfully"}
            except Exception as e:
                return {
                    "status": "error",
                    "action": action,
                    "filename": filename,
                    "location": full_path,
                    "message": str(e)
                    }
        
        elif action == "delete":
            try:

                if os.path.exists(full_path):



                    if os.path.isfile(full_path):
                        os.remove(full_path)
                        return {
                            "status": "success",
                            "action": action,
                            "filename": filename,
                            "location": full_path,
                            "message": "File deleted successfully"
                            }
                    elif os.path.isdir(full_path):
                        shutil.rmtree(full_path)
                        return {
                            "status": "success",
                            "action": action,
                            "foldername": filename,
                            "location": full_path,
                            "message": "Folder deleted successfully"
                            }
                else:
                    return {
                        "status": "error",
                        "action": action,
                        "filename": filename,
                        "location": full_path,
                        "message": "File doesn't exists"
                        }
            except Exception as e:
                return {
                        "status": "error",
                        "action": action,
                        "filename": filename,
                        "location": full_path,
                        "message": str(e)
                        }
        

        elif action == "move":
            try :
                target = command.get("target")
                if not target:
                    return {
                        "status": "error",
                        "action": action,
                        "filename": filename,
                        "message": "move operation needs 'target' field"
                        }
                destination = os.path.join(resolve_path(target), filename)
                os.makedirs(os.path.dirname(destination), exist_ok=True)
                shutil.move(full_path, destination)
                return {
                    "status": "success",
                    "action": action,
                    "filename": filename,
                    "from": full_path,
                    "to": destination,
                    "message": "File moved successfully"
                    }
            except Exception as e:
                return {
                        "status": "error",
                        "action": action,
                        "filename": filename,
                        "location": full_path,
                        "message": str(e)
                        }


        elif action == "rename":
            newname = command.get("newname")
            if not newname:
                return {
                        "status": "error",
                        "action": action,
                        "filename": filename,
                        "message": "rename operation needs 'newname' field"
                        }
            
            try:

                new_path = os.path.join(resolve_path(location), newname)
                os.rename(full_path, new_path)
                return {
                        "status": "success",
                        "action": action,
                        "old_name": filename,
                        "new_name": newname,
                        "location": new_path,
                        "message": "File renamed successfully"
                        }
            except Exception as e:
                return {
                        "status": "error",
                        "action": action,
                        "filename": filename,
                        "location": full_path,
                        "message": str(e)
                        }

        elif action == "copy":
            
            target = command.get("target")
            if not target:
                return {
                        "status": "error",
                        "action": action,
                        "filename": filename,
                        "location": full_path,
                        "message": "copy operation needs 'target' field"
                        }
            try :

                destination = os.path.join(resolve_path(target), filename)
                os.makedirs(os.path.dirname(destination), exist_ok=True)
                shutil.copy2(full_path, destination)
                return{
                        "status": "success",
                        "action": action,
                        "filename": filename,
                        "from": full_path,
                        "to": destination,
                        "message": "File copied successfully"
                        }
            except Exception as e:
                return {
                        "status": "error",
                        "action": action,
                        "filename": filename,
                        "location": full_path,
                        "message": str(e)
                        }

        elif action == "search":
            found = False

            try:

                for root, dirs, files in os.walk(resolve_path(location)):
                    if filename in files:
                        found = True

                        return {
                            "status": "success",
                            "action": action,
                            "filename": filename,
                            "searched_directory": root,
                            "data": {
                                "found": found,
                                "path": os.path.join(root, filename)
                            }
                        }
                        
                    

                if not found:
                    return {
                        "status": "success",
                        "action": action,
                        "filename": filename,
                        "searched_directory": resolve_path(location),
                        "data": {
                            "found": found
                        }
                    }
            except Exception as e :
                return {
                        "status": "error",
                        "action": action,
                        "filename": filename,
                        "searched_directory": full_path,
                        "message": str(e)
                        }

        elif action == "write":
            content = command.get("content", "")
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            
            special_append_path = os.path.abspath(r"C:\Users\HP\Desktop\JARVIS 5.0\conscious_core\reflective_summaries\weekly\temp_week_summary")
            current_folder = os.path.abspath(os.path.dirname(full_path))

            try:

                mode = 'a' if command.get("mode", "").lower() == "append" or current_folder == special_append_path else 'w'

                with open(full_path, mode, encoding='utf-8') as f:
                    if mode == 'a':
                        f.write(content.strip() + "\n")
                    else:
                        f.write(content.strip())
 
                return {
                    "status": "success",
                    "action": action,
                    "filename": filename,
                    "location": full_path,
                    "message": f"Content {'Appended' if mode == 'a' else 'Written'} successfully"
                    }
            except Exception as e:
                return {
                        "status": "error",
                        "action": action,
                        "filename": filename,
                        "location": full_path,
                        "message": str(e)
                        }

        elif action == "read":
            try:

                if os.path.isfile(full_path):
                    with open(full_path, 'r', encoding='utf-8') as f:
                        data = f.read()
                    return {
                            "status": "success",
                            "action": action,
                            "filename": filename,
                            "location": full_path,
                            "data": {
                                "content": data
                            }
                        }
                else:
                    return {
                        "status": "error",
                        "action": action,
                        "filename": filename,
                        "location": full_path,
                        "message": "File not found to read"
                    }
            except Exception as e:
                return {
                        "status": "error",
                        "action": action,
                        "filename": filename,
                        "location": full_path,
                        "message": str(e)
                        }
            
        elif action == "list_dir":
            directory = command.get("directory")
            
            if not directory:
                return {
                    "status": "error",
                    "action": action,
                    "message": "Directory field is required"
                }
            try:
                full_dir_path = resolve_path(directory)
                if os.path.exists(full_dir_path):

                    
                        items = os.listdir(full_dir_path)
                        result = []
                        truncated = False
                        no_of_files = 0
                        
                        
                        for item in items:
                            full_item_path = os.path.join(full_dir_path, item)

                            if os.path.isdir(full_item_path):
                                result.append({"name": item, "type": "folder"})
                            
                            elif os.path.isfile(full_item_path):
                                result.append({"name":item, "type":"file"})
                            
                            else:
                                result.append({"name":item, "type":"neither a file, nor a folder"})
                            
                            no_of_files+=1

                            if no_of_files>=50:
                                truncated = True
                                break

                        
                        return {
                                "status": "success",
                                "action": action,
                                "directory": directory,
                                "location": full_dir_path,
                                "truncated": truncated,
                                "items_count": no_of_files,
                                "data": {
                                    "items": result
                                }
                            }
                else :
                    
                    return {
                        "status": "error",
                        "action": action,
                        "message": "Directory not found"
                        }
            except Exception as e:
                return {
                        "status": "error",
                        "action": action,
                        "directory": directory,
                        "location": full_dir_path,
                        "message": str(e)
                        }
                


        elif action == "create_folder":
            try:
                folder_name = command.get("foldername")
                full_folder_path = os.path.join(resolve_path(location), folder_name)

                if not os.path.exists(full_folder_path):
                    os.makedirs(full_folder_path)
                    return{
                        "status": "success",
                        "action": action,
                        "foldername": folder_name,
                        "location": full_folder_path,
                        "message": "Folder created successfully"
                    }
                else:
                    return {
                        "status": "success",
                        "action": action,
                        "foldername": folder_name,
                        "location": full_folder_path,
                        "message": "Folder already exists"
                    }
                    
            except Exception as e:
                return {
                        "status": "error",
                        "action": action,
                        "foldername": folder_name,
                        "location": full_folder_path,
                        "message": str(e)
                    }

        else:
            from os_command_brain.command_brain import execute_os_command
            response = execute_os_command(command)
            return response

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }



def execute_command(message):
    from utils.cmd_strm import cmd_strm
    if isinstance(message, dict):
       cmd_strm(complete_command(message))
    elif isinstance(message, list):
        results = []
        for cmd in message:
           res = complete_command(cmd)
           results.append(res)
        cmd_strm(results)
    elif isinstance(message, str):
        stripped = message.strip()
        if stripped.startswith("["):
            command_list = json.loads(message)
            results = []
            for cmd in command_list:
               res = complete_command(cmd)
               results.append(res)
            cmd_strm(results)
        elif stripped.startswith("{"):
            command = json.loads(message)
            cmd_strm(complete_command(command))
        else:
            print("❌ Invalid command format")
    else:
        print("❌ Unsupported command type:", type(message))




