from vosk import Model, KaldiRecognizer
import sounddevice as sd
import queue
import json
import difflib

def is_similar_to_jarvis(text):
    # Check each word in spoken text for similarity to 'jarvis'
    words = text.split()
    for word in words:
        match = difflib.get_close_matches(word, ["jarvis"], n=1, cutoff=0.75)
        if match:
            return True
    return False

def listen_for_wake_word():
    model = Model("vosk-model-en-us-0.22")  # Path to your Vosk model (use large model for best accuracy)
    recognizer = KaldiRecognizer(model, 16000)
    q = queue.Queue()

    def callback(indata, frames, time, status):
        if status:
            print("⚠️ Mic Status:", status)
        q.put(bytes(indata))

    print("🎧 Listening for wake word 'Jarvis'...")

    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").lower().strip()
                print("🔹 Heard:", text)

                if is_similar_to_jarvis(text):
                    print("✅ Wake word detected (fuzzy match).")
                    return True
