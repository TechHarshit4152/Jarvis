import json
import re

def extract_command(message: str):
    try:
        # Extract either JSON object or array, even if multi-line
        match = re.search(r'(\{[\s\S]*?\}|\[[\s\S]*?\])', message)
        if match:
            json_str = match.group(0)
            commands = json.loads(json_str)
            return commands
    except Exception as e:
        return ""
    return None


