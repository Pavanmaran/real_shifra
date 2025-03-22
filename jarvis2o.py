import speech_recognition as sr
import random
import webbrowser
from gtts import gTTS
import os
import pygame
import pygame.mixer
from typing import Optional
import google.generativeai as genai

# Initialize recognizer
r = sr.Recognizer()

# Configure the Google AI Python SDK
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "AIzaSyATtV86B2Hzv9C_jFfF8tFzrdvmtc-q7kY"

genai.configure(api_key=os.environ["GOOGLE_APPLICATION_CREDENTIALS"])

# Create the model
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
)

def record_audio() -> Optional[str]:
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
    """Convert text to speech and play it."""
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

def query_gemini(input_text: str) -> str:
    """Query the Gemini API for a response."""
    chat_session = model.start_chat(
        history=[
            {"role": "user", "parts": [{"text": input_text}]}
        ]
    )
    response = chat_session.send_message(input_text)
    return response.text

def respond(voice_data: str):
    """Respond to user's voice command using the Gemini API."""
    gemini_response = query_gemini(voice_data)
    shivi_speaks(gemini_response)

# Main loop
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
