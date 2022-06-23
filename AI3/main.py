import datetime
import cv2
import PyPDF2
import cv2.cv2
import pyautogui
import pywikihow
from PyPDF2.generic import TextStringObject
from PyPDF2.pdf import ContentStream
from PyPDF2.utils import u_, b_
from google.auth.transport import requests
from prompt_toolkit.keys import Keys
from selenium.webdriver.chrome import webdriver
import sys
from Jarvis import JarvisAssistant
import speech_recognition as sr
import pyttsx3
import wikipedia
import whatsapp
import pyjokes
import re
import pprint
import pywhatkit
import os
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer,QTime,QDate,Qt
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import controller as cnt

from gui import Ui_MainWindow
from googletrans import Translator
from gtts import gTTS
from playsound import playsound

import smtplib
import webbrowser as web
import time
import keyword





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

def extractText(self):
        """
        Locate all text drawing commands, in the order they are provided in the
        content stream, and extract the text.  This works well for some PDF
        files, but poorly for others, depending on the generator used.  This will
        be refined in the future.  Do not rely on the order of text coming out of
        this function, as it will change if this function is made more
        sophisticated.

        :return: a unicode string object.
        """
        text = u_("")
        content = self["/Contents"].getObject()
        if not isinstance(content, ContentStream):
            content = ContentStream(content, self.pdf)
        # Note: we check all strings are TextStringObjects.  ByteStringObjects
        # are strings where the byte->string encoding was unknown, so adding
        # them to the text here would be gibberish.
        for operands, operator in content.operations:
            if operator == b_("Tj"):
                _text = operands[0]
                if isinstance(_text, TextStringObject):
                    text += _text
            elif operator == b_("T*"):
                text += "\n"
            elif operator == b_("'"):
                text += "\n"
                _text = operands[0]
                if isinstance(_text, TextStringObject):
                    text += operands[0]
            elif operator == b_('"'):
                _text = operands[2]
                if isinstance(_text, TextStringObject):
                    text += "\n"
                    text += _text
            elif operator == b_("TJ"):
                for i in operands[0]:
                    if isinstance(i, TextStringObject):
                        text += i
                text += "\n"
        return text

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
   # speak("Face verification start")
   # speak("scanning")
   # speak("scanning")
   # speak("scanning")

   # speak("Face verification successful")

    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour <=12:
        speak("Good Morning! s")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening! ")
    music_dir = 'D:\Musics'
    songs = os.listdir(music_dir)
    print(songs)
    os.startfile(os.path.join(music_dir, songs[0]))
    speak("How can I help you sir")




def pdf_reader():
    book=open('abcd.pdf','rb')
    pdfReader=PyPDF2.PdfFileReader(book)
    pages=pdfReader.getNumPages()
    speak(f"Total number of page {pages}")
    speak("sir please enter the page number i have to read")
    pg=int(input("please enter the page number: "))
    page=pdfReader.getPage(pg)
    text=page.extractText()
    print("reach1")
    print(text)
    speak(text)
    print("reach2")
    lang=takeCommand()



class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()




def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening......")
        r.pause_threshold=1
        audio=r.listen(source,0,1.5)

    try:
        print("Recognizing.....")
        query=r.recognize_google(audio,language='en-in')
        print("user said: ",query)
    except Exception as e:

            #speak('i dont know that ')
            #speak("can you please repeat sir")

            print(e)
            print("say that again please")
            return "None"
    return query


def takeCommand2():
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

    server.login('bishal.saha04052002@gmail.com', '04052002IwfZ129')

    server.sendmail('bishal.saha04052002@gmail.com',to,content)
    server.close()

def sleep(self):
    while True:
        a=takeCommand().lower()
        if "wake up" in a:
            self.TaskExecution()
