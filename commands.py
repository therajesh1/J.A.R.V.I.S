from mac_control import execute_command
from speak import speak
import speech_recognition as sr  # Make sure file name is not speech_recognition.py

def confirm_shutdown():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Are you sure you want to shutdown? Say yes or no.")
        try:
            audio = recognizer.listen(source, timeout=5)
            response = recognizer.recognize_google(audio).lower()
            return "yes" in response
        except:
            return False

def execute_intent(intent):
    if intent == "shutdown":
        if confirm_shutdown():
            return execute_command(intent)
        else:
            return "Shutdown cancelled."
    else:
        return execute_command(intent)
