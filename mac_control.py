
import os

def execute_command(command):
    if command == "shutdown":
        os.system("osascript -e 'tell app \"System Events\" to shut down'")
    elif command == "open_chrome":
        os.system("open -a 'Google Chrome'")
    return "Command executed"
