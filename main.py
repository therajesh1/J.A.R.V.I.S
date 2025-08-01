# main.py
from wake_and_command import listen_and_extract_command
from speak import speak
from brain import predict_intent
from commands import execute_intent
from fallback_llm import query_llm
from memory import save_to_memory, retrieve_memory

def main():
    while True:
        command = listen_and_extract_command()
        if not command:
            speak("Sorry, I didn't catch that.")
            continue

        command = command.strip().lower()

        if command in ["stop", "exit", "quit", "shutdown"]:
            speak("Okay, shutting down. See you later!")
            break

        print("🎙️ Command Received:", command)
        speak("You said: " + command)

        intent = predict_intent(command)
        print(f"🔍 Predicted Intent: {intent}")

        if intent:
            print("⚡ Executing Intent...")
            response = execute_intent(intent)
        else:
            print("🧠 Using Memory or LLM fallback...")
            response = retrieve_memory(command)

            if not response:
                response = query_llm(command)
                save_to_memory(command, response)

        if response:
            print("📢 Final Response:", response)
            speak(response)
        else:
            print("❌ No response generated.")
            speak("Sorry, I don't have an answer for that.")

if __name__ == "__main__":
    main()
