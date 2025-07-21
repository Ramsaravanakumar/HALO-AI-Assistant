import sounddevice as sd
import joblib
import numpy as np
import librosa
from scipy.io.wavfile import write
import pyttsx3  # Text-to-speech library
import cmd
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import pyjokes
import os
import requests
import subprocess
import webbrowser
import time
import itertools
import tkinter as tk
import threading

def extract_features(file):
    audio, sr = librosa.load(file)
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
    return np.mean(mfcc.T, axis=0)

# Load the model
def load_model():
    return joblib.load("voice_authentication_model.pkl")

# Function to speak text (Text-to-Speech)
def speak(text):
    engine = pyttsx3.init()  # Initialize the pyttsx3 engine
    engine.say(text)  # Say the text
    engine.runAndWait()  # Wait until the speech is finished

# Authenticate the user
def authenticate_user():
    print("Please speak into the microphone for voice authentication...")
    speak("Please speak into the microphone for voice authentication")
    filename = "authentication_sample.wav"
    
    # Record the user's voice sample
    fs = 44100
    duration = 3
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    write(filename, fs, recording)
    print(f"Authentication sample saved as {filename}")

    # Extract features from the recorded audio
    features = extract_features(filename)

    # Load the trained model
    model = load_model()

    # Predict if the sample matches the user's voice (1 for match, 0 for no match)
    prediction = model.predict([features])[0]
    if prediction == 1:
        print("✅ Access granted. Welcome, boss!")
        speak("You are my boss.")  # TTS response when access is granted
    else:
        print("❌ Access denied. Voice not recognized.")
        speak("Access denied.")  # TTS response when access is denied

# Run the authentication
authenticate_user()
engine = pyttsx3.init()
recognizer = sr.Recognizer()


engine = pyttsx3.init()

engine.runAndWait()

def speak(text):
    print(f"HALO: {text}")
    engine.say(text)
    engine.runAndWait()



# Modified listen function
def listen():
    with sr.Microphone() as source:
        print("Listening..." )
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand.")
        except sr.RequestError:
            speak("Speech service is not available right now.")
    return ""

def get_weather():
    speak("Sure. Please tell me the city name.")
    city = listen()  # Ask the user to speak the city name

    if not city:
        speak("I didn't catch the city name.")
        return

    api_key = "bca3d547fd7fadaf7184343301a91a2d"  # Replace with your real API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url).json()
        if response["cod"] == 200:
            temp = response["main"]["temp"]
            desc = response["weather"][0]["description"]
            speak(f"The weather in {city} is {desc} with a temperature of {temp}°C.")
        else:
            speak(f"Sorry, I couldn't find weather data for {city}.")
    except:
        speak("Sorry, I couldn't connect to the weather service.")
import time

# Function to handle the wait command for a specific number of minutes
def wait_for_minutes(minutes):
    speak(f"Okay, I will wait for {minutes} minutes.")
    time.sleep(minutes * 60)  # Wait for the specified number of minutes (converted to seconds)
    speak(f"{minutes} minutes are over. Do you have any other tasks for me? Just let me know.")


def open_website(command):
    # Predefined website mappings
    website_map = {
        "chatgpt": "https://chat.openai.com",
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "gmail": "https://mail.google.com",
        "stackoverflow": "https://stackoverflow.com",
        "github": "https://github.com",
        "kaggle": "https://www.kaggle.com",
        "facebook": "https://www.facebook.com",
        "instagram": "https://www.instagram.com",
        "twitter": "https://www.twitter.com",
        "linkedin": "https://www.linkedin.com"
    }

    # Match known site names
    for site in website_map:
        if site in command:
            speak(f"Opening {site}")
            webbrowser.open(website_map[site])
            return

    # Fallback for "open <site>" pattern
    words = command.split()
    for i, word in enumerate(words):
        if word == "open" and i + 1 < len(words):
            site = words[i + 1].lower().replace(".", "")
            url = f"https://{site}.com"
            speak(f"Opening {site}")
            webbrowser.open(url)
            return

    speak("Sorry, I couldn't find the website name.")


    # Check for any known site in the user's command
    for site in known_sites:
        if site in command:
            speak(f"Opening {site}")
            webbrowser.open(known_sites[site])
            return

    # If no known site matched
    speak("Sorry, I couldn't find the website name.")
