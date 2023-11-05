from flask import Flask, request, render_template, send_file
import requests
import json
import os
from dotenv import load_dotenv
import openai
import pyttsx3
import random
import json
from elevenlabs import set_api_key, voices, generate as generate_voice

load_dotenv()

openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
engine = pyttsx3.init()
DEPLOYMENT_NAME = os.getenv("OPENAI_API_ENGINE")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
set_api_key(ELEVENLABS_API_KEY)

@app.route("/", methods=['GET'])
def home():
    return "Hello World"


@app.route("/generate", methods=["GET", "POST"])
def generate_lyrics():
    if request.method == "POST":
        requestBody = request.json
        topic = requestBody["topic"]

        # OpenAI Prompt Engineering
        print("Start Processing OpenAI")
        response = openai.ChatCompletion.create(
            engine=DEPLOYMENT_NAME,
            messages=[
                {"role": "user", "content": f"""Generate a short song that is maximum 30 seconds long with the description of how the song should sound like and lyrics about """ + topic + """. Make the song catchy and memorable. Give the response only in JSON object formatted like the following
{
    "description": string,
    "lyrics": string
}"""}
            ],
            temperature=0.8,
            max_tokens=500,
            top_p=0.9,
            frequency_penalty=0,
            presence_penalty=0,
        )
        json_response = json.loads(response['choices'][0]['message']['content'])
        print("End Processing OpenAI")

        # Processing Lyrics
        print("Start Processing Lyrics")
        lyrics = json_response["lyrics"]
        engine.setProperty('rate', 170)
        voices = engine.getProperty("voices")
        # voiceNum = random.randint(0, len(voices)-1)
        voiceNum = 1
        engine.setProperty("voice", voices[voiceNum].id)
        engine.save_to_file(lyrics, 'temp.mp3')
        engine.runAndWait()
        sing = generate_voice(
            text=lyrics, voice="Grace", model="eleven_monolingual_v1"
        )
        with open("sing2.mp3", "wb") as f:
            f.write(sing)
            f.close()
        print("End Processing Lyrics")

        # Processing Music
        print("Start Processing Music")
        description = json_response["description"]
        API_URL = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
        headers = {"Authorization": HUGGINGFACE_API_KEY}
        payload = {
            "inputs": description,
        }
        audio_response = requests.post(API_URL, headers=headers, json=payload)
        audio_bytes = audio_response.content
        with open("bg.mp3", 'wb') as f:
            f.write(audio_bytes)
            f.close()
        print("End Processing Music")

        # Processing Autotuning
        
        
        return json_response
    # audioURL = f"https://translate.google.com/translate_tts?ie=UTF-8&q={prompt.replace(' ','%20')}&tl=en-US&client=tw-ob"
    # audio = requests.get(audioURL)
    # print(audioURL)
    # print(audio)
    return "audio"
#     print(prompt)
    return "hi"


if __name__ == "__main__":
    app.run(debug=True)
