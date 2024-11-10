import threading
import time

class InputThread(threading.Thread):
    def __init__(self, prompt, timeout):
        super().__init__()
        self.prompt = prompt
        self.timeout = timeout
        self.input = None
        self.daemon = True

    def run(self):
        self.input = input(self.prompt)

def non_blocking_input(prompt="", timeout=5):
    input_thread = InputThread(prompt, timeout)
    input_thread.start()
    input_thread.join(timeout)
    if input_thread.is_alive():
        return None
    return input_thread.input

# Example usage
timeout = 5  # seconds

user_input = non_blocking_input("Enter something: ", timeout)
if user_input is None:
    print("Input timed out")
else:
    print(f"You entered: {user_input}")