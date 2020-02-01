import aiml
import os
import time
import argparse
import pyttsx3
import smtplib
import webbrowser as wb
import wikipedia as wk
import datetime as dt

dictionary = {'Google':'google', "Facebook":"facebook", "youtube":"youtube", "Jira":"jira", "Confluence":"confluence", "instagram":"instagram", "hotstar":"hotstar", "gaana":"gaana"}

mode = "text"
voice = "pyttsx3"
terminate = ['nothing bye', 'nothing buy', 'nothing shutdown', 'nothing exit', 'quit', 'gotosleep', 'nothing goodbye', 'goodbye']


def get_arguments():
    parser = argparse.ArgumentParser()
    optional = parser.add_argument_group('params')
    optional.add_argument('-v', '--voice', action='store_true', required=False,
                          help='Enable voice mode')
    optional.add_argument('-g', '--gtts', action='store_true', required=False,
                          help='Enable Google Text To Speech engine')
    arguments = parser.parse_args()
    return arguments


def gtts_speak(jarvis_speech):
    tts = gTTS(text=jarvis_speech, lang='en')
    tts.save('jarvis_speech.mp3')
    mixer.init()
    mixer.music.load('jarvis_speech.mp3')
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(1)


def offline_speak(jarvis_speech):
    engine = pyttsx3.init()
    engine.say(jarvis_speech)
    engine.runAndWait()


def speak(jarvis_speech):
    if voice == "gTTS":
        gtts_speak(jarvis_speech)
    else:
        offline_speak(jarvis_speech)


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Talk to I.P.M ")
        r.pause_threshold = 0.8
        audio = r.listen(source)
    try:
        print (r.recognize_google(audio))
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        speak(
            "I couldn't understand what you said! Would you like to repeat?")
        return(listen())
    except sr.RequestError as e:
        print("Could not request results from " +
              "Google Speech Recognition service; {0}".format(e))

def wishme():
    hour = int(dt.datetime.now().hour)
    if (hour >= 0 and hour < 12):
        speak("Good Morning Sir, Have a Nice day")
    elif (hour >= 12 and hour < 18):
        speak("Good Afternoon Sir, have a nice noon")
    else:
        speak("Good Evening Sir, Have a nice evening")
    speak("hello sir how may i help you")

def sendemail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("dzkakadiya3@gmail.com", "Dhruv@81282")
    server.sendmail("dzkakadiya3@gmail.com", to, content)
    server.close()
    
if __name__ == '__main__':
    wishme()
    try:
        import speech_recognition as sr
        mode = "voice"
    except ImportError:
        print("\nInstall SpeechRecognition to use this feature." +
              "\nStarting text mode\n")
   
    kernel = aiml.Kernel()

    if os.path.isfile("bot_brain.brn"):
        kernel.bootstrap(brainFile="bot_brain.brn")
    else:
        kernel.bootstrap(learnFiles="std-startup.xml", commands="load aiml b")
   

    # kernel now ready for use
    while True:
        if mode == "voice":
            response = listen()
        else:
            response = input("Talk to I.P.M  :- ")
        if response.lower().replace(" ", "") in terminate:
            speak("okay nice to see you sir, goodbye")
            break
            
        elif "send email to" in response :
            try:
                speak("what would you like to mail?")
                content = listen()
                to = "nevilparmar24@gmail.com"
                sendemail(to, content)
                speak("email has been sent successfully")
            except Exception as e:
                print(e)
                speak("sorry try again")
        elif "search about" in response:
            try:
                lst = response.split(" ")
                b = False
                string = ""
                for i in lst:
                    if b == True:
                        string = string + "+" + i
                    if (i == "about"): 
                        b = True
                    
                if string:
                    print(string)
                    wb.open("google.com/search?q=" + string)
                else:
                    speak("what you mean to say")
            except Exception as e:
                print(e)
                speak("i cant find it")
        elif "open" in response:
            try:
                for key,value in dictionary.items():
                    if key.upper() in response.upper():
                        br = value + ".com"
                        wb.open(br)
                        speak("opened")
            except Exception as e:
                print(e)
                speak("sorry")
        elif "time" in response:
            strtime = dt.datetime.now().strftime("%H:%M:%S")
            print(strtime)
            speak(f"Sir, the time is {strtime}")
        elif ("about"  in response):
            try:
                speak("Sure sir,Searching.......")
                response = response.replace("wikipedia", "")
                response = response.replace("about", "")
                response = response.replace("tell me ","")
                print(response)
                results = wk.summary(response, sentences = 5)
                
                speak("According to your search")
                print(results)
                speak(results)
            except Exception as e:
                print("information not available")
                speak("information not available")
        else:
            jarvis_speech = kernel.respond(response)
            print ("ALEXA " + jarvis_speech)
            speak(jarvis_speech)