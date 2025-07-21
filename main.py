import speech_recognition as sr
import cohere
from gtts import gTTS
import pygame
import time

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 تكلم الآن...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="ar-SA")
        print(f"📝 قلت: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ لم يتم التعرف على الصوت.")
        return None
    except sr.RequestError as e:
        print(f"⚠️ خطأ في الاتصال: {e}")
        return None

def get_response(text):
    co = cohere.Client("L8WUxKSfUKUjddVr2ZrRYHF0Jl4znTkKxogG2eW3")
    prompt = f"أجب على السؤال التالي باللغة العربية الفصحى وبأسلوب بسيط وواضح:\nس: {text}\nج:"
    response = co.chat(
        model="command-r-plus",
        message=prompt,
    )
    return response.text.strip()

def speak_text(text):
    tts = gTTS(text=text, lang="ar")
    filename = "response.mp3"
    tts.save(filename)

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.5)

if __name__ == "__main__":
    user_input = recognize_speech()
    if user_input:
        reply = get_response(user_input)
        print(f"🤖 الرد: {reply}")
        speak_text(reply)
