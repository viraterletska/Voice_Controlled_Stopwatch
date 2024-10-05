from transformers import pipeline

pipe = pipeline("automatic-speech-recognition", model="openai/whisper-small")


def recognize_voice_command():
    pass