def close_website(command):
    website_keywords = [
        "chatgpt", "youtube", "google", "gmail", "stackoverflow",
        "github", "kaggle", "facebook", "instagram", "twitter", "linkedin"
    ]
    for site in website_keywords:
        if site in command:
            speak(f"Please close the {site} tab manually, HALO cannot force close browser tabs yet.")
            return
    speak("I couldn't find which website you want to close.")
    close_website(command)

def open_calculator():
    speak("Opening Calculator")
    os.system("start calc")



def close_calculator():
    speak("Closing Calculator.")
    try:
        # List all running tasks
        tasklist = subprocess.check_output('tasklist', shell=True).decode()

        # Check for the process name of CalculatorApp
        if "CalculatorApp.exe" in tasklist:
            os.system("taskkill /f /im CalculatorApp.exe >nul 2>&1")
            speak("Calculator closed.")
        else:
            speak("Calculator is not running.")
    except Exception as e:
        speak(f"Error: {str(e)}")

# Function to speak (for testing purposes)

def open_app(command):
    commands = {
        # Core System Apps
        "settings": "start ms-settings:",
        "file explorer": "explorer",
        "task manager": "taskmgr",
        "control panel": "control",

        # Media & Camera
        "camera": "start microsoft.windows.camera:",
        "photos": "start microsoft.windows.photos:",
        "video editor": "start microsoft.videoeditor:",

        # Microsoft Tools
        "microsoft store": "start ms-windows-store:",
        "xbox": "start xbox:",
        "mail": "start outlookmail:",
        "calendar": "start outlookcal:",

        # Custom Tools
        "notepad": "notepad",
        "paint": "mspaint",
        
    }

    for name, exe in commands.items():
        if name in command:
            speak(f"Launching {name}.")
            try:
                # Preferred on Windows
                os.startfile(exe)
            except AttributeError:
                # Fallback for subprocess
                subprocess.Popen([exe])
            return
    speak("I can't find that app on your PC.")
import os

def close_app(command):
    # Dictionary of apps and their corresponding executable names
    app_processes = {
        "settings": "SystemSettings.exe",
        "file explorer": "explorer.exe",
        "task manager": "taskmgr.exe",
        "control panel": "control.exe",
        "camera": "WindowsCamera.exe",
        "photos": "Microsoft.Photos.exe",
        "video editor": "VideoEditor.exe",
        "microsoft store": "WinStore.App.exe",
        "xbox": "xboxapp.exe",
        "mail": "outlook.exe",
        "calendar": "calendarmodern.exe",
        "notepad": "notepad.exe",
        "paint": "mspmsn.exe"
    }

    # Check if any of the phrases are in the command and close the respective app
    for command, process_name in app_processes.items():
        if any(phrase in command for phrase in [f"close {command}", f"close the {command}", f"close {command} app"]):
            os.system(f"taskkill /f /im {process_name}")  # Close the application
            speak(f"Closed {command}.")
            return

    speak("I don't recognize the application to close.")


def control_bluetooth(command):
    if any(k in command for k in ["on", "enable"]):
        speak("Opening Bluetooth settings. Please enable Bluetooth.")
    elif any(k in command for k in ["off", "disable"]):
        speak("Opening Bluetooth settings. Please disable Bluetooth.")
    else:
        speak("Do you want Bluetooth on or off?")
        return
    os.system("start ms-settings:bluetooth")
def close_bluetooth_settings():
    try:
        subprocess.run("taskkill /f /im SystemSettings.exe", shell=True)
        speak("Bluetooth settings closed.")
    except Exception as e:
        speak(f"Unable to close Bluetooth settings: {str(e)}")

