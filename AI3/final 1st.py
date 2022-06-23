import datetime

import PyPDF2
import pywikihow
from google.auth.transport import requests
from prompt_toolkit.keys import Keys
from selenium.webdriver.chrome import webdriver
import sys
from Jarvis import JarvisAssistant
import speech_recognition as sr
import pyttsx3
import wikipedia
import pyjokes
import re
import pprint
import pywhatkit
import os
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer,QTime,QDate,Qt
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from gui import Ui_MainWindow

import smtplib

from Jarvis.config import config
def google_search(command):

    reg_ex = re.search('search google for (.*)', command)
    search_for = command.split("for", 1)[1]
    url = 'https://www.google.com/'
    if reg_ex:
        subgoogle = reg_ex.group(1)
        url = url + 'r/' + subgoogle
    speak("Okay sir!")
    speak(f"Searching for {subgoogle}")
    driver = webdriver.Chrome(
        executable_path='driver/chromedriver.exe')
    driver.get('https://www.google.com')
    search = driver.find_element_by_name('q')
    search.send_keys(str(search_for))
    search.send_keys(Keys.RETURN)


def fetch_weather(city):
    """
    City to weather
    :param city: City
    :return: weather
    """
    api_key = config.weather_api_key
    units_format = "&units=metric"

    base_url = "http://api.openweathermap.org/data/2.5/weather?q="
    complete_url = base_url + city + "&appid=" + api_key + units_format

    response = requests.get(complete_url)

    city_weather_data = response.json()

    if city_weather_data["cod"] != "404":
        main_data = city_weather_data["main"]
        weather_description_data = city_weather_data["weather"][0]
        weather_description = weather_description_data["description"]
        current_temperature = main_data["temp"]
        current_pressure = main_data["pressure"]
        current_humidity = main_data["humidity"]
        wind_data = city_weather_data["wind"]
        wind_speed = wind_data["speed"]

        final_response = f"""
        The weather in {city} is currently {weather_description} 
        with a temperature of {current_temperature} degree celcius, 
        atmospheric pressure of {current_pressure} hectoPascals, 
        humidity of {current_humidity} percent 
        and wind speed reaching {wind_speed} kilometers per hour"""

        return final_response

    else:
        return "Sorry Sir, I couldn't find the city in my database. Please try again"


engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
print(voices[0].id)
engine.setProperty('voice',voices[0].id)
engine.setProperty('rate',165)

obj = JarvisAssistant()
import webbrowser, requests
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import geocoder

def loc(place):
    webbrowser.open("http://www.google.com/maps/place/" + place + "")
    geolocator = Nominatim(user_agent="myGeocoder")
    location = geolocator.geocode(place, addressdetails=True)
    target_latlng = location.latitude, location.longitude
    location = location.raw['address']
    target_loc = {'city': location.get('city', ''),
                   'state': location.get('state', ''),
                   'country': location.get('country', '')}

    current_loc = geocoder.ip('me')
    current_latlng = current_loc.latlng

    distance = str(great_circle(current_latlng, target_latlng))
    distance = str(distance.split(' ',1)[0])
    distance = round(float(distance), 2)

    return current_loc, target_loc, distance

def my_location():
    ip_add = requests.get('https://api.ipify.org').text
    url = 'https://get.geojs.io/v1/ip/geo/' + ip_add + '.json'
    geo_requests = requests.get(url)
    geo_data = geo_requests.json()
    city = geo_data['city']
    state = geo_data['region']
    country = geo_data['country']

    return city, state,country


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    speak("I am Artificial Intelligence , face verification starts")
    speak("look at the camera please")
    speak("look at the camera please")
    speak("scanning")
    speak("scanning................")
    speak("scanning")
    speak("scanning")
    speak("scanning")
    speak("scanning")
    speak("scanning")
    speak("scanning")
    speak("face Verification successful")
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour <=12:
        speak("Good Morning! s")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening! ")
    speak("How can I help you Bishal sir")


def pdf_reader():
    book=open('abc.pdf','rb')
    pdfReader=PyPDF2.PdfFileReader(book)
    pages=pdfReader.numPages
    speak(f"Total number of page {pages}")
    speak("sir please enter the page number i have to read")
    pg=int(input("please enter the page number: "))
    page=pdfReader.getPage(pg)
    text=page.extractText(page)
    print("reach1")
    print(text)
    speak(text)
    print("reach2")

class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()




def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening......")
        r.pause_threshold=1
        audio=r.listen(source)

    try:
        print("Recognizing.....")
        query=r.recognize_google(audio,language='en-in')
        print("user said: ",query)
    except Exception as e:
        print(e)
        print("say that again please")
        return "None"
    return query

def sendEmail(to,content):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()

    server.login('bishal.saha04052002@gmail.com', 'lahsib@saha')

    server.sendmail('bishal.saha04052002@gmail.com',to,content)
    server.close()


