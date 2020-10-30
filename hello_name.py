# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 17:38:39 2020

@author: Ishita
"""
from playsound import playsound
from gtts import gTTS
import os
import shutil
import random
import speech_recognition as sr 
import pyttsx3 
from datetime import datetime, timedelta
from .web_cam_photo_capture_save import web_cam_capture_image

home = os.getcwd()
#print(home)

def hello_name_identified(name_of_person_identified):
    greetings = ["Hi", "Hello", "Namaste", "hi", "hello", "namaste", "Ok", "Good", "Nice","ok", "good", "nice"]
    # Initialize the recognizer  
    r = sr.Recognizer()  

    # Initialize the engine
    def speak_text(command): 
        engine = pyttsx3.init() 
        engine.say(command)  
        engine.runAndWait() 
    
    mytext = greetings[random.randint(0,5)] + " " + name_of_person_identified
    language = "en"

    myobj = gTTS(text=mytext, lang=language)
    name = "hello_name.mp3"
    myobj.save(name)
    playsound("hello_name.mp3")
    
    # os.makedirs(name.split(".")[0])
    # destination_folder = home + "\\" + name.split(".")[0]
    # shutil.move("C:\\Users\\Ishita\\Desktop\\Parity-InfoTech\\text_to_speech\\"+name, destination_folder)

    
    # Function to convert text to 
    # speech 
      
        
        
    # Loop infinitely for user to 
    # speak
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
                if MyText in greetings:
                    print("Verified. Presence Marked.") 
                else:
                    print("OOPS!Sorry...Kindly refresh.")
                print(MyText) 
                reply_counter += 1
                #SpeakText(MyText) 
        except sr.RequestError as e: 
            print("Could not request results; {0}".format(e)) 
        except sr.UnknownValueError: 
            print("unknown error occured")
        