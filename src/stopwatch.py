import time
import sounddevice as sd
from transformers import pipeline

# Load the Whisper model
pipe = pipeline("automatic-speech-recognition", model="openai/whisper-small")

# Parameters for recording
DURATION = 5  # Duration to record each time (in seconds)
SAMPLE_RATE = 16000  # Sample rate for the microphone


class Stopwatch:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0
        self.running = False

    def start(self):
        """Start the stopwatch"""
        if not self.running:
            self.start_time = time.time() - self.elapsed_time
            self.running = True

    def stop(self):
        """Stop the stopwatch"""
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            self.running = False

    def reset(self):
        """Reset the stopwatch"""
        self.elapsed_time = 0
        if self.running:
            self.start_time = time.time()

    def get_time(self):
        """Get the formatted current time"""
        if self.running:
            return time.strftime("%H:%M:%S", time.gmtime(time.time() - self.start_time))
        else:
            return time.strftime("%H:%M:%S", time.gmtime(self.elapsed_time))


def continuous_listening(stopwatch, time_label):
    """Listen continuously for voice commands to control the stopwatch."""
    print("Listening for commands...")

    while True:
        try:
            # Record audio for a specified duration
            audio_data = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
            sd.wait()  # Wait until recording is finished

            # Convert the audio data to a format compatible with the Whisper model
            audio_data = audio_data.flatten()  # Flatten the array to ensure it is 1D

            # Process the audio using the Whisper model
            result = pipe(audio_data)
            recognized_text = result['text']
            print(f"Recognized: {recognized_text}")

            # Process recognized commands
            if "start" in recognized_text.lower():
                print("Start command recognized")
                stopwatch.start()
            elif "stop" in recognized_text.lower():
                print("Stop command recognized")
                stopwatch.stop()
            elif "reset" in recognized_text.lower():
                print("Reset command recognized")
                stopwatch.reset()

            # Update the time display on the UI
            time_label.config(text=stopwatch.get_time())

            # Short delay before listening again
            time.sleep(1)

        except Exception as e:
            print(f"Error in listening: {e}")
