import tkinter as tk
from src.stopwatch import Stopwatch, continuous_listening
import threading


class StopwatchApp:
    def __init__(self, window):
        self.stopwatch = Stopwatch()

        window.title("Voice Controlled Stopwatch")
        window.geometry("300x200")

        # Create a label for the time display
        self.time_label = tk.Label(window, text="00:00:00", font=("Arial", 30))
        self.time_label.pack(pady=20)

        # Create a button to start voice command listening
        self.listen_button = tk.Button(window, text="Listen for Command", command=self.listen_command)
        self.listen_button.pack(pady=10)

        # Update the time display
        self.update_time_display()

    def listen_command(self):
        # This function will start listening when the button is pressed
        thread = threading.Thread(target=self.listen_for_voice_command)
        thread.daemon = True  # Ensure thread exits when the app closes
        thread.start()

    def listen_for_voice_command(self):
        # This function is responsible for listening to the voice command
        continuous_listening(self.stopwatch, self.time_label)

    def update_time_display(self):
        # This method updates the stopwatch time every second
        def update():
            self.time_label.config(text=self.stopwatch.get_time())
            self.time_label.after(1000, update)

        update()


if __name__ == "__main__":
    root = tk.Tk()  # Create the main Tkinter window
    app = StopwatchApp(root)  # Create the StopwatchApp instance
    root.mainloop()  # Start the Tkinter main loop