class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        #self.TaskExecution()
        speak("system is activated")
        speak("I am online")

        while True:
            #a = takeCommand2()
            #if "wake up" in a or "hello" in a or "are you there" in a:

             self.TaskExecution()

           # elif "goodbye" in a:
              #  sys.exit()






    def TaskExecution(self):

        #speak("Enter the voice password")
        #while True:
         #   speak("Enter the voice password")
         #   a=takeCommand2().lower()
         #   if "username" in a:
          #      speak("Password verified successfuly")
          #      break




        while True:
            query = takeCommand().lower()

            # logic for executing tasks based on query
            if 'wikipedia' in query:
                speak('Searching Wikipedia....')
                try:
                    query = query.replace("wikipedia","")
                    results = wikipedia.summary(query, sentences=2)
                    speak("According to wikipedia")
                    print(results)
                    speak(results)
                except:
                    speak("sorry sir there is no information about that")

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

            elif 'send email' in query:
                try:
                    speak("what should I say")
                    content = takeCommand()
                    to = "hanumansaha.1975@gmail.com"
                    sendEmail(to, content)
                    speak("Email has been send")
                except Exception as e:
                    print(e)
                    speak("Sorry bhai")

            elif 'quit' in query:
                sys.exit()

            elif 'open gmail' in query:
                webbrowser.open("gmail.com")




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

            elif "start reading" in query:
                pdf_reader()





            elif 'check whatsapp message' in query:
                speak('opening whatsapp sir')
                open_chat = "https://web.whatsapp.com/"
                web.open(open_chat)

            elif 'enter into whatsapp message' in query:
                speak('sure sir')
                speak('enter phone number sir')
                a=int(input("Enter number:-"))
                open_chat = "https://web.whatsapp.com/send?phone=+91 "+str(a)
                web.open(open_chat)



            elif 'send whatsapp message' in query:
                speak('sure sir')
                speak('enter phone number sir')
                a=int(input("Enter number:-"))
                speak('what is the message sir')
                b=takeCommand().lower()
                open_chat = "https://web.whatsapp.com/send?phone=+91 7585848186 &text="+str(b)
                web.open(open_chat)




            elif 'google search' in query:
                speak('sure sir')
                speak('what do you want to search')
                a=takeCommand()
                open_chat = "https://www.google.com/search?q="+str(a)+"&rlz=1C1CHNY_enIN965IN965&sxsrf=AOaemvLfJcDGZDCd1f9UfI74dANMgJVTBQ%3A1636364786467&ei=8vGIYdDMG7yf4-EPo520oAs&oq="+str(a)+"&gs_lcp=Cgdnd3Mtd2l6EAMyBAgjECcyBQgAEJECMgUIABCABDIFCAAQgAQyBQgAEJECMgUIABCRAjIFCAAQgAQyBQgAEIAEMgUIABCRAjIFCAAQgAQ6BwgjELADECc6BwgAEEcQsAM6CwgAEIAEELEDEIMBOhEILhCABBCxAxCDARDHARCjAjoLCC4QgAQQsQMQgwE6CAgAEIAEELEDOgUILhCABDoICC4QgAQQsQM6CAgAELEDEJECSgQIQRgAUMYIWMwmYMMsaAJwAngAgAHyAYgByRSSAQYwLjEwLjSYAQCgAQHIAQnAAQE&sclient=gws-wiz&ved=0ahUKEwjQjcfuvYj0AhW8zzgGHaMODbQQ4dUDCA8&uact=5"
                speak('opening')
                speak(a)
                web.open(open_chat)

            elif 'official website' in query:
                speak('sure sir')
                open_chat = "https://vtop.vit.ac.in/vtop/initialProcess"
                speak('opening')
                web.open(open_chat)




            elif 'online class' in query:
                speak('sure sir')
                open_chat = "https: // teams.microsoft.com / _?culture = en - in & country = IN & lm = deeplink & lmsrc = homePageWeb & cmpid = WebSignIn  # /school/teams-grid/General?ctx=teamsGrid"
                speak('opening')
                web.open(open_chat)

            elif 'you can sleep now' in query or 'sleep now' in query:
                speak("okay sir,i am going to sleep you can call me anytime")
                break

            elif 'volume up' in query:
                pyautogui.press("volumeup")

            elif 'volume down' in query:
                pyautogui.press("volumedown")

            elif 'volume mute' in query:
                pyautogui.press("volumemute")

            elif "open camera"in query:
                cap=cv2.cv2.VideoCapture(0)
                while True:
                    success,img=cap.read()
                    cv2.imshow("webcam",img)
                    k=cv2.waitKey(1)
                    if k==27:
                        break
                cap.release()
                cv2.destroyAllWindows()

            elif "take screenshot" in query or "take a screenshot" in query:
                speak("sir,please tell me the name of screenshot file")
                name=takeCommand().lower()
                speak("sir please hold a moment for a second,i am taking screenshot")
                time.sleep(3)
                img=pyautogui.screenshot()
                img.save(f"{name}.png")
                speak("done sir")

            elif 'remember that' in query:
                remembermsg=query
                remember=open('data.txt','w')
                remember.write(remembermsg)
                speak('okay sir')
                remember.close()

            elif 'what do you remember' in query:
                remember=open('data.txt','r')
                speak("you tell me to "+remember.read())

            elif 'light on' in query:
                print("Light On.............")
                speak("light on")
                cnt.led(1)

            elif 'light off' in query:
                print("Light off.............")
                speak("light off")
                cnt.led(0)


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

        self.ui.movie = QtGui.QMovie("Jarvis/utils/images/initiating.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("jarvis.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("Jarvis/utils/images/loading.gif")
        self.ui.label_3.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("Jarvis/utils/images/loading_1.gif")
        self.ui.label_4.setMovie(self.ui.movie)
        self.ui.movie.start()

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_time)
        self.ui.textBrowser_2.setText(label_date)


app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())


