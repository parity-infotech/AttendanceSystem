from playsound import playsound
import speech_recognition as sr 
import pyttsx3  
# import kivy 
# kivy.require("1.9.1")   
# from kivy.app import App 
# from kivy.uix.vkeyboard import VKeyboard
# from kivy.core.window import Window
# from kivy.uix.widget import Widget
# from kivy.base import runTouchApp
# from kivy.config import Config    
from datetime import datetime, timedelta    

#from auxillary_codes.virtual_keypad import VkeyboardApp

# class Test(VKeyboard): 
#     player = VKeyboard() 
# class VkeyboardApp(App): 
#     def build(self): 
#         return Test() 

# class MyKeyboardListener(Widget):
#     def __init__(self, **kwargs):
#         super(MyKeyboardListener, self).__init__(**kwargs)
#         self._keyboard = Window.request_keyboard(
#             self._keyboard_closed, self, 'text')
#         if self._keyboard.widget:
#             # If it exists, this widget is a VKeyboard object which you can use
#             # to change the keyboard layout.
#             pass
#         self._keyboard.bind(on_key_down=self._on_keyboard_down)

#     def _keyboard_closed(self):
#         print('My keyboard have been closed!')
#         self._keyboard.unbind(on_key_down=self._on_keyboard_down)
#         self._keyboard = None

#     def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
#         print('The key', keycode, 'have been pressed')
#         print(' - text is %r' % text)
#         print(' - modifiers are %r' % modifiers)

#         # Keycode is composed of an integer + a string
#         # If we hit escape, release the keyboard
#         if keycode[1] == 'escape':
#             keyboard.release()

#         # Return True to accept the key. Otherwise, it will be used by
#         # the system.
#         return True

def answers_to_questions():
    negation = ["no", "wrong", "incorrect", "galat", "not"]
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

    

def new_visitor():
    new_visitor_details = {}
    playsound("dear-visitor-name.mp3")
    visitor_name = answers_to_questions()
    new_visitor_details["visitor_name"] = visitor_name
    playsound("dear-visitor-organisation.mp3")
    visitor_organization = answers_to_questions()
    new_visitor_details["visitor_organization"] = visitor_organization
    playsound("dear-visitor-emp_ID.mp3")
    visitor_emp_id = answers_to_questions()
    new_visitor_details["visitor_emp_id"] = visitor_emp_id
    playsound("dear-visitor-phone.mp3")
    visitior_phone_num = answers_to_questions()
    new_visitor_details["visitor_phone_num"] = visitior_phone_num
    playsound("visitor-email_ID.mp3")
    #VkeyboardApp().run()
    #runTouchApp(MyKeyboardListener())
    visitor_email_id = input("Your email_ID please!")
    print(visitor_email_id)
    new_visitor_details["visitor_email_id"] = visitor_email_id
    print(new_visitor_details)
    return new_visitor_details