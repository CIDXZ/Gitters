import soundfile as sf
import sounddevice as sd
import numpy as np
import tkinter as tk
from tkinter import filedialog

def select_sound_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(title="Select Sound File", filetypes=[("Sound Files", "*.wav;*.flac;*.ogg;*.mp3")])
    root.destroy()  # Close the Tkinter window
    return file_path

def record_audio(duration=10):
    try:
        fs = 44100  # Sample rate
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
        sd.wait()  # Wait until recording is finished
        return recording, fs
    except Exception as e:
        print("Error recording audio:", e)

def detect_sound_from_mic(similarity_threshold=0.5):
    sound_file = select_sound_file()
    if not sound_file:
        print("No sound file selected.")
        return

    try:
        print("Listening for sound from microphone...")
        sound_data, _ = sf.read(sound_file)
        while True:
            recorded_data, fs = record_audio()
            correlation = np.correlate(recorded_data.ravel(), sound_data.ravel(), mode='valid')
            max_correlation = np.max(correlation)
            if max_correlation > similarity_threshold * len(sound_data):
                print("Detected!")
                break
            else:
                print("No similar sound detected.")
    except Exception as e:
        print("Error detecting sound from microphone:", e)

if __name__ == "__main__":
    detect_sound_from_mic()
