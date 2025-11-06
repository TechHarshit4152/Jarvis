import time
from TTS.api import TTS
import numpy as np
import sounddevice as sd

# Initialize model (lightweight + CPU-friendly)
tts = TTS("tts_models/en/ljspeech/tacotron2-DDC").to("cpu")

# Text to test
while True:
    text = input("enter your text : ")

# Start timer
    start_time = time.time()


    audio_data = tts.tts(text)

# End timer
    end_time = time.time()

# Playback
    audio_np = np.array(audio_data, dtype=np.float32)
    sd.play(audio_np, samplerate=22050)
    sd.wait()

# Show synthesis time
    print(f"\n⏱️ Time taken to synthesize: {end_time - start_time:.2f} seconds")
