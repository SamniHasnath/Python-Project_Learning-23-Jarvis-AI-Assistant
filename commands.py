import os
import re
import random
import socket
import threading
import datetime
import webbrowser
import xml.etree.ElementTree as ET

import requests

from config import MUSIC_DIR

# Optional packages — app keeps working if any are missing
try:
    import wikipedia
    _wikipedia_ok = True
except ImportError:
    _wikipedia_ok = False

try:
    import pywhatkit
    _pywhatkit_ok = True
except ImportError:
    _pywhatkit_ok = False

try:
    import pyautogui
    _pyautogui_ok = True
except ImportError:
    _pyautogui_ok = False

try:
    import pygame
    _pygame_ok = True
except ImportError:
    _pygame_ok = False

try:
    import psutil
    _psutil_ok = True
except ImportError:
    _psutil_ok = False


# ── helpers ───────────────────────────────────────────────────────────────────

def _files_in(folder, exts):
    if not os.path.isdir(folder):
        return []
    return [f for f in os.listdir(folder) if f.lower().endswith(tuple(exts))]


# ── time / date ───────────────────────────────────────────────────────────────

def get_time():
    now = datetime.datetime.now().strftime("%I:%M %p")
    return f"The current time is {now}"


def get_date():
    today = datetime.date.today().strftime("%A, %B %d %Y")
    return f"Today is {today}"


# ── search / web ──────────────────────────────────────────────────────────────

def search_wikipedia(query):
    if not _wikipedia_ok:
        return "Wikipedia package is not installed. Run: pip install wikipedia"
    try:
        result = wikipedia.summary(query, sentences=2)
        return result
    except wikipedia.exceptions.DisambiguationError as e:
        return f"That topic is ambiguous. Try one of these: {', '.join(e.options[:3])}"
    except wikipedia.exceptions.PageError:
        return "I couldn't find anything on Wikipedia for that."
    except Exception:
        return "Wikipedia search failed."


def search_google(query):
    webbrowser.open(f"https://www.google.com/search?q={query}")
    return f"Searching Google for {query}"


def play_youtube(query):
    if not _pywhatkit_ok:
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        return f"Opening YouTube search for {query}"
    pywhatkit.playonyt(query)
    return f"Playing {query} on YouTube"


def open_website(url):
    if not url.startswith("http"):
        url = "https://" + url
    webbrowser.open(url)
    return f"Opening {url}"


# ── music ─────────────────────────────────────────────────────────────────────

def play_music(song_name=None):
    if not _pygame_ok:
        return "pygame is not installed. Run: pip install pygame-ce"
    tracks = _files_in(MUSIC_DIR, [".mp3", ".wav", ".ogg"])
    if not tracks:
        return "No music files found in the assets/music folder."
    if song_name:
        match = next((t for t in tracks if song_name.lower() in t.lower()), None)
        if not match:
            return f"Couldn't find a song matching '{song_name}'."
        track = match
    else:
        track = tracks[0]
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join(MUSIC_DIR, track))
    pygame.mixer.music.play()
    return f"Playing {track}"


def stop_music():
    if not _pygame_ok:
        return "pygame is not installed."
    try:
        pygame.mixer.music.stop()
        return "Music stopped."
    except Exception:
        return "No music is currently playing."


# ── apps / system ─────────────────────────────────────────────────────────────

def open_app(app_name):
    apps = {
        "notepad":      "notepad.exe",
        "calculator":   "calc.exe",
        "paint":        "mspaint.exe",
        "browser":      "start chrome",
        "chrome":       "start chrome",
        "edge":         "start msedge",
        "explorer":     "explorer.exe",
        "task manager": "taskmgr.exe",
        "vs code":      "code",
        "vscode":       "code",
        "whatsapp":     "start whatsapp:",
        "spotify":      "start spotify:",
        "telegram":     "start telegram:",
        "settings":     "start ms-settings:",
        "camera":       "start microsoft.windows.camera:",
        "clock":        "start ms-clock:",
        "word":         "start winword",
        "excel":        "start excel",
        "powerpoint":   "start powerpnt",
        "vlc":          "start vlc",
        "file manager": "explorer.exe",
    }
    name = app_name.lower().strip()
    if name in apps:
        os.system(apps[name])
        return f"Opening {app_name}"
    try:
        os.system(f"start {app_name}")
        return f"Trying to open {app_name}"
    except Exception:
        return f"Sorry, I couldn't open {app_name}."


