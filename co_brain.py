import os
import time
from voices.listen import listen
from voices.speak import speak
from brain.brain import Main_Brain
from os_command_brain.command_brain import process_command
from intent_recognition.intent_model import recognize_intent

is_awake = True

def jarvis_loop():
    """Main loop to keep JARVIS running."""
    global is_awake
    while True:
        # print("\nListening...")  # Show in console that it's waiting for input
        command = listen()  # Capture user voice input
        
        if command:
            print(f"\nYou: {command}")  # Show user command in terminal
            
            if "exit" in command.lower():
                print("JARVIS: Goodbye, Sir.")
                speak("Goodbye, Sir.")
                break  # Stop execution
            
            


            if not is_awake:
                if "wake up" in command:
                    is_awake = True
                    speak("I'm back online, sir.")
                else:
                    continue  # Ignore all input while asleep
            else:
                if "go to sleep" in command:
                    is_awake = False
                    speak("Going to sleep, sir.")
                else:
                    intent = recognize_intent(command)
                    if intent in ["info", "chat"]:
                        category, response = Main_Brain(command)   # Handles both info and chat
                        print(f"\nJARVIS:{category} | {message}")
                    elif intent == "command":
                        response = process_command(command)
                    
                    if response:
                        speak(response)




