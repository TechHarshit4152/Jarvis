from brain.brain import Main_Brain
from os_command_brain.command_brain import check_command



def cmd_strm(prompt: str):
    """
    Sends prompt to Main_Brain, streams and prints the response,
    and triggers command execution if needed.
    """
    full_message = ""

    for part in Main_Brain(prompt):
        if "chunk" in part:
            print(part["chunk"], end="", flush=True)
        elif "final" in part:
            full_message = part["final"]
    
    print()  # for clean line break
    check_command(full_message)