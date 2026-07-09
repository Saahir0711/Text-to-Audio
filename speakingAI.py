import speech_recognition as sr
import pyttsx3
from googletrans import Translator

def speak(text, language="en"):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    voices = engine.getProperty("voices")
    if language == "en":
        engine.setProperty("voice", voices[0].id)
    else:
        engine.setProperty("voice", voices[1].id)
    engine.say(text)
    engine.runAndWait()

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please speak now in English")
        audio = recognizer.listen(source)
    try:
        print("Recognizing speech...")
        text = recognizer.recognize_google(audio, language="en-US")
        print(f"You said: {text}")
        return text
    except sr.UnkownValueError:
        print("Could not understand the audio")
    except sr.RequestError as e:
        print(f"API Error: {e}")
        return""
    
def translate_text(text, target_language="es"):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    print(f"Translated text: {translation.text}")
    return translation.text

def display_language_options():
    print("Available translation languages: ")
    print("1. Hindi (hi)")
    print("2. Tamil (ta)")
    print("3 Telugu (te)")
    print("4. Bengali (bn)")
    print("5. Marathi (mr)")
    print("6. Gujarati (gu)")
    print("7. Malayalam (ml)")
    print("8. Punjabi (pa)")

    choice = input("Please select the target language number (1-8): ")
    language_dict = {
        "1": "hi",
        "2": "ta",
        "3": "te",
        "4": "bn",
        "5": "mr",
        "6": "gu",
        "7": "ml",
        "8":"pa"
    }
    return language_dict.get(choice, "es")

def main():
    target_language = display_language_options()
    original_text = speech_to_text()
    if original_text:
        translated_text = translate_text(original_text, target_language=target_language)
        speak(translated_text, language="en")
        print("Translation spoken out")

if __name__ == "__main__":
    main()
    