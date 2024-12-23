import time
import sounddevice as sd
import numpy as np
from transformers import pipeline

# Load the Whisper model
pipe = pipeline("automatic-speech-recognition", model="openai/whisper-small")

# Parameters for recording
DURATION = 3  # Duration to record each time (in seconds)
SAMPLE_RATE = 16000  # Sample rate for the microphone
THRESHOLD = 0.002  # Energy threshold for detecting speech
WINDOW_SIZE = 0.02  # Window size for energy calculation (in seconds)


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


def calculate_energy(signal, window_size, sample_rate):
    """Calculate the energy of the signal in moving windows."""
    window_length = int(window_size * sample_rate)
    energy = np.array([np.mean(signal[i:i + window_length] ** 2)
                       for i in range(0, len(signal) - window_length + 1, window_length)])
    return energy


def is_speech(signal, threshold=THRESHOLD):
    """Determine if the signal contains speech based on energy."""
    energy = calculate_energy(signal, WINDOW_SIZE, SAMPLE_RATE)
    return np.any(energy > threshold)


def preprocess_audio(audio_data):
    """Preprocess audio data by flattening and checking for speech activity."""
    signal = audio_data.flatten()
    if is_speech(signal):
        return signal
    return None


def continuous_listening(stopwatch, time_label):
    """Listen continuously for voice commands to control the stopwatch."""
    print("Listening for commands...")

    while True:
        try:
            # Record audio for the specified duration
            audio_data = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
            sd.wait()  # Wait until recording is finished

            # Preprocess the audio
            processed_audio = preprocess_audio(audio_data)
            if processed_audio is None:
                print("No speech detected.")
                continue

            # Process the audio using the Whisper model
            result = pipe(processed_audio)
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