def take_screenshot():
    if not _pyautogui_ok:
        return "pyautogui is not installed. Run: pip install pyautogui"
    path = os.path.join(
        os.path.dirname(__file__), "screenshots",
        f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    )
    pyautogui.screenshot(path)
    return "Screenshot saved."


# ── weather ───────────────────────────────────────────────────────────────────

def get_weather(city):
    try:
        resp = requests.get(f"https://wttr.in/{city}?format=3", timeout=5)
        if resp.status_code == 200:
            return resp.text.strip()
        return "Couldn't fetch weather right now."
    except Exception:
        return "No internet connection or weather service unavailable."


# ── jokes ─────────────────────────────────────────────────────────────────────

def tell_joke():
    try:
        resp = requests.get("https://official-joke-api.appspot.com/random_joke", timeout=5)
        data = resp.json()
        return f"{data['setup']} ... {data['punchline']}"
    except Exception:
        return "Why don't scientists trust atoms? Because they make up everything!"


# ── greetings ─────────────────────────────────────────────────────────────────

def greet_back():
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "Good morning! How can I help you?"
    elif hour < 18:
        return "Good afternoon! How can I help you?"
    else:
        return "Good evening! How can I help you?"


# ── [NEW] battery ─────────────────────────────────────────────────────────────

def get_battery():
    if not _psutil_ok:
        return "psutil is not installed. Run: python -m pip install psutil"
    battery = psutil.sensors_battery()
    if battery is None:
        return "No battery detected. You may be on a desktop PC."
    percent = int(battery.percent)
    status  = "charging" if battery.power_plugged else "not charging"
    return f"Battery is at {percent} percent and {status}."


# ── [NEW] system info ─────────────────────────────────────────────────────────

def get_system_info():
    if not _psutil_ok:
        return "psutil is not installed. Run: python -m pip install psutil"
    cpu   = psutil.cpu_percent(interval=1)
    ram   = psutil.virtual_memory()
    disk  = psutil.disk_usage("/")
    used  = round(ram.used  / (1024 ** 3), 1)
    total = round(ram.total / (1024 ** 3), 1)
    d_used  = round(disk.used  / (1024 ** 3), 1)
    d_total = round(disk.total / (1024 ** 3), 1)
    return (f"CPU usage is {cpu} percent. "
            f"RAM usage is {used} GB out of {total} GB. "
            f"Disk usage is {d_used} GB out of {d_total} GB.")


# ── [NEW] IP address ──────────────────────────────────────────────────────────

def get_ip():
    try:
        public  = requests.get("https://api.ipify.org", timeout=5).text.strip()
        private = socket.gethostbyname(socket.gethostname())
        return f"Your public IP is {public} and private IP is {private}."
    except Exception:
        try:
            private = socket.gethostbyname(socket.gethostname())
            return f"Your private IP address is {private}."
        except Exception:
            return "Could not retrieve IP address."


# ── [NEW] coin flip / dice roll ───────────────────────────────────────────────

def flip_coin():
    result = random.choice(["Heads", "Tails"])
    return f"I flipped a coin and got {result}!"


def roll_dice(sides=6):
    result = random.randint(1, sides)
    return f"I rolled a {sides}-sided dice and got {result}!"


# ── [NEW] motivational quote ──────────────────────────────────────────────────

def get_quote():
    try:
        resp = requests.get("https://zenquotes.io/api/random", timeout=5)
        data = resp.json()
        return f"{data[0]['q']} — {data[0]['a']}"
    except Exception:
        quotes = [
            "Believe you can and you're halfway there. — Theodore Roosevelt",
            "It always seems impossible until it's done. — Nelson Mandela",
            "The secret of getting ahead is getting started. — Mark Twain",
        ]
        return random.choice(quotes)


# ── [NEW] news headlines ──────────────────────────────────────────────────────

def get_news():
    try:
        url  = "https://feeds.bbci.co.uk/news/rss.xml"
        resp = requests.get(url, timeout=5)
        root = ET.fromstring(resp.content)
        items = root.findall("./channel/item")[:5]
        headlines = [item.find("title").text for item in items if item.find("title") is not None]
        if not headlines:
            return "Couldn't fetch news right now."
        result = "Here are the top news headlines. "
        for i, h in enumerate(headlines, 1):
            result += f"{i}. {h}. "
        return result.strip()
    except Exception:
        return "Couldn't fetch news right now. Please check your internet connection."


