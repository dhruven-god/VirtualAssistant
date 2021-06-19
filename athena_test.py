# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.5 (tags/v3.8.5:580fbb0, Jul 20 2020, 15:57:54) [MSC v.1924 64 bit (AMD64)]
# Embedded file name: c:\Users\dhruven\Desktop\Publish\Virtual Assistant\Athena.py
# Compiled at: 2021-06-17 15:30:15
# Size of source mod 2**32: 3477 bytes
import speech_recognition as sr, pyttsx3, datetime, wikipedia, webbrowser, pywhatkit,sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer,QTime,QDate
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from athenaUi import Ui_MainWindow
import wolframalpha

try:

    app = wolframalpha.Client("T3R7U5-7J2H54P2Q2")

except Exception as e:
    print("Something is wrong")

chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

hour = int(datetime.datetime.now().hour)
min = int(datetime.datetime.now().minute + 2)

engine = pyttsx3.init('sapi5')
rate = engine.getProperty('rate')

engine.setProperty('rate', 180)

voices = engine.getProperty('voices')

engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def greeting():
    if hour >= 0 and hour < 12:
        speak('Hello Boss Good Morning')
    else:
        if hour >= 12 and hour < 16:
            speak('Good Afternoon Boss')
        else:
            speak('Good Evening Boss')

speak("Initializing System")


class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()

    def run(self):
        self.execute()


            

    def givecommand(self):
        r = sr.Recognizer()

        with sr.Microphone() as source:
            print("Yes boss")
            r.adjust_for_ambient_noise(source,duration= 1)
            audio = r.listen(source)

        try :
            print("Recognizing...")
            self.query = r.recognize_google(audio, language = 'en-in')
            print(f"user said: {self.query}\n")

        except Exception as e:
            print("Say that again please...")
            self.query = "None"

        return self.query

    def execute(self):

        greeting()
        while True:
            self.query = self.givecommand().lower()
            if "your name" in self.query:
                speak('My name is Athena')

            elif "who made you" in self.query:
                speak('I was made by Dhruven')

            elif 'what does it mean' in self.query:
                speak('I am named after a greek goddess of Wisdom and Knowledge')

            elif 'open youtube' in self.query:
                speak('Opening Youtube...')
                webbrowser.get(chrome_path).open('youtube.com')

            elif 'wikipedia' in self.query:
                speak('Searching Boss....')
                self.query = self.query.replace('wikipedia', ' ')
                results = wikipedia.summary(self.query, sentences=1)
                speak('So According to wikipedia')
                print(results)
                speak(results)

            elif 'open google' in self.query:
                speak('Opening google...')
                webbrowser.get(chrome_path).open("https://www.google.com/")
            
            elif "search" in self.query:
                speak("Searching.....Please wait")
                self.query = self.query.replace('search',' ')
                webbrowser.get(chrome_path).open(f"https://www.google.com/search?q={self.query}")

            elif 'open whatsapp' in self.query:
                speak('Opening whatsapp...')
                webbrowser.get(chrome_path).open('https://web.whatsapp.com/')

            elif 'open linkedin' in self.query:
                speak('Opening linkedin...')
                webbrowser.get(chrome_path).open('https://www.linkedin.com/feed/')

            elif 'send a message' in self.query:
                speak('What would you like to say?')
                mssg = self.query.givecommand()

                def sendMessage():
                    pywhatkit.sendwhatmsg('{Number}', mssg, hour, min)

                sendMessage()

            elif "Bye" or "Seeya" or "Shutdown" in self.query:
                speak("Shutting down the system")
                sys.exit()

execution = MainThread()

class Mywindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startgif)
        
    def startgif(self):
        self.ui.movie = QtGui.QMovie("circle.gif")
        self.ui.circle.setMovie(self.ui.movie)
        self.ui.movie.start()
        execution.start()


app = QApplication(sys.argv)
athena = Mywindow()
athena.show()
exit(app.exec_())