# speak.py
from pydub import AudioSegment
import simpleaudio as sa
import requests
import io
import threading

# Global lock to prevent overlapping audio
speak_lock = threading.Lock()

def generate_audio(message: str, voice: str = "Matthew"):
    url = f"https://api.streamelements.com/kappa/v2/speech?voice={voice}&text={message}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        result = requests.get(url=url, headers=headers)
        return result.content
    except Exception as e:
        print("Error fetching audio:", e)
        return None

def speak(message: str, voice: str = "Matthew"):
    with speak_lock:
        audio_data = generate_audio(message, voice)
        if not audio_data:
            return

        # Convert mp3 bytes into AudioSegment
        audio = AudioSegment.from_file(io.BytesIO(audio_data), format="mp3")

        # Play directly from memory
        play_obj = sa.play_buffer(
            audio.raw_data,
            num_channels=audio.channels,
            bytes_per_sample=audio.sample_width,
            sample_rate=audio.frame_rate
        )

        play_obj.wait_done()



