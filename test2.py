from utils.print_strm import print_strm
from utils.exit_procedure import handle_exit_procedure
from conscious_core.memory_manager import append_to_chat_file
from utils.boot_message import dynamic_boot
from daily_summary_automation.date_manager import is_new_day
from daily_summary_automation.chat_logger import handle_new_day
from daily_summary_automation.chat_logger import log_chat
from task_scheduler.scheduler_thread import start_scheduler
import threading
import json
from datetime import datetime
from alert.alert import alert
import os

if is_new_day():
    handle_new_day()

full_boot_message = dynamic_boot()



start_scheduler()

threading.Thread(
    target=alert,
    args=(full_boot_message,),
    daemon=True
).start()



try:

    while True:
        inp = input("\nenter your prompt : ")

        if inp=="exit":
            handle_exit_procedure()
            break

        if is_new_day():
            handle_new_day()

        response = print_strm(inp)
        append_to_chat_file(inp, response)
        log_chat(inp, response)
except KeyboardInterrupt:
    print("\n🛑 Jarvis Stopped")
    print("\n Signing off for now sir!")
        
except Exception as e:
    print(f"\n❌ An error occurred: {e}")
    print("\n Attempting to save chat history and exit gracefully...")


            
        
