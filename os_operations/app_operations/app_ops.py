# core/app_launcher/launcher.py

import subprocess
from fuzzywuzzy import process
from .db import load_apps_db

def fuzzy_find_app(app_query):
    apps = load_apps_db()
    choices = [app["name"] for app in apps.values()]
    best_match, score = process.extractOne(app_query, choices)
    if score >= 70:
        for app_id, app_data in apps.items():
            if app_data["name"] == best_match:
                return app_data
    return None

def launch_app(app_query):
    app = fuzzy_find_app(app_query)
    if app:
        try:
            print(f"[JARVIS] Launching {app['name']}...")
            subprocess.Popen(app["path"], shell=True)
            return True
        except Exception as e:
            print(f"[ERROR] Failed to launch {app['name']}: {e}")
            return False
    print(f"[JARVIS] App '{app_query}' not found.")
    return False
