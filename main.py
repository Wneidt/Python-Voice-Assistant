import datetime
import os, sys
import time
import pyttsx3
import speech_recognition as sr
import pytz
import subprocess
import webbrowser
import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import bleach
import pyowm

firefox_path = "Mozilla Firefox\\firefox.exe" #Your path to whichever browser you use
webbrowser.register('firefox', None,webbrowser.BackgroundBrowser(firefox_path)) 

owm = pyowm.OWM('bf8709382889f09ca061086740f533cf') #Provide your own key


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception: " + str(e))
            
    return said.lower()


def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])

def get_time_in_city(city):
    try:
        website = "https://time.is/london"
        hdr = {'User-Agent': 'Mozilla/5.0'}
        page = Request(website,headers=hdr)
        page = urlopen(page)
        soup = BeautifulSoup(page,"lxml")
        time = soup.findAll("div", {"id": "twd"})
        time = " ".join(str(x) for x in time)
        time = time[:-6]
        time = time[14:]
        print(time)
        return time
    except:
        return "Unable to get time of that area"

def get_weather(city):
    try:
        obs = owm.weather_at_place(city)
        w = obs.get_weather()
        speak("Temperature is " + str(w.get_temperature('celsius')['temp']))
        speak("Weather is " + str(w.get_detailed_status()))
        speak("Wind speed is " + str(w.get_wind()['speed']))
        speak("Humidity is " + str(w.get_humidity()))
    except:
        speak("I couldn't find any weather information for that area") 


WAKE = ["hey sam","hi sam", "sam"]

print("Start")

while True:
    print("Listening")
    text = get_audio()

    for phrase in WAKE:
        if phrase in text:
            speak("I am ready")
            text = get_audio()

            TIME_STRS = ["what time is it", "what time it is", "say time", "tell time", "current time", "time in my area", "tell time", "say me time", "tell me time"]       
            for phrase in TIME_STRS:
                if phrase in text:
                    speak("Time in your area is " + time.strftime("%H:%M"))

            DATE_STRS = ["what date it is", "what date is it", "tell me date", "tell date", "say date" ]       
            for phrase in DATE_STRS:
                if phrase in text:
                    speak("Today is " +time.strftime("%A") +time.strftime("%B %d, %Y"))


            NOTE_STRS = ["make a note", "write this down", "remember this"]
            for phrase in NOTE_STRS:
                if phrase in text:
                    speak("What would you like me to write down?")
                    note_text = get_audio()
                    note(note_text)
                    speak("I've made a note of that.")

            WEB_STRS = ["open website", "open link", "open the website", "open a website"]
            for phrase in WEB_STRS:
                if phrase in text:
                    speak("Say the name website where you want to go")
                    url = get_audio()
                    url = "https://www."+ url
                    try:
                        webbrowser.get('firefox').open_new_tab(url)
                        speak("Here you are")
                    except:
                        speak("I couldn't find that website")

            GOOGLE_STRS = ["search in google", "google for me", "search", "google", "search for me"]    
            for phrase in GOOGLE_STRS:
                if phrase in text:  
                    speak("Say what do you want me to search")
                    search = get_audio()
                    search = "https://www.google.com/search?q=" + search
                    try:
                        webbrowser.get('firefox').open_new_tab(search)
                        speak("Here you are")
                    except:
                        speak("I couldn't search for that")

            END_STRS = ["end program", "terminate", "close it", "shut down", "end it", "kill program"," stop it", "stop everything", "close", "close program"]
            for phrase in END_STRS:
                if phrase in text:  
                    speak("I am shutting down")
                    sys.exit()

            CITY_TIME_STRS = ["tell me time in a city", " what's the time in another city", "tell me time somewhere", "say time in a city", "say me time somewhere", "time somewhere"]
            for phrase in CITY_TIME_STRS:
                if phrase in text:  
                    speak("In which city you want to know time?")
                    city = get_audio()
                    speak("Time there is" + str(get_time_in_city(city)))

            WEATHER_STRS = ["tell me weather", "tell weather", "say me weather", "what is weather", "say weather"]
            for phrase in WEATHER_STRS:
                if phrase in text:
                    speak("In which city you want to know weather?")
                    city = get_audio()
                    get_weather(city)
















