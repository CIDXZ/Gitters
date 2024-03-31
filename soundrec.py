import pyaudio
import wave
import threading

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
WAVE_OUTPUT_FILENAME = "output.wav"
Input_Index = 1



audio = pyaudio.PyAudio()

# Open stream with the desired input device index
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=Input_Index)


print("Press Enter to start recording...")
input()

print("Recording... Press Enter again to stop.")

frames = []
recording = True

def stop_recording():
    global recording
    input()  # Wait for user to press Enter
    recording = False

# Start a thread to listen for user input to stop recording
thread = threading.Thread(target=stop_recording)
thread.start()

while recording:
    data = stream.read(CHUNK)
    frames.append(data)

print("Recording stopped.")

# Stop Recording
stream.stop_stream()
stream.close()
audio.terminate()

# Save the recorded audio to a WAV file
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

print("Audio saved as", WAVE_OUTPUT_FILENAME)



