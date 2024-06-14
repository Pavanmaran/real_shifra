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

# Initialize recognizer
r = sr.Recognizer()

def load_chat_prompts(file_path: str) -> Dict[str, str]:
    """Load chat prompts from a JSON file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Load chat prompts
chat_prompts = load_chat_prompts('promts.json')

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
        print("Say something : ")
        audio = r.listen(source)
        try:
            voice_data = r.recognize_google(audio)
            return voice_data
        except sr.UnknownValueError:
            return "I didn't get that"
        except sr.RequestError:
            return "Sorry, the service is down"
        except Exception:
            return "An error occurred"

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
    best_match = find_best_match(voice_data, chat_prompts)
    if best_match:
        if best_match == "play songs":
            url = 'https://www.youtube.com/watch?v=-PZDNZK4ctg'
            webbrowser.get().open(url)
        shivi_speaks(chat_prompts[best_match])
        if best_match == "stop":
            exit()
    else:
        shivi_speaks('Sorry, I did not understand that command')

# Main loop
shivi_speaks('Hello Pawan, Kese Ho aap ?')
while True:
    voice_data = record_audio()
    print(voice_data)
    respond(voice_data)
