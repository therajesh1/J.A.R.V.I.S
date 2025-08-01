from vosk import Model, KaldiRecognizer
import os
import pyaudio
import json

model_path = os.path.join(os.path.dirname(__file__), "model")
model = Model(model_path)

rec = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1,
                  rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

def listen_command():
    print("Listening for command...")
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            return result.get("text", "")
