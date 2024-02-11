import speech_recognition as sr
import random
import webbrowser
from gtts import gTTS
import os
import pygame
import pygame.mixer
from difflib import SequenceMatcher

# Initialize recognizer
r = sr.Recognizer()

# Chat dictionary
chat_prompts = {
    "Hi Shiwani": "Hi Handsome! Kaise ho?",
    "theek hoon": "Soon kar maza aa gaya!",
    "kya kar rahi ho": "Bas tumhare liye wait kar rahi thi. Tum kya kar rahe ho?",
    "kuch nahi": "Kyun? Bored ho? Kuch interesting facts sunaoon?",
    "sunao": "Did you know that the average person takes 7 minutes to fall asleep?",
    "kesi ho pooja": "Main theek hoon. Tumhe kya chahiye?",

    "Do you love me?": "Always and forever.",
    "What's for dinner?": "I'm thinking Italian tonight. How about some pasta?",
    "Can we meet tomorrow?": "Yes, I'd love to. Where should we meet?",
    "I had a tough day": "I'm sorry to hear that. Want to talk about it?",
    "You look beautiful": "Thank you! You always make me blush.",
    "Let's plan a vacation": "Yes! I've been thinking about the beach. What do you think?",
    "I bought you a gift": "Aww, that's so sweet! Can't wait to see it.",
    "Remember our first date?": "Of course! It's one of my most cherished memories.",
    "Goodnight": "Goodnight! Sweet dreams. Talk to you tomorrow.",
    "hello Jarvis": "Hello! Pawan How can I assist you?",
    "how r u": "I am just a program, so I don't have feelings, but I'm functioning properly. How can I assist you?",
    "How are you?": "Main theek hoon, aur tum?",
    "hello Jarvis": "Namaste! Pawan, kaise madad kar sakta hoon?",
    "play songs": "Yeh rahe gaane apke liye. Enjoy karo!",  # The URL opening action will be handled separately
    "stop": "Theek hai, alvida!",
    "kya chal raha hai": "Main toh bas yahin hoon apke pass, apki baten enjoy kar rahi hun. Batao kaise madad kar sakti hoon apki?",
    "batao joke": "Kyun nahi! Suno toh... Why did the chicken join a band? Kyunki usko drum pasand tha!",
    "thanks yaar": "Koi baat nahi! Hamesha madad ke liye yahaan hoon.",
    "kuch naya sunao": "Kya sunna pasand karoge? Kuch gaane ya fir kuch interesting facts?",
    "weather kaisa hai": "Maaf karo, mujhe real-time weather check karne ki capability nahi hai. Lekin tum kisi weather website ya app ko check kar sakte ho.",
    "himanshu kaisa hai": "Himanshu toh bahut hi Chootiya hai! dil karta he uske mooh me land de du",
}

def find_best_match(input_text, prompts):
    """Find the closest match in the chat prompts."""
    max_similarity = 0
    best_match = None
    for prompt in prompts:
        similarity = SequenceMatcher(None, input_text, prompt).ratio()
        if similarity > max_similarity:
            max_similarity = similarity
            best_match = prompt
    return best_match if max_similarity > 0.5 else None

def record_audio():
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
        except:
            return "An error occurred"

def shivi_speaks(audio_string):
    tts = gTTS(text=audio_string, slow=False, lang='hi')
    r = random.randint(1, 100000000)
    audio_file = 'audio-' + str(r) + '.mp3'
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

def respond(voice_data):
    """Respond to user's voice command."""
    best_match = find_best_match(voice_data, chat_prompts.keys())
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
