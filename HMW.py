import threading 
import sys
import time
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import wave
import speech_recognition as sr
import os

stop_event = threading.Event()


def wait_for_enter():
    print("Press enter to end the recording")
    input("...")
    stop_event.set()

def record():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    frames = []

    while not stop_event.is_set():
        frames.append(stream.read(1024))

    stream.stop_stream()
    stream.close()
    width = p.get_sample_size(pyaudio.paInt16)
    p.terminate()

    frames = b"".join(frames)

    with wave.open("speech.wav", "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(width)
        wf.setframerate(16000)
        wf.writeframes(frames)
        print("File saved as 'speech.wav'")
    
    return frames, width

def transcribe(data, width):
    recognizer = sr.Recognizer()
    audio = sr.AudioData(data, 16000, width)
    try:
        text = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Could not understand the speech. Please try again.")
        return ""
    with open("speech.txt", "w") as wf:
        wf.write(text)
    print("You said:", text)
    print("Transcription saved as 'speech.txt")

def waveform(data):
    samples = np.frombuffer(data, dtype=np.int16)
    time_axis = np.linspace(0, len(samples) / 16000, len(samples))
    plt.figure(figsize=(10, 4))
    plt.plot(time_axis, samples, color="blue")
    plt.title("Your Voice Waveform")
    plt.xlabel("Time(seconds)")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.show()

def spinner():
    chars = "|/-\\"
    i =0
    while not stop_event.is_set():
        sys.stdout.write(f"\r Recording... {chars[i%4]}")
        sys.stdout.flush()
        i += 1
        time.sleep(0.1)
    print("\n")

def main():
        threading.Thread(target=spinner, daemon=True).start()
        threading.Thread(target=wait_for_enter, daemon=True).start()
        frames, width = record()
        transcribe(frames, width)
        waveform(frames)

if __name__ == "__main__":
    main()

