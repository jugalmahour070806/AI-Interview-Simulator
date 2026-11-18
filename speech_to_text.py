
import speech_recognition as sr

def convert_speech_to_text(audio_file):
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)
        return text

    except sr.UnknownValueError:
        return "Could not understand the audio."

    except sr.RequestError:
        return "Speech recognition service unavailable. Check internet."

    except Exception as e:
        return f"Error: {e}"
