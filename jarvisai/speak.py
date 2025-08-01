# speak.py
import asyncio
import edge_tts
import os
import uuid
from playsound import playsound

VOICE = "en-IN-PrabhatNeural"  # ✅ Male Indian voice
RATE = "-10%"  # ✅ Slower for clarity

async def _speak(text):
    if not text.strip():
        return
    print("🗣️ Speaking:", text)

    filename = f"temp_{uuid.uuid4()}.mp3"
    communicate = edge_tts.Communicate(text, voice=VOICE, rate=RATE)
    await communicate.save(filename)

    playsound(filename)
    os.remove(filename)

def speak(text):
    asyncio.run(_speak(text))
