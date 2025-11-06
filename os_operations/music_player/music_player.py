import os
import re
from rapidfuzz import process, fuzz

def clean_song_name(song_name):
    """Removes special characters and extra words for better matching."""
    song_name = song_name.lower()
    song_name = re.sub(r"[^a-z0-9\s]", "", song_name)  # Remove special chars
    song_name = song_name.replace("slowed", "").replace("reverb", "").strip()
    return song_name

def find_song(song_query):
    """Search for the best-matching song in the given directory (including subfolders)."""
    all_songs = []
    music_folder = r"C:\Users\HP\Music"  # Change this to your music folder path
    
    # Walk through directory and collect all song files
    for root, _, files in os.walk(music_folder):
        for file in files:
            if file.endswith((".mp3", ".wav", ".flac", ".m4a")):
                all_songs.append(os.path.join(root, file))  # Store full path

    if not all_songs:
        return None, "No music files found."

    # Extract song names without extensions
    song_dict = {clean_song_name(os.path.splitext(os.path.basename(song))[0]): song for song in all_songs}

    # Clean query
    cleaned_query = clean_song_name(song_query)

    # 🔹 **First, try exact keyword matching** (for small queries like "Dil Nu")
    for song in song_dict.keys():
        if cleaned_query in song:
            return song_dict[song], f"Playing {song}..."

    # 🔹 **If no exact keyword match, use fuzzy matching**
    match = process.extractOne(cleaned_query, song_dict.keys(), scorer=fuzz.partial_ratio)

    # ✅ **Fix: Ensure match is a tuple before unpacking**
    if match and isinstance(match, tuple) and len(match) >= 2:
        best_match, score = match[:2]  # Unpack only the first two values
        if score > 60:  # Lowered threshold for better recognition
            return song_dict[best_match], f"Playing {best_match}..."
    
    return None, "No similar song found."

def play_music(song_name):
    """Plays the best-matching song."""
    song_path, message = find_song(song_name)
    
    if song_path:
        os.startfile(song_path)
    
    return message

# 🔥 **Testing**

