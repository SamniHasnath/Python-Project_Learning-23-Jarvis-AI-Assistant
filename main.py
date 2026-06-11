import sys
import threading
import datetime

import pyttsx3
import speech_recognition as sr

import commands
from config import (
    ASSISTANT_NAME,
    OPENAI_API_KEY,
    VOICE_RATE, VOICE_VOLUME, VOICE_INDEX,
)

# ── Initialize Text-to-Speech -- TTS engine ────────────────────────────────────────────────────────────────

engine = pyttsx3.init()
engine.setProperty("rate",   VOICE_RATE)
engine.setProperty("volume", VOICE_VOLUME)
voices = engine.getProperty("voices")
if voices:
    engine.setProperty("voice", voices[VOICE_INDEX].id)

_tts_lock = threading.Lock()


def speak(text: str):
    print(f"{ASSISTANT_NAME}: {text}")
    with _tts_lock:
        engine.say(text)
        engine.runAndWait()


# ── speech recognition ────────────────────────────────────────────────────────

recognizer = sr.Recognizer()
recognizer.pause_threshold  = 0.8
recognizer.energy_threshold = 300


def listen() -> str | None:
    with sr.Microphone() as source:
        print("Listening…")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            return None

    try:
        text = recognizer.recognize_google(audio)
        print(f"You: {text}")
        return text.lower()
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        speak("Speech recognition service is unavailable.")
        return None


# ── AI fallback ───────────────────────────────────────────────────────────────

_ai_client   = None
_chat_history = [
    {"role": "system", "content": (
        f"You are {ASSISTANT_NAME}, a helpful AI voice assistant. "
        "Keep responses short and conversational — two sentences max."
    )}
]

if OPENAI_API_KEY:
    try:
        from openai import OpenAI
        _ai_client = OpenAI(api_key=OPENAI_API_KEY)
    except ImportError:
        pass


def ask_ai(prompt: str) -> str:
    if not _ai_client:
        return "I'm not sure about that. You can set an OpenAI API key in the .env file for smarter replies."
    _chat_history.append({"role": "user", "content": prompt})
    try:
        response = _ai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=_chat_history,
            max_tokens=120,
        )
        reply = response.choices[0].message.content.strip()
        _chat_history.append({"role": "assistant", "content": reply})
        return reply
    except Exception as e:
        return f"AI error: {e}"


# ── greeting ──────────────────────────────────────────────────────────────────

def greet():
    hour = datetime.datetime.now().hour
    if hour < 12:
        period = "Good morning"
    elif hour < 18:
        period = "Good afternoon"
    else:
        period = "Good evening"
    speak(f"{period}! I am {ASSISTANT_NAME}. How can I help you?")


# ── main loop ─────────────────────────────────────────────────────────────────

def run():
    greet()

    while True:
        command = listen()
        if not command:
            continue

        result = commands.route(command)

        if result == "QUIT":
            speak("Goodbye! Have a great day.")
            sys.exit(0)

        if result is not None:
            speak(result)
        else:
            reply = ask_ai(command)
            speak(reply)


if __name__ == "__main__":
    run()
