from playsound import playsound
from gtts import gTTS
import os
import shutil
import random
import speech_recognition as sr 
import pyttsx3 
from datetime import datetime, timedelta

home = os.getcwd()
#print(home)

def details_correction():
    r = sr.Recognizer()
    replies_positive = ["yes", "ya", "yeah", "yup", "Yes", "Ya", "Yeah", "Yup", "Haan", "haan"]
    ans = True
    reply_counter = 0 
    while(timedelta(seconds=5) and reply_counter<1):     
        
        # Exception handling to handle 
        # exceptions at the runtime 
        try: 
            
            # use the microphone as source for input. 
            with sr.Microphone() as source2: 
                
                # wait for a second to let the recognizer 
                # adjust the energy threshold based on 
                # the surrounding noise level  
                r.adjust_for_ambient_noise(source2, duration=0.2) 
                
                #listens for the user's input  
                audio2 = r.listen(source2) 
                
                # Using ggogle to recognize audio 
                MyText = r.recognize_google(audio2) 
                MyText = MyText.lower() 
                if MyText in replies_positive:
                    print("Details are verified to be correct.")
                else:
                    print("OOPS!Sorry...kindly update your details...")
                    ans = False
                print(MyText) 
                reply_counter += 1
                return ans
                #SpeakText(MyText) 
        except sr.RequestError as e: 
            print("Could not request results; {0}".format(e)) 
        except sr.UnknownValueError: 
            print("unknown error occured")
