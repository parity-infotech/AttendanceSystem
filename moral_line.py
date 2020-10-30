import speech_recognition as sr 
import pyttsx3  
from gtts import gTTS
from playsound import playsound
import sounddevice as sd
from scipy.io.wavfile import write
from datetime import datetime, timedelta 
import os
import shutil

def check_and_record_moral_line(moral_line):
    time = str(datetime.now().time()).replace(":", "_").split("."[0])[0]
    print(time)
    # Initialize the recognizer  
    r = sr.Recognizer()  
    
    # Function to convert text to 
    # speech 
    def SpeakText(command): 
        
        # Initialize the engine 
        engine = pyttsx3.init() 
        engine.say(command)  
        engine.runAndWait() 
        
        
    # Loop infinitely for user to 
    # speak 
    
    while(timedelta(seconds=2)):     
        
        # Exception handling to handle 
        # exceptions at the runtime 
        try:
            fs = 44100  # Sample rate
            seconds = 5  # Duration of recording
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.2)
                audio2 = r.listen(source)
                myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
                print("Say it!")
                sd.wait()  # Wait until recording is finished listens for the user's input 
                #write('output.wav', fs, myrecording) 
                MyText = r.recognize_google(audio2) 
                mytext = MyText.lower() 
                print("mytext", mytext)
                moral_line = moral_line.lower().split(".")[0]
                print("moral_line", moral_line)
                if moral_line == mytext:
                    language = "en"
                    myobj = gTTS(text=mytext, lang=language)
                    SpeakText("Your Employee_ID please!")
                    while(timedelta(seconds=2) and 1):
                        try:
                            with sr.Microphone() as source2:
                                r.adjust_for_ambient_noise(source2, duration=0.2)
                                audio3 = r.listen(source2)
                                emp_id_num = str(r.recognize_google(audio3))
                                print(emp_id_num)
                                name = "PI00" + str(emp_id_num) + "__" + time + ".mp3"
                                myobj.save(name)
                                file_name = "PI00" + str(emp_id_num) + "__" + time + ".wav"
                                write(file_name, fs, myrecording)  # Save as WAV file
                                SpeakText("Good luck for the day!")
                                return file_name
                        except sr.RequestError as e:
                            print("Could not request results; {0}".format(e))
                        except sr.UnknownValueError:
                            print("unknown error occurred")
                else:
                    print("Moral Line not recorded.")
        except sr.RequestError as e: 
            print("Could not request results; {0}".format(e)) 
                
        except sr.UnknownValueError: 
            print("unknown error occured")

        # except sr.TimeoutError:
        #     print("Time out error occurred")     
        # try: 
        #     # use the microphone as source for input. 
        #     with sr.Microphone() as source2: 
                
        #         # wait for a second to let the recognizer 
        #         # adjust the energy threshold based on 
        #         # the surrounding noise level  
        #         r.adjust_for_ambient_noise(source2, duration=0.2) 
        #         print("Once more please!...")
        #         audio2 = r.listen(source2) 
        #         # Using google to recognize audio 
        #         MyText = r.recognize_google(audio2) 
        #         mytext = MyText.lower() 
        #         moral_line = moral_line.lower().split(".")[0]
        #         if moral_line == mytext:
        #             language = "en"
        #             myobj = gTTS(text=mytext, lang=language)
        #             SpeakText("Your Employee_ID please!")
        #             while(timedelta(seconds=10) and 1):
        #                 try:
        #                     with sr.Microphone() as source2:
        #                         r.adjust_for_ambient_noise(source2, duration=0.2)
        #                         audio3 = r.listen(source2)
        #                         emp_id_num = str(r.recognize_google(audio3))
        #                         print(emp_id_num)
        #                         name = "PI00" + str(emp_id_num) + "__" + time + ".mp3"
        #                         myobj.save(name)
        #                         file_name = "PI00" + str(emp_id_num) + "__" + time + ".wav"
        #                         write(file_name, fs, myrecording)  # Save as WAV file
        #                         SpeakText("Good luck for the day!")
        #                         return file_name
                        