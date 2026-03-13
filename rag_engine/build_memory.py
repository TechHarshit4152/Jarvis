import json
import faiss
import numpy as np
import re
from sentence_transformers import SentenceTransformer

CHAT_FILE = r"C:\Users\Harshit\Desktop\JARVIS 5.0\conscious_core\memory_data\chat_history.txt"
MEMORY_JSON = r"C:\Users\Harshit\Desktop\JARVIS 5.0\rag_engine\memory\memory.json"
FAISS_INDEX = r"C:\Users\Harshit\Desktop\JARVIS 5.0\rag_engine\memory\memory.index"

model = SentenceTransformer("all-MiniLM-L6-v2")

log_pattern = r"\[(.*?)\]\s*(User|JARVIS):\s*(.*)"

def parse_chat_history():

    conversation = []

    with open(CHAT_FILE, "r", encoding="utf-8") as f:

        for line in f:

            line = line.strip()

            match = re.match(log_pattern, line)

            if not match:
                continue

            timestamp, speaker, message = match.groups()

            conversation.append({
                "timestamp": timestamp,
                "speaker": speaker,
                "text": message
            })

    return conversation



def build_memories(conversation):

    memories = []

    current_user = None
    timestamp = None

    for entry in conversation:

        if entry["speaker"] == "User":

            current_user = entry["text"]
            timestamp = entry["timestamp"]

        elif entry["speaker"] == "JARVIS" and current_user:

            memory_text = f"User: {current_user} JARVIS: {entry['text']}"

            memories.append({
                "timestamp": timestamp,
                "text": memory_text
            })

            current_user = None

    return memories



def build_vector_index(memories):

    texts = [m["text"] for m in memories]

    embeddings = model.encode(texts)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings))

    return index



def save_memory(memories):

    memory_data = []

    for i, mem in enumerate(memories):

        memory_data.append({
            "id": i,
            "timestamp": mem["timestamp"],
            "text": mem["text"]
        })

    with open(MEMORY_JSON, "w", encoding="utf-8") as f:
        json.dump(memory_data, f, indent=4, ensure_ascii=False)

    print(f"Saved {len(memory_data)} memories")



def build_database():

    print("Parsing chat history...")

    conversation = parse_chat_history()

    memories = build_memories(conversation)

    print(f"Extracted {len(memories)} conversation memories")

    if len(memories) == 0:
        print("No memories extracted.")
        return

    print("Creating embeddings...")

    index = build_vector_index(memories)

    print("Saving memory files...")

    save_memory(memories)

    faiss.write_index(index, FAISS_INDEX)

    print("Memory database built successfully.")



def add_memory(user_text, jarvis_text):

    new_memory = f"User: {user_text} JARVIS: {jarvis_text}"

    embedding = model.encode([new_memory])

    index = faiss.read_index(FAISS_INDEX)

    index.add(np.array(embedding))

    with open(MEMORY_JSON, "r", encoding="utf-8") as f:
        memories = json.load(f)

    new_id = len(memories)

    memories.append({
        "id": new_id,
        "timestamp": "runtime",
        "text": new_memory
    })

    with open(MEMORY_JSON, "w", encoding="utf-8") as f:
        json.dump(memories, f, indent=4, ensure_ascii=False)

    faiss.write_index(index, FAISS_INDEX)

    print("New memory added.")



if __name__ == "__main__":
    build_database()