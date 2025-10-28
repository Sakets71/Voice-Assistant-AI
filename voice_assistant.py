import os
import time
import datetime
import subprocess
import webbrowser
import requests
import pyttsx3
import speech_recognition as sr
import wikipedia
import pywhatkit
import pyautogui
import wolframalpha
from ecapture import ecapture as ec
from fuzzywuzzy import fuzz

# ---------- CONFIG ----------
ASSISTANT_NAME = "Saket " 
WEATHER_API_KEY = ""
WOLFRAM_APP_ID = ""

HF_API_TOKEN = None  # Set to your Hugging Face API token if available
HF_CHAT_MODEL = "google/gemma-2b-it"  # recommended free model endpoint

wolfram_client = wolframalpha.Client(WOLFRAM_APP_ID)

NOTES_FILE = f"{ASSISTANT_NAME.lower()}_notes.txt"

# ---------- TTS ----------
def speak(text):
    """Print + speak text. Reinitializes TTS engine each call to avoid 'one-shot' bug."""
    print(f"🧠 {ASSISTANT_NAME}: {text}")
    try:
        engine = pyttsx3.init("sapi5")
        voices = engine.getProperty("voices")
        if voices:
            engine.setProperty("voice", voices[0].id)
        engine.setProperty("rate", 175)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print("Speech error:", e)


# ---------- INPUT ----------
def take_input():
    """Prompt user to choose voice or text input, then return the lowercased statement."""
    choice = input("Input Mode - (1) Voice  (2) Text : ").strip()
    if choice == "1":
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print(" Listening...")
            r.pause_threshold = 1
            try:
                audio = r.listen(source, timeout=7, phrase_time_limit=8)
                statement = r.recognize_google(audio, language="en-in")
                print(f" You said: {statement}")
                return statement.lower().strip()
            except sr.WaitTimeoutError:
                speak("Listening timed out. Try again.")
                return ""
            except sr.UnknownValueError:
                speak("Sorry, I couldn't understand you.")
                return ""
            except Exception as e:
                print("Microphone error:", e)
                speak("Sorry, I couldn't hear that.")
                return ""
    else:
        statement = input("Type your command: ").strip()
        return statement.lower()


# ---------- NLU ----------
def detect_intent(statement):
    """Simple intent classification using keyword sets + fuzzy matching."""
    if not statement:
        return "unknown"

    intents = {
        "open_website": ["open", "launch", "visit", "browse"],
        "search_web": ["search", "find", "google", "look for"],
        "play_youtube": ["play", "youtube", "song", "video"],
        "wikipedia": ["who is", "what is", "tell me about", "wikipedia"],
        "weather": ["weather", "temperature", "climate"],
        "note": ["note", "remember", "write down"],
        "reminder": ["remind", "reminder"],
        "wolfram": ["calculate", "math", "solve", "what is", "how many", "convert"],
        "time": ["time","minute","only","just"],
        "camera": ["camera", "photo", "picture"],
        "chat": ["talk", "chat", "gpt", "conversation"],
        "system": ["notepad", "code", "calculator", "screenshot", "log off", "shutdown", "folder"],
        "exit": ["good bye", "bye", "exit", "stop", "quit"],
       
    }

    best_intent = "unknown"
    best_score = 0
    for intent, keywords in intents.items():
        for key in keywords:
            score = fuzz.partial_ratio(key, statement)
            if score > best_score and score > 70:
                best_score = score
                best_intent = intent

    print(f"🔍 Intent recognized: {best_intent} (score {best_score})")
    return best_intent


# ---------- FEATURES ----------
def open_website(statement):
    if "youtube" in statement:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube.")
    elif "google" in statement:
        webbrowser.open("https://www.google.com")
        speak("Opening Google.")
    elif "gmail" in statement:
        webbrowser.open("https://mail.google.com")
        speak("Opening Gmail.")
    elif "stackoverflow" in statement:
        webbrowser.open("https://stackoverflow.com")
        speak("Opening Stack Overflow.")
    else:
        speak("Which website should I open? (say domain without https)")
        site = take_input()
        if site:
            if not site.startswith("http"):
                url = f"https://{site}"
            else:
                url = site
            webbrowser.open(url)
            speak(f"Opening {site}.")


def search_web(statement):
    query = statement.replace("search", "").replace("google", "").strip()
    if not query:
        speak("What should I search for?")
        query = take_input()
    if query:
        webbrowser.open(f"https://www.google.com/search?q={query}")
        speak(f"Searching Google for {query}.")


def play_youtube(statement):
    query = statement.replace("play", "").replace("youtube", "").strip()
    if not query:
        speak("What should I play on YouTube?")
        query = take_input()
    if query:
        try:
            pywhatkit.playonyt(query)
            speak(f"Playing {query} on YouTube.")
        except Exception as e:
            print("YouTube play error:", e)
            speak("Sorry, I couldn't play that on YouTube.")


def get_weather(_statement=None):
    speak("Please tell me the city.")
    city = take_input()
    if not city:
        speak("City name not provided.")
        return
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if data.get("cod") != 200:
            speak("I couldn't find the weather for that city.")
            return
        desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        speak(f"The weather in {city} is {desc} with a temperature of {temp}°C and humidity {humidity} percent.")
    except Exception as e:
        print("Weather error:", e)
        speak("Sorry, I couldn't retrieve the weather.")


def search_wikipedia(statement):
    query = statement.replace("wikipedia", "").strip()
    if not query:
        speak("What should I look up on Wikipedia?")
        query = take_input()
    if not query:
        speak("No query provided.")
        return
    try:
        results = wikipedia.summary(query, sentences=2, auto_suggest=True, redirect=True)
        speak(f"According to Wikipedia: {results}")
    except Exception as e:
        print("Wikipedia error:", e)
        speak("Sorry, I couldn't find results on Wikipedia.")


def add_note():
    speak("What should I note down?")
    note = take_input()
    if not note:
        speak("No note provided.")
        return
    try:
        with open(NOTES_FILE, "a", encoding="utf-8") as f:
            f.write(f"{datetime.datetime.now()}: {note}\n")
        speak("Note saved successfully!")
    except Exception as e:
        print("File write error:", e)
        speak("Sorry, I couldn't save the note.")


def show_notes():
    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            notes = f.read()
        if notes:
            speak("Here are your notes.")
            print(notes)
        else:
            speak("You have no notes.")
    except FileNotFoundError:
        speak("No notes found.")


def set_reminder():
    speak("What should I remind you about?")
    reminder = take_input()
    if not reminder:
        speak("No reminder provided.")
        return
    speak("In how many minutes?")
    try:
        minutes = int(take_input())
        speak(f"Reminder set for {minutes} minutes.")
        time.sleep(minutes * 60)
        speak(f"Reminder: {reminder}")
    except ValueError:
        speak("Invalid time input.")
    except Exception as e:
        print("Reminder error:", e)
        speak("I couldn't set the reminder.")


def ask_wolfram():
    speak("What would you like to calculate?")
    question = take_input()
    if not question:
        speak("No question provided.")
        return
    try:
        res = wolfram_client.query(question)
        answer = next(res.results).text
        speak(answer)
    except Exception as e:
        print("Wolfram error:", e)
        speak("Sorry, I couldn't find an answer.")


def chat_with_gpt():
    speak("What do you want to talk about?")
    user_msg = take_input()
    if not user_msg:
        speak("No input received.")
        return

    headers = {"Content-Type": "application/json"}
    if HF_API_TOKEN:
        headers["Authorization"] = f"Bearer {HF_API_TOKEN}"

    payload = {"inputs": user_msg}
    url = f"https://api-inference.huggingface.co/models/{HF_CHAT_MODEL}"

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            answer = None
            # possible response shapes:
            # - [{"generated_text": "..."}]
            # - {"generated_text": "..."}
            if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
                answer = data[0].get("generated_text") or data[0].get("text")
            elif isinstance(data, dict):
                answer = data.get("generated_text") or data.get("text") or data.get("error")
            if not answer:
                answer = "Sorry, I couldn't generate a response. The model might be busy."
        else:
            print("HF status:", resp.status_code, resp.text)
            answer = "The AI service is busy or requires an API token. Try again later or set HF_API_TOKEN."
    except requests.RequestException as e:
        print("Chat request error:", e)
        answer = "Sorry, I couldn't connect to the AI service."

    speak(answer)


def system_control(statement):
    try:
        if "notepad" in statement:
            os.system("notepad")
            speak("Opening Notepad.")
        elif "calculator" in statement:
            subprocess.Popen("calc.exe")
            speak("Opening Calculator.")
        elif "vs code" in statement or "code" in statement:
            # Try to run 'code' command first, fallback to common install path
            try:
                subprocess.Popen(["code"])
                speak("Opening Visual Studio Code.")
            except Exception:
                possible = os.path.expanduser(r"C:\Users\%s\AppData\Local\Programs\Microsoft VS Code\Code.exe" % os.getlogin())
                if os.path.exists(possible):
                    subprocess.Popen([possible])
                    speak("Opening Visual Studio Code.")
                else:
                    speak("Could not open VS Code. Please open it manually.")
        elif "screenshot" in statement:
            path = "screenshot.png"
            pyautogui.screenshot(path)
            speak("Screenshot taken.")
        elif "folder" in statement:
            folder_path = os.path.join(os.path.expanduser("~"), "Documents")
            try:
                os.startfile(folder_path)
                speak("Opening Documents folder.")
            except Exception:
                speak("Cannot open Documents folder.")
        elif "log off" in statement or "shutdown" in statement:
            speak("Logging off in 10 seconds. Please save your work.")
            subprocess.call(["shutdown", "/l"])
    except Exception as e:
        print("System control error:", e)
        speak("Sorry, I couldn't perform that system action.")


# ---------- GREETING ----------
def greet_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        greet = "Good morning"
    elif hour < 18:
        greet = "Good afternoon"
    else:
        greet = "Good evening"
    speak(f"{greet}! I am {ASSISTANT_NAME}, your AI assistant. How can I help you today?")


# ---------- MAIN ----------
def main():
    greet_user()
    while True:
        statement = take_input()
        if not statement:
            continue

        intent = detect_intent(statement)

        if intent == "exit":
            speak("Goodbye! Have a nice day.")
            break
        elif intent == "open_website":
            open_website(statement)
        elif intent == "search_web":
            search_web(statement)
        elif intent == "play_youtube":
            play_youtube(statement)
        elif intent == "weather":
            get_weather(statement)
        elif intent == "note":
            if "show" in statement:
                show_notes()
            else:
                add_note()
        elif intent == "reminder":
            set_reminder()
        elif intent == "wolfram":
            ask_wolfram()
        elif intent == "wikipedia":
            search_wikipedia(statement)
        elif intent == "chat":
            chat_with_gpt()
        elif intent == "system":
            system_control(statement)
        elif intent == "camera":
            try:
                ec.capture(0, f"{ASSISTANT_NAME} Camera", "photo.jpg")
                speak("Photo captured.")
            except Exception as e:
                print("Camera error:", e)
                speak("Could not capture photo.")
        elif intent == "time":
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {current_time}")
        else:
            speak("I'm not sure what you mean. Let me check with the AI service.")
            chat_with_gpt()


if __name__ == "__main__":
    main()
