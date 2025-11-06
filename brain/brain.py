from rich import print
from dotenv import load_dotenv
from conscious_core.jarvis_system_prompt_builder import build_system_prompt
import os
import time
from groq import Groq



load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)
SYSTEM_PROMPT =build_system_prompt()

print(SYSTEM_PROMPT)




chat_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]


def Main_Brain(text):

    chat_history.append({"role": "user", "content": text})

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=chat_history,
        stream=True,
    )

    full_reply = ""

    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            full_reply += content
            yield {"chunk": content}  



    # After streaming is finished
    full_reply = full_reply.strip()
    chat_history.append({"role": "assistant", "content": full_reply})
    

    yield {"final": full_reply}