# ── [NEW] timer ───────────────────────────────────────────────────────────────

def _parse_duration(cmd):
    match = re.search(r'(\d+)\s*(hour|hr|minute|min|second|sec)', cmd)
    if not match:
        return None, None
    value = int(match.group(1))
    unit  = match.group(2)
    if unit.startswith("h"):
        return value * 3600, f"{value} hour{'s' if value > 1 else ''}"
    if unit.startswith("m"):
        return value * 60,   f"{value} minute{'s' if value > 1 else ''}"
    return value, f"{value} second{'s' if value > 1 else ''}"


def set_timer(cmd):
    seconds, label = _parse_duration(cmd)
    if seconds is None:
        return "Please say the duration, for example: set timer for 5 minutes."

    def _ring():
        import pyttsx3
        _e = pyttsx3.init()
        _e.say(f"Timer done! {label} are up!")
        _e.runAndWait()

    t = threading.Timer(seconds, _ring)
    t.daemon = True
    t.start()
    return f"Timer set for {label}. I'll let you know when it's done."


# ── command router ────────────────────────────────────────────────────────────

def route(command: str):
    cmd = command.lower().strip()

    if any(w in cmd for w in ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "good night"]):
        return greet_back()

    if "how are you" in cmd:
        return "I'm doing great, thank you for asking! How can I help you?"

    if "your name" in cmd or "who are you" in cmd:
        return "I am Jarvis, your personal AI assistant. How can I help you?"

    if "what can you do" in cmd or "can you do" in cmd or "help" in cmd:
        return ("I can tell the time, date, battery, system info, IP address, "
                "news headlines, quotes, jokes, weather, set timers, flip a coin, "
                "roll dice, open apps, search Google or Wikipedia, and play YouTube. Just ask!")

    if "time" in cmd:
        return get_time()

    if "date" in cmd:
        return get_date()

    # ── easy features ─────────────────────────────────────────────────────────

    if "battery" in cmd:
        return get_battery()

    if "system info" in cmd or "cpu" in cmd or "ram" in cmd or "memory" in cmd:
        return get_system_info()

    if "ip address" in cmd or "my ip" in cmd:
        return get_ip()

    if "flip" in cmd and "coin" in cmd:
        return flip_coin()

    if "roll" in cmd and "dice" in cmd:
        match = re.search(r'(\d+)', cmd)
        sides = int(match.group(1)) if match else 6
        return roll_dice(sides)

    if "quote" in cmd or "motivate" in cmd or "inspire" in cmd:
        return get_quote()

    if "news" in cmd or "headlines" in cmd:
        return get_news()

    if "set timer" in cmd or "start timer" in cmd or "timer for" in cmd:
        return set_timer(cmd)

    # ── existing features ─────────────────────────────────────────────────────

    if "wikipedia" in cmd or "who is" in cmd or "what is" in cmd:
        query = (cmd.replace("wikipedia", "")
                    .replace("who is", "")
                    .replace("what is", "")
                    .strip())
        return search_wikipedia(query)

    if "play" in cmd and ("youtube" in cmd or "song" in cmd or "music" in cmd):
        query = (cmd.replace("play", "")
                    .replace("on youtube", "")
                    .replace("youtube", "")
                    .replace("song", "")
                    .replace("music", "")
                    .strip())
        return play_youtube(query) if query else play_music()

    if "stop music" in cmd or "pause music" in cmd:
        return stop_music()

    if "screenshot" in cmd:
        return take_screenshot()

    if "weather" in cmd:
        city = (cmd.replace("weather", "")
                   .replace(" in ", "")
                   .replace(" for ", "")
                   .strip())
        return get_weather(city if city else "London")

    if "joke" in cmd:
        return tell_joke()

    if "open" in cmd:
        target = cmd.replace("open", "").strip()
        if "." in target or "www" in target:
            return open_website(target)
        return open_app(target)

    if "search" in cmd or "google" in cmd:
        query = (cmd.replace("search", "")
                    .replace("google", "")
                    .replace("for", "")
                    .strip())
        return search_google(query)

    if any(w in cmd for w in ["bye", "exit", "quit", "goodbye", "stop"]):
        return "QUIT"

    return None  # fall through to AI
