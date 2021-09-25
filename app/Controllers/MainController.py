import datetime
import pyttsx3
import app.Models.DataModel
import speech_recognition as sr
from PyQt5 import QtCore, QtWidgets
import os
from app.Views.MainView import MainView


engine = pyttsx3.init()


class MainController(QtWidgets.QMainWindow):
    # установка настроек и значений по умолчанию для всех элементов
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = MainView()
        self.answer = app.Models.DataModel.DataModel()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.center()

        self.ui.send_btn.clicked.connect(self.start_conversation)
        self.stop = False
        self.repeat_start = False

# разметка приложения по центру
    def center(self):
        frame_geometry = self.frameGeometry()
        center = QtWidgets.QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center)
        self.move(frame_geometry.topLeft())

# нажатие кнопки мыши
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

# перемещение окна приложения, т.к. стандартные элементы убраны
    def mouseMoveEvent(self, event):
        try:
            delta = QtCore.QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
        except AttributeError:
            pass

    # воспроизведение речи ассистента
    def speak(self, text):
        engine.say(text)
        engine.runAndWait()
        engine.stop()

    # распознавание речи пользователя
    def recordAudio(self, phrase='Говорите: '):
        recognize = sr.Recognizer()
        with sr.Microphone() as source:
            recognize.adjust_for_ambient_noise(source)
            self.ui.chat_list.clear()
            self.send_message(phrase, user=False)
            self.speak(phrase)
            audio = recognize.listen(source)
        try:
            data = recognize.recognize_google(audio, language='ru-RU').lower()
            self.ui.chat_list.clear()
            self.send_message(data)
        except sr.UnknownValueError:
            self.ui.chat_list.clear()
            error = "Извините,но я вас не понимаю"
            self.send_message(error, user=False)
            self.speak(error)
            return None
        except sr.RequestError as e:
            self.ui.chat_list.clear()
            error = "Не удалось запросить результаты у службы распознавания речи Google"
            self.speak(error)
            self.send_message(error, user=False)
            return None
        return data


# отправка сообщений в чат
    def send_message(self, text, user=True):
        item = QtWidgets.QListWidgetItem()
        if user == True:
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
            item.setText('Вы' + ': ' + text)
        else:
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
            item.setText('Алена' + ': ' + text)
        self.ui.chat_list.addItem(item)

    # выявление времени суток пользователя
    def getTimeOfDay(self):
        getTime = int(datetime.datetime.now().hour)
        if getTime >= 0 and getTime < 6:
            text = 'Доброе ночи'
            self.send_message(text, user=False)
            self.speak(text)
        elif getTime >= 6 and getTime < 12:
            text = 'Доброе утро'
            self.send_message(text, user=False)
            self.speak(text)
        elif getTime >= 12 and getTime < 18:
            text = 'Добрый день'
            self.send_message(text, user=False)
            self.speak(text)
        elif getTime >= 18 and getTime != 0:
            text = 'Добрый вечер!'
            self.send_message(text, user=False)
            self.speak(text)


    # начало диалога
    def start_conversation(self):
        self.ui.send_btn.hide()
        self.ui.chat_list.show()
        if self.repeat_start == False:
            start_text = ' Могу ли я вам чем-нибудь помочь?'
            self.getTimeOfDay()
            self.ui.chat_list.clear()
            self.send_message(start_text, user=False)
            self.speak(start_text)

        self.repeat_start = True
        self.stop = False

        while self.stop == False:
            self.ui.chat_list.clear()
            statement = self.recordAudio()
            if statement == None: continue
            answer, action = self.answer.get_answer(statement)
            if type(action) is str:
                self.ui.chat_list.clear()
                self.send_message(action, user=False)
                self.speak(action)
            self.ui.chat_list.clear()
            self.send_message(answer, user=False)
            self.speak(answer)

            if action == True:
                self.stop = True
                self.ui.chat_list.hide()
                self.ui.send_btn.show()
                break

            if engine._inLoop:
                engine.endLoop()