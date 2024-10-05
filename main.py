import tkinter as tk
# from stopwatch import recognize_voice_command


class StopwatchApp:
    def __init__(self, window):
        window.title("Voice Controlled Stopwatch")
        window.geometry("300x200")  # Window size

        # Create a label for the time display
        self.time_label = tk.Label(window, text="00:00:00", font=("Arial", 30))
        self.time_label.pack(pady=20)

        # Add a single button for voice recognition
        self.voice_button = tk.Button(window, text="Voice Command")
        self.voice_button.pack(pady=10)

    # def listen_for_command(self):
    #    """Call the voice recognition function from stopwatch.py."""
    #    recognize_voice_command()


if __name__ == "__main__":
    root = tk.Tk()
    app = StopwatchApp(root)
    root.mainloop()
