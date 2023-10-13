import soundcard as sc
import numpy as np

# Get the loopback device (replace with the appropriate device name on your system)
loopback = [mic for mic in sc.all_microphones(include_loopback=True) if 'headset microphone' in mic.name.lower()][0]

# Define chunk size
CHUNK_SIZE = 1024

# Define samplerate
SAMPLERATE = 44100

def normalize_rms(rms_value):
    # If the value is already between 1 and 100, return it as is
    if 1 <= rms_value <= 100:
        return rms_value
    
    # Otherwise, normalize based on a predefined range
    min_original = 1e-6
    max_original = 1e-4
    normalized_value = 1 + (rms_value - min_original) / (max_original - min_original) * 99
    
    # Clip the value to ensure it remains between 1 and 100
    return np.clip(normalized_value, 1, 100)


# Capture and process audio in chunks
with loopback.recorder(samplerate=SAMPLERATE) as mic:
    while True:
        # Capture a chunk of audio data
        data = mic.record(numframes=CHUNK_SIZE)
        
        # Compute RMS of the audio chunk
        rms = np.sqrt(np.mean(data**2))
        rms = normalize_rms(rms)
        print(rms)
        # Use the RMS value for your application (e.g., adjust brush size)
        brush_size = int(rms * 1000)  # This is just an example scaling factor
        # print(f"Brush Size: {brush_size}")