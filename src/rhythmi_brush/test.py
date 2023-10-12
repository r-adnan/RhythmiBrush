import soundcard as sc
import numpy as np

# Get the loopback device (replace with the appropriate device name on your system)
loopback = [mic for mic in sc.all_microphones(include_loopback=True) if 'Stereo Mix' in mic.name][0]

# Define chunk size
CHUNK_SIZE = 1024

# Define samplerate
SAMPLERATE = 44100

# Capture and process audio in chunks
with loopback.recorder(samplerate=SAMPLERATE) as mic:
    while True:
        # Capture a chunk of audio data
        data = mic.record(numframes=CHUNK_SIZE)
        
        # Compute RMS of the audio chunk
        rms = np.sqrt(np.mean(data**2))
        
        # Use the RMS value for your application (e.g., adjust brush size)
        brush_size = int(rms * 1000)  # This is just an example scaling factor
        print(f"Brush Size: {brush_size}")