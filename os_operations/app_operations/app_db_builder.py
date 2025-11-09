import os
import json

SEARCH_DIRS = [
    r"C:\Program Files",
    r"C:\Program Files (x86)",
    r"C:\Windows\System32"
]

def build_app_db():
    app_db = {}
    for base_dir in SEARCH_DIRS:
        for root, _, files in os.walk(base_dir):
            for file in files:
                if file.lower().endswith(".exe"):
                    app_name = os.path.splitext(file)[0].lower()
                    if app_name not in app_db:  # Avoid duplicates
                        full_path = os.path.join(root, file)
                        app_db[app_name] = full_path

    with open("app_db.json", "w") as f:
        json.dump(app_db, f, indent=2)
    
    print(f"[JARVIS] App DB updated with {len(app_db)} apps.")

if __name__ == "__main__":
    build_app_db()
