import speech_recognition as sr
import random
import webbrowser
from gtts import gTTS
import os
import pygame
import pygame.mixer
from difflib import SequenceMatcher
from typing import Dict, Optional
import json

"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import os

import google.generativeai as genai

# 1. Set up the environment variable (using the correct API key)
# Replace 'YOUR_API_KEY' with the actual key from your Google AI Platform project. 
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "AIzaSyATtV86B2Hzv9C_jFfF8tFzrdvmtc-q7kY"

# 2. Configure the Google AI Python SDK
genai.configure(api_key=os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

chat_session = model.start_chat(
  history=[
  ]
)

# Initialize recognizer
r = sr.Recognizer()

def load_chat_prompts(file_path: str) -> Dict[str, str]:
    """Load chat prompts from a JSON file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Load chat prompts
chat_prompts = load_chat_prompts('prompts.json')

def find_best_match(input_text: str, prompts: Dict[str, str]) -> Optional[str]:
    """Find the closest match in the chat prompts."""
    max_similarity = 0
    best_match = None
    for prompt in prompts:
        similarity = SequenceMatcher(None, input_text, prompt).ratio()
        if similarity > max_similarity:
            max_similarity = similarity
            best_match = prompt
    return best_match if max_similarity > 0.5 else None

def record_audio() -> str:
    """Record user's voice and return the recognized text."""
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            voice_data = r.recognize_google(audio)
            return voice_data
        except sr.UnknownValueError:
            return None  # Return None if the speech was unintelligible
        except sr.RequestError:
            return "Sorry, the service is down"
        except Exception as e:
            print(f"Error: {e}")
            return None

def shivi_speaks(audio_string: str):
    tts = gTTS(text=audio_string, slow=False, lang='hi')
    r = random.randint(1, 100000000)
    audio_file = f'audio-{r}.mp3'
    tts.save(audio_file)
    
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()
    
    print(audio_string)
    
    try:
        os.remove(audio_file)
    except Exception as e:
        print(f"Error removing {audio_file}: {e}")

def respond(voice_data: str):
    """Respond to user's voice command."""
    # best_match = find_best_match(voice_data, chat_prompts)
    best_match = chat_session.send_message(voice_data)
    if best_match:
        if best_match == "play songs" or best_match == "gaane chalao" or best_match == "gane suna do" or best_match == "gana suna do" or best_match == "songs":
            url = 'https://www.youtube.com/shorts/ELqyInFBM7g'
            webbrowser.get().open(url)
        shivi_speaks(chat_prompts[best_match])
        if best_match == "stop" or "bye" or "bye shiwani" or "bye shivani":
            exit()
    else:
        shivi_speaks('Sorry, par samajh nahi aaya, phir se bolo')

# Main loop
# shivi_speaks('Hello sir! Kaise ho?')
error_count = 0  # Initialize error counter

while True:
    voice_data = record_audio()
    if voice_data:
        print(f"You said: {voice_data}")
        respond(voice_data)
        error_count = 0  # Reset error counter after a successful recognition
    else:
        error_count += 1
        if error_count > 2:
            shivi_speaks("or kya kar rahe ho") and shivi_speaks("Kuch bolo") and shivi_speaks("kya kar rahe ho aap")
            error_count = 0  # Reset error counter after prompting the user
        else:
            print("I didn't get that, listening again...")
