# wake_and_command.py
from vosk import Model, KaldiRecognizer
import sounddevice as sd
import queue
import json
import os

q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print("⚠️ Mic Error:", status)
    q.put(bytes(indata))

def load_model():
    model_path = "vosk-model-en-us-0.22"
    if not os.path.exists(model_path):
        raise Exception(f"Vosk model not found at '{model_path}'. Download and unzip from https://alphacephei.com/vosk/models")
    return Model(model_path)

def listen_for_phrase(model, expected=None, timeout=10):
    recognizer = KaldiRecognizer(model, 16000)
    recognizer.SetWords(True)

    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        print(f"🎤 Listening{' for wake word...' if expected else ' for command...'}")
        while True:
            try:
                data = q.get(timeout=timeout)
            except queue.Empty:
                print("⏳ Listening timed out.")
                return None

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").lower().strip()

                if not text:
                    continue

                print("🔹 Heard:", text)

                if expected:
                    if expected in text:
                        print("✅ Wake word detected.")
                        return True
                else:
                    return text

def listen_and_extract_command():
    model = load_model()

    # First wait for wake word
    while True:
        wake = listen_for_phrase(model, expected="jarvis")
        if wake:
            break

    # Then get the actual command
    command = listen_for_phrase(model)
    return command
