from playsound import playsound
import speech_recognition as sr 
import pyttsx3  
from datetime import datetime, timedelta    

def answers_to_questions():
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
    
    while(timedelta(seconds=5)):     
        
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
    
                print("Did you say "+MyText) 
                SpeakText(MyText)
                return MyText 
                
        except sr.RequestError as e: 
            print("Could not request results; {0}".format(e)) 
            
        except sr.UnknownValueError: 
            print("unknown error occured")

    

def meeting_request_replies():
    meeting_request = {}
    playsound("dear-visitor-meeting-person.mp3")
    visitor_meeting_person = answers_to_questions()
    meeting_request["visitor_meeting_person"] = visitor_meeting_person
    playsound("dear-visitor-meeting-purpose.mp3")
    visitor_meeting_purpose = answers_to_questions()
    meeting_request["visitor_meeting_purpose"] = visitor_meeting_purpose
    playsound("dear-visitor-meeting-time.mp3")
    visitor_meeting_time = answers_to_questions()
    meeting_request["visitor_meeting_time"] = visitor_meeting_time
    print(meeting_request)
    return meeting_request