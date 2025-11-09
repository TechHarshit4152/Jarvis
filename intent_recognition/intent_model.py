from rapidfuzz import process

def recognize_intent(text):
    intents = {
        "info": ["how", "when", "what", "where", "why", "explain", "describe", "tell me about"],
        "command": ["play music", "play song", "play some music", "play some song", "open bluetooth", "bluetooth", "open wifi panel", "open wifi", "wifi", "open notepad", "open", "close", "shutdown", "restart", "lock", "check battery", "battery"]
    }

    text = text.lower()
    best_match = None
    best_score = 0


    for intent, keywords in intents.items():
        keywords = [kw.lower() for kw in keywords]  
        match = process.extractOne(text, keywords)
        if match and match[1] > best_score:
            best_match = intent
            best_score = match[1]


    if best_match == "command" and any(word in text for word in ["how", "using", "by coding"]):
        return "info"

    return best_match if best_score > 70 else "chat" 



