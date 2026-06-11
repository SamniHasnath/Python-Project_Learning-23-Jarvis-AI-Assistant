import os
from dotenv import load_dotenv

load_dotenv()

ASSISTANT_NAME = "Jarvis"
WAKE_WORD      = "jarvis"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

MUSIC_DIR = os.path.join(os.path.dirname(__file__), "assets", "music")

VOICE_RATE   = 170   # words per minute
VOICE_VOLUME = 1.0   # 0.0 – 1.0
VOICE_INDEX  = 0     # 0 = first system voice
