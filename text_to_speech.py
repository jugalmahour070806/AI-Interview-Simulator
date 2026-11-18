
import pyttsx3

def speak_text(text):
    """Convert text into speech."""
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 165)
        engine.setProperty("volume", 1.0)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print("Text-to-speech error:", e)
