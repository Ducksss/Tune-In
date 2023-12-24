from elevenlabs import set_api_key, voices, generate as generate_voice
import os
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
print(ELEVENLABS_API_KEY)
set_api_key(ELEVENLABS_API_KEY)
print(voices())
