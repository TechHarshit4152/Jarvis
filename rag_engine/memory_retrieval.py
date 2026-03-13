import json
import faiss
import numpy as np
from dateparser.search import search_dates
from sentence_transformers import SentenceTransformer

MEMORY_JSON = r"C:\Users\Harshit\Desktop\JARVIS 5.0\rag_engine\memory\memory.json"
FAISS_INDEX = r"C:\Users\Harshit\Desktop\JARVIS 5.0\rag_engine\memory\memory.index"

model = SentenceTransformer("all-MiniLM-L6-v2")

with open(MEMORY_JSON, "r", encoding="utf-8") as f:
    memories = json.load(f)

index = faiss.read_index(FAISS_INDEX)


# -----------------------------
# DATE EXTRACTION
# -----------------------------
def extract_date(query):

    result = search_dates(query)

    if not result:
        return None

    dt = result[0][1]
    return dt.strftime("%Y-%m-%d")


# -----------------------------
# KEYWORD SEARCH
# -----------------------------
def search_keyword(query, memories, top_k=20):

    query_words = query.lower().split()
    scored = []

    for mem in memories:

        text = mem["text"].lower()
        score = sum(1 for word in query_words if word in text)

        if score > 0:
            scored.append((score, mem))

    scored.sort(reverse=True, key=lambda x: x[0])

    return [m[1] for m in scored[:top_k]]


# -----------------------------
# VECTOR SEARCH
# -----------------------------
def search_vector(query, top_k=20):

    query_embedding = model.encode([query])

    distances, indices = index.search(np.array(query_embedding), top_k)

    results = []

    for i, d in zip(indices[0], distances[0]):

        similarity = 1 / (1 + d)

        if similarity > 0.35 and i < len(memories):
            results.append(memories[i])

    return results


# -----------------------------
# HYBRID SEARCH
# -----------------------------
def hybrid_search(query, memories, top_k=20):

    vector_results = search_vector(query, top_k)
    keyword_results = search_keyword(query, memories, top_k)

    combined = []
    seen = set()

    for m in vector_results + keyword_results:

        if m["id"] not in seen:
            combined.append(m)
            seen.add(m["id"])

    return combined[:top_k]


# -----------------------------
# DATE SEARCH
# -----------------------------
def search_by_date(date, memories, top_k=20):

    results = []

    for mem in memories:
        mem_date = mem["timestamp"][:10]

        if mem_date == date:
            results.append(mem)

    return results[:top_k]


# -----------------------------
# MEMORY RETRIEVAL PIPELINE
# -----------------------------
def retrieve_memory(query):

    date = extract_date(query)
    print("Detected date:", date)

    if date:
        results = search_by_date(date, memories, top_k=5)

        if not results:
            print("No memories found for that date.")
            return []

        return results

    else:
        return hybrid_search(query, memories, top_k=5)


# -----------------------------
# CLI LOOP
# -----------------------------
try:

    while True:

        query = input("enter your query : ").strip()

        if len(query) < 3:
            print("Query too short.")
            continue

        results = retrieve_memory(query)
        results.sort(key=lambda x: x["timestamp"], reverse=True)

        if not results:
            continue

        for r in results:
            print("\n--- MEMORY ---")
            print(r["timestamp"])
            print(r["text"])

except KeyboardInterrupt:
    print("\nExiting.")