# Wi-Fi control
def control_wifi(command):
    if any(k in command for k in ["on", "enable"]):
        speak("Opening Wi-Fi settings. Please enable Wi-Fi.")
    elif any(k in command for k in ["off", "disable"]):
        speak("Opening Wi-Fi settings. Please disable Wi-Fi.")
    else:
        speak("Do you want Wi-Fi on or off?")
        return
    os.system("start ms-settings:network-wifi")

# Volume control
def control_volume(command):
    if any(k in command for k in ["volume up", "increase volume", "turn up volume"]):
        speak("Opening sound settings. Please adjust the volume.")
        os.system("start ms-settings:sound")
    elif any(k in command for k in ["volume down", "decrease volume", "turn down volume"]):
        speak("Opening sound settings. Please adjust the volume.")
        os.system("start ms-settings:sound")
    elif any(k in command for k in ["mute", "mute volume", "silence"]):
        speak("Opening sound settings. Please mute the volume.")
        os.system("start ms-settings:sound")
    else:
        speak("Do you want to increase, decrease, or mute volume?")
def close_system_settings():
    try:
        subprocess.run("taskkill /f /im SystemSettings.exe", shell=True)
        speak("System settings window closed.")
    except Exception as e:
        speak(f"Could not close system settings: {str(e)}")
def respond_to_boss_query(command):
    if any(k in command for k in ["who is your boss", "who created you", "who made you", "who is your owner","who"]):
        speak("You are my boss, Ram. I only respond to your voice.")
    else:
        speak("I'm not sure who you're referring to.")

# System controls
def system_control(command):
    if any(k in command for k in ["shutdown", "turn off computer", "power off"]):
        speak("Shutting down the system.")
        os.system("shutdown /s /t 5")
    elif any(k in command for k in ["restart", "reboot"]):
        speak("Restarting the system.")
        os.system("shutdown /r /t 5")
    elif any(k in command for k in ["lock", "lock workstation"]):
        speak("Locking the system.")
        os.system("rundll32.exe user32.dll,LockWorkStation")
    else:
        speak("Do you want to shutdown, restart, or lock?")

