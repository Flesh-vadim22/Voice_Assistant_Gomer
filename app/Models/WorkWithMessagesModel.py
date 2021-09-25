import pyttsx3

engine = pyttsx3.init()

class WorkWithMessageModel:
    def speak_object(self, text):
        engine.say(text)
        engine.runAndWait()
        engine.stop()