import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import time
import musicLibrary


#NEWS_API_KEY = "d09353d72bc40248998159804e0e67d"
#MIC_INDEX = None   # Set mic index if needed (e.g. 1)

# ================== INIT ==================
recognizer = sr.Recognizer()
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True

engine = pyttsx3.init()

# ================== FUNCTIONS ==================
def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

def listen(timeout=8, phrase_time=5):
    with sr.Microphone(device_index=MIC_INDEX) as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time)
    return audio

def get_text(audio):
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        speak("Internet connection problem")
        return None

def process_command(command):
    command = command.lower()

    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")

    elif "open linkedin" in command:
        speak("Opening LinkedIn")
        webbrowser.open("https://www.linkedin.com")

    elif command.startswith("play"):
        song = command.split(" ", 1)[1]
        if song in musicLibrary.music:
            link=musicLibrary.music[song]
            webbrowser.open(link)
        else:
            speak("Song not found")

    elif "news" in command:
        speak("Fetching latest news")
        url = f"https://newsapi.org/v2/everything?q=india&language=en&apiKey={NEWS_API_KEY}"
        r = requests.get(url)

        if r.status_code == 200:
            articles = r.json().get("articles", [])
            if not articles:
                speak("No news available")
            for article in articles[:5]:
                speak(article["title"])
                time.sleep(0.5)
        else:
            speak("Failed to fetch news")
         

    else:
        #Let opem AI handle request
        pass
       

# ================== MAIN LOOP ==================
if __name__ == "__main__":
    speak("Initializing Jarvis")

    while True:
        try:
            print("Listening for wake word...")
            wake_audio = listen(timeout=8, phrase_time=3)
            wake_word = get_text(wake_audio)

            if wake_word and wake_word.lower() == "jarvis":
                speak("Yes")

                print("Jarvis active...")
                command_audio = listen(timeout=8, phrase_time=6)
                command = get_text(command_audio)

                if command:
                    print("You said:", command)
                    process_command(command)
                    time.sleep(2)
                else:
                    speak("I did not understand")

        except KeyboardInterrupt:
            print("\nExiting Jarvis")
            break

        except Exception as e:

            print("Error:", e)