if __name__ == "__main__":
    speak("hi boss , I am Hallo, your AI assistant.")
    while True:
        command = listen()
        if not command:
            continue

        if any(phrase in command for phrase in ["bye", "quit", "goodbye", "stop assistant","poda "]):
            speak("Goodbye!")
            break

        elif any(phrase in command for phrase in ["your name", "who are you"]):
            speak("I am HALO, your personal AI assistant.")

        elif any(phrase in command for phrase in ["how are you", "how do you do"]):
            speak("I'm doing great, always ready to help you.")

        elif any(phrase in command for phrase in ["what time", "tell me the time", "current time", "time now"]):
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {current_time}.")
        elif any(k in command for k in ["who is your boss", "who created you", "who made you", "who is your owner","who"]):
             respond_to_boss_query(command)

        elif any(phrase in command for phrase in ["what date", "today's date", "tell me the date", "current date"]):
            today = datetime.datetime.now().strftime("%B %d, %Y")
            speak(f"Today's date is {today}.")

        elif any(phrase in command for phrase in ["tell me a joke", "can you tell a joke", "say a joke", "joke please", "make me laugh", "joke"]):
            joke = pyjokes.get_joke()
            speak(joke)

        elif any(phrase in command for phrase in ["weather", "tell me the weather", "how is the weather", "what's the weather like"]):
            get_weather()

        elif any(phrase in command for phrase in [
             "launch website",
             "open youtube", "launch youtube", "start youtube",
             "can you open google", "open google", "launch google", "go to google",
             "open instagram", "launch instagram", "go to instagram",
              "open facebook", "launch facebook", "go to facebook",
             "open twitter", "launch twitter", "go to twitter",
             "open linkedin", "launch linkedin", "please open linkedin", "go to linkedin",
             "open stack overflow", "launch stack overflow", "go to stack overflow",
             "open github", "launch github", "go to github",
             "open kaggle", "launch kaggle", "go to kaggle",
             "open spotify", "start spotify", "play on spotify",
            "open chat gpt", "open chatgpt", "go to chatgpt", "launch chatgpt", "chatgpt"]):
             open_website(command)


        


        elif any(phrase in command for phrase in ["bluetooth on", "bluetooth off", "enable bluetooth", "disable bluetooth"]):
            control_bluetooth(command)
        elif any(phrase in command for phrase in ["wifi on", "wifi off", "enable wifi", "disable wifi"]):
            control_wifi(command)
        elif any(phrase in command for phrase in ["volume up", "volume down", "mute"]):
            control_volume(command)
        elif any(phrase in command for phrase in ["shutdown", "restart", "lock"]):
            system_control(command)
        elif any(phrase in command for phrase in ["close bluetooth page", "close bluetooth window"]):
              close_bluetooth_settings()
        elif any(phrase in command for phrase in ["close settings", "exit settings", "close system settings"]):
             close_system_settings()
        elif any(phrase in command for phrase in ["open settings", "launch settings"]):
             speak("Opening Settings")
             os.system("start ms-settings:")

        elif any(phrase in command for phrase in ["open file explorer", "launch file explorer"]):
            os.system("explorer")

        elif any(phrase in command for phrase in ["open control panel", "launch control panel"]):
              speak("Opening Control Panel")  
              os.system("control")
        

        elif any(phrase in command for phrase in ["open gmail", "launch gmail"]): 
              speak("Opening Gmail")  
              webbrowser.open("https://mail.google.com")

        elif any(phrase in command for phrase in ["open microsoft store", "launch microsoft store"]):
                 speak("Opening Microsoft Store")
                 os.system("start ms-windows-store:")
        elif any(phrase in command for phrase in ["open calendar", "launch calendar"]):
                 speak("Opening calendar")
                 os.system("start outlookcal:")
        elif any(phrase in command for phrase in ["launch video editor", "open video editor"]):
                speak("Opening video editor")
                os.system("start vlc")  # Make sure VLC is installed and in PATH

        elif any(phrase in command for phrase in ["close video editor", "exit video editor"]):
                 os.system("taskkill /f /im vlc.exe")
                 speak("Video editor closed.")
        elif any(phrase in command for phrase in ["open environment", "launch environment"]):
                 speak("Opening environment")
                 os.system("start anaconda-navigator")  # or your script path

        elif any(phrase in command for phrase in ["close environment", "exit environment"]):
                 os.system("taskkill /f /im anaconda-navigator.exe")
                 speak("Environment closed.")
        elif any(phrase in command for phrase in ["open notepad", "launch notepad"]): 
                 speak("Opening Notepad")  
                 os.system("start notepad")

        

        elif any(phrase in command for phrase in ["close calendar", "exit calendar"]):
                   os.system("taskkill /f /im HxCalendarAppImm.exe")
                   speak("Calendar closed.")

        elif any(phrase in command for phrase in ["close settings", "exit settings"]):
                 speak("Settings closed.")

        elif any(phrase in command for phrase in ["close file explorer", "exit file explorer"]):
                  os.system("taskkill /f /im explorer.exe && start explorer.exe")  # Restart to prevent system freeze
                  speak("File Explorer closed and restarted.")

        elif any(phrase in command for phrase in ["close control panel", "exit control panel"]):
                  os.system("taskkill /f /im control.exe")
                  speak("Control Panel closed.")

        elif any(phrase in command for phrase in ["close microsoft store", "exit microsoft store"]):
                  os.system("taskkill /f /im WinStore.App.exe")
                  speak("Microsoft Store closed.")
        elif any(phrase in command for phrase in ["open camera", "launch camera"]):
                  speak("Opening Camera")
                  os.system("start microsoft.windows.camera:")
        elif any(phrase in command for phrase in ["open calculator", "start calculator", "launch calculator"]):
                    open_calculator()

        elif any(phrase in command for phrase in ["close calculator", "exit calculator", "turn off calculator"]):
                     close_calculator()

        elif any(phrase in command for phrase in ["open photos", "launch photos"]):
                  speak("Opening Photos")
                  os.system("start microsoft.windows.photos:")

        elif any(phrase in command for phrase in ["open movies", "launch movies and tv"]):
                  speak("Opening Movies & TV")
                  os.system("start mswindowsvideo:")

        elif any(phrase in command for phrase in ["open media player", "launch media player"]):
                  speak("Opening Media Player")
                  os.system("start wmplayer")
        elif any(phrase in command for phrase in ["close camera", "exit camera"]):
                  os.system("taskkill /f /im WindowsCamera.exe")
                  speak("Camera closed.")

        elif any(phrase in command for phrase in ["close photos", "exit photos"]):
                  os.system("taskkill /f /im Microsoft.Photos.exe")
             
        elif any(phrase in command for phrase in ["close movies", "exit movies and tv"]):
                  os.system("taskkill /f /im Video.UI.exe")
                  speak("Movies & TV closed.")

        elif any(phrase in command for phrase in ["close media player", "exit media player"]):
                  os.system("taskkill /f /im wmplayer.exe")
                  speak("Media Player closed.")
        elif any(phrase in command for phrase in ["open onedrive", "launch onedrive"]):
                  speak("Opening OneDrive")
                  os.system("start onedrive")

        elif any(phrase in command for phrase in ["open xbox", "launch xbox"]):
                  speak("Opening Xbox")
                  os.system("start xbox:")
        elif any(phrase in command for phrase in ["close app", "exit notepad", "close camera"]):
                 close_app(command)
        elif any(phrase in command for phrase in ["open your phone", "open phone link"]):
                  speak("Opening Phone Link")
                  os.system("start ms-phone:")

        
        elif any(phrase in command for phrase in ["close onedrive", "exit onedrive"]):
                  os.system("taskkill /f /im OneDrive.exe")
                  speak("OneDrive closed.")

        elif any(phrase in command for phrase in ["close xbox", "exit xbox"]):
                   os.system("taskkill /f /im GameBar.exe")

                   speak("Xbox closed.")

        elif any(phrase in command for phrase in ["close phone link", "exit phone link"]):
                  os.system("taskkill /f /im YourPhone.exe")
                  speak("Phone Link closed.")

        elif any(phrase in command for phrase in ["open mail", "launch mail"]):
               speak("Opening Mail")
               os.system("start outlookmail:")  # Opens Windows Mail app

        elif any(phrase in command for phrase in ["close mail", "exit mail"]):
              os.system("taskkill /f /im HxMail.exe")  # or HxTsr.exe depending on version
              speak("Mail app closed.")

        elif any(phrase in command for phrase in ["close chatgpt", "close the chatgpt page", "close chatgpt tab"]):
                 os.system("taskkill /f /im chrome.exe")  # Adjust for your browser if necessary
                 speak("Closed ChatGPT.")
        elif any(phrase in command for phrase in ["close youtube", "close the youtube page", "close youtube tab"]):
                  os.system("taskkill /f /im msedge.exe")
                  speak("Closed YouTube.")
  
        elif any(phrase in command for phrase in ["close google", "close the google page", "close google tab"]):
                os.system("taskkill /f /im msedge.exe")
                speak("Closed Google.")

        elif any(phrase in command for phrase in ["close gmail", "exit gmail", "close the gmail"]):
                os.system("taskkill /f /im msedge.exe")
                speak("Gmail closed by exiting Microsoft Edge.")


        elif any(phrase in command for phrase in ["close stackoverflow", "close the stackoverflow page", "close stackoverflow tab"]):
               os.system("taskkill /f /im msedge.exe")
               speak("Closed StackOverflow.")
 
        elif any(phrase in command for phrase in ["close github", "close the github page", "close github tab"]):
                os.system("taskkill /f /im msedge.exe")
                speak("Closed GitHub.")

        elif any(phrase in command for phrase in ["close kaggle", "close the kaggle page", "close kaggle tab"]):
                 os.system("taskkill /f /im msedge.exe")
                 speak("Closed Kaggle.")

        elif any(phrase in command for phrase in ["close facebook", "close the facebook page", "close facebook tab"]):
                os.system("taskkill /f /im msedge.exe")
                speak("Closed Facebook.")

        elif any(phrase in command for phrase in ["close instagram", "close the instagram page", "close instagram tab"]):
                os.system("taskkill /f /im msedge.exe")
                speak("Closed Instagram.")

        elif any(phrase in command for phrase in ["close twitter", "close the twitter page", "close twitter tab"]):
                os.system("taskkill /f /im msedge.exe")
                speak("Closed Twitter.")

        elif any(phrase in command for phrase in ["close linkedin", "close the linkedin page", "close linkedin tab"]):
                os.system("taskkill /f /im msedge.exe")
                speak("Closed LinkedIn.")
        elif any(phrase in command for phrase in ["close settings", "close the settings", "close settings app"]):
                   os.system("taskkill /f /im SystemSettings.exe")
                   speak("Closed Settings.")
        elif any(phrase in command for phrase in ["close file explorer", "close the file explorer"]):
                   os.system("taskkill /f /im explorer.exe")
                   speak("Closed File Explorer.")
        elif any(phrase in command for phrase in ["close task manager", "close the task manager"]):
                    os.system("taskkill /f /im taskmgr.exe")
                    speak("Closed Task Manager.")
        elif any(phrase in command for phrase in ["close control panel", "exit control panel"]):
                 os.system('powershell "Get-Process | Where-Object {$_.MainWindowTitle -like \'*Control Panel*\'} | ForEach-Object { $_.CloseMainWindow() | Out-Null }"')
                 speak("Control Panel closed.")


        elif any(phrase in command for phrase in ["close camera", "close the camera", "close camera app"]):
                       os.system("taskkill /f /im WindowsCamera.exe")
                       speak("Closed Camera.")
        elif any(phrase in command for phrase in ["close photos", "close the photos app"]):
                       os.system("taskkill /f /im Microsoft.Photos.exe")
                       speak("Closed Photos.")
        elif any(phrase in command for phrase in ["close video editor", "close the video editor"]):
                        os.system("taskkill /f /im VideoEditor.exe")
                        speak("Closed Video Editor.")
        elif any(phrase in command for phrase in ["close microsoft store", "close the microsoft store"]):
                       os.system("taskkill /f /im WinStore.App.exe")
                       speak("Closed Microsoft Store.")
        elif any(phrase in command for phrase in ["close xbox", "close the xbox app"]):
                       os.system("taskkill /f /im GameBar.exe")
                       speak("Closed Xbox.")
        elif any(phrase in command for phrase in ["close mail", "close the mail app"]):
                         os.system("taskkill /f /im outlook.exe")
                         speak("Closed Mail.")
        elif any(phrase in command for phrase in ["close calendar", "close the calendar app"]):
                        os.system("taskkill /f /im calendarmodern.exe")
                        speak("Closed Calendar.")
        elif any(phrase in command for phrase in ["close notepad", "close the notepad"]):
                        os.system("taskkill /f /im notepad.exe")
                        speak("Closed Notepad.")
        elif any(phrase in command for phrase in ["close paint", "close the paint app"]):
                       os.system("taskkill /f /im mspmsn.exe")
                       speak("Closed Paint.")
        elif any(phrase in command for phrase in ["close chat gpt", "exit chat gpt"]):
                    os.system("taskkill /f /im msedge.exe")  # or "chrome.exe" / "firefox.exe"
                    speak("ChatGPT closed by closing the browser.")
        elif any(phrase in command for phrase in ["wait 5 minutes", "wait five minutes"]):
                  speak("Okay, I will wait for 5 minutes.")
                  time.sleep(5 * 60)  # Wait for 5 minutes (5 * 60 seconds)
                  speak("5 minutes are over. Do you have any other tasks for me? Just let me know.")
        elif any(phrase in command for phrase in ["wait 2 minutes", "wait two minutes"]):
                  speak("Okay, I will wait for 2 minutes.")
                  time.sleep(2 * 60)  # Wait for 5 minutes (5 * 60 seconds)
                  speak("2 minutes are over. Do you have any other tasks for me? Just let me know.")      
        else:
            speak("Sorry, I don't understand that yet.")