class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.TaskExecution()

    def TaskExecution(self):


        wishMe()
        while True:
            query = takeCommand().lower()

            # logic for executing tasks based on query
            if 'wikipedia' in query:
                speak('Searching Wikipedia....')
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to wikipedia")
                print(results)
                speak(results)

            elif 'open youtube' in query:
                webbrowser.open("youtube.com")

            elif 'open google' in query:
                print('called')
                webbrowser.open("google.com")

            elif 'open stack overflow' in query:
                webbrowser.open("https://stackoverflow.com/")

            elif 'open game' in query:

                webbrowser.open("https://game.com/")


            elif 'open github' in query:
                webbrowser.open("github.com")

            elif 'play music' in query:
                music_dir = 'D:\Music'
                songs = os.listdir(music_dir)
                print(songs)
                os.startfile(os.path.join(music_dir, songs[0]))

            elif 'the time' in query:
                Time = datetime.datetime.now().strftime("%H:%M:%S")
                print(Time)
                speak(Time)

            elif 'open vs code' in query:
                path = "C:\\Users\\BISHAL SAHA\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                os.startfile(path)

            elif 'open pdf' in query:
                path = "D:\\"
                os.startfile(path)

            elif ' game' in query:
                path = "C:\\Users\\BISHAL SAHA\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs"
                os.startfile(path)

            elif 'send email to madhu' in query:
                try:
                    speak("what should I say")
                    content = takeCommand()
                    to = "madhumitasaha999@gmail.com"
                    sendEmail(to, content)
                    speak("Email has been send")
                except Exception as e:
                    print(e)
                    speak("Sorry bhai")

            elif 'quit' in query:
                break

            elif 'open gmail' in query:
                webbrowser.open("gmail.com")


            elif "system" in query:
                sys_info = obj.system_info()
                print(sys_info)
                speak(sys_info)

            if "tell me a joke" in query:
                joke = pyjokes.get_joke()

                print(joke)

                speak(joke)


            elif re.search('open', query):

                domain = query.split(' ')[-1]

                open_result = obj.website_opener(domain)

                speak(f'Alright sir !! Opening {domain}')

                print(open_result)

            elif 'kolkata' in query :

                weather_res = fetch_weather(query)
                print(weather_res)
                speak(weather_res)


            elif "buzzing" in query or "news" in query or "headlines" in query:
                news_res = obj.news()
                speak('Source: The Times Of India')
                speak('Todays Headlines are..')
                for index, articles in enumerate(news_res):
                    pprint.pprint(articles['title'])
                    speak(articles['title'])
                    if index == len(news_res) - 2:
                        break
                speak('These were the top headlines, Have a nice day Sir!!..')

            if "make a note" in query or "write this down" in query or "remember this" in query:
                speak("What would you like me to write down?")
                note_text = obj.mic_input()
                obj.take_note(note_text)
                speak("I've made a note of that")

            elif "where i am" in query or "current location" in query or "where am i" in query:
                try:
                    city, state, country = my_location()
                    print(city, state, country)
                    speak(
                        f"You are currently in {city} city which is in {state} state and country {country}")
                    loc(city)
                except Exception as e:
                    speak(
                        "Sorry sir, I coundn't fetch your current location. Please try again")

            elif re.search('launch', query):
                dict_app = {
                    'chrome': 'C:\\Program Files\\Google\\Chrome\\Application\\chrome'
                }
                app = query.split(' ', 1)[1]
                path = dict_app.get(app)

                if path is None:
                    speak('Application path not found')
                    print('Application path not found')



                else:
                    speak('Launching: ' + app + 'for you sir!')
                    obj.launch_any_app(path_of_app=path)

            elif 'youtube' in query:
                video = query.split(' ')[1]
                speak(f"Okay sir, playing {video} on youtube")
                pywhatkit.playonyt(video)

            elif 'activate'in query:
                speak("activated")
                how=takeCommand()
                max_result=1
                how_to= pywikihow.search_wikihow(how, max_result)
                assert len(how_to)==1
                how_to[0].print()
                speak(how_to[0].summary)

            elif "what is your name" in query:
                speak("my name is Artificicial Intelligence sir")

            elif "what to do" in query:
                speak("your wish sir")

            elif "what is my name" in query:
                speak("Your name is bishal saha sir")
            elif "who are you" in query:
                speak("I am AI an Artificial intelligence")

            elif "who is your friend" in query:
                speak("well I have a large number of friends like jaarvid,google assistant,alexa,siri ")

            elif 'what is your favourite game' in query:
                speak("cricket sir ")

            elif 'which is your favourite game' in query:
                speak("cricket sir")

            elif "what is your favourite food" in query:
                speak("pizza sir")

            elif "start" in query:
                pdf_reader()



startExecution = MainThread()
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def __del__(self):
        sys.stdout = sys.__stdout__

    # def run(self):
    #     self.TaskExection
    def startTask(self):
        self.ui.movie = QtGui.QMovie("Jarvis/utils/images/live_wallpaper.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("Jarvis/utils/images/initiating.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()

        timer = QTimer(self)

        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)


app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())


