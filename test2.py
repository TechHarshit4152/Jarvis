from utils.print_strm import print_strm
from utils.exit_procedure import handle_exit_procedure
from conscious_core.memory_manager import append_to_chat_file
from utils.boot_message import dynamic_boot
import threading
import json
from datetime import datetime
from alert.alert import alert
import os



full_boot_message = dynamic_boot()

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
        response = print_strm(inp)
        append_to_chat_file(inp, response)
except KeyboardInterrupt:
    print("\n🛑 Jarvis Stopped")
    print("\n Signing off for now sir!")
        


            
        
