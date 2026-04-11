from pathlib import Path

# Base JARVIS directory
BASE_DIR = Path.home() / "Desktop" / "Projects" /"JARVIS 5.0"


CHECK_INTERVAL = 5

ACTIVE_TASK_FILE = BASE_DIR / "task_scheduler" / "storage" / "tasks_active.json"
TASK_HISTORY_FILE = BASE_DIR / "task_scheduler" / "storage" / "tasks_history.json"