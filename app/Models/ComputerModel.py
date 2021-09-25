import subprocess
import os

class ComputerModel():
    # открытие приложения из командной строки
    def openApp(self, app):
        pipe = subprocess.PIPE
        p = subprocess.Popen(app, shell=True, stdin=pipe, stdout=pipe, stderr=subprocess.STDOUT,)
    # выключение компьютера
    def Computeroff(self):
        os.system('shutdown -s')
    # перезагрузка компьютера
    def CompuerReboot(self):
        os.system('shutwodn /r /t 1')
    # погружение компьютера в сон
    def ComputerSleep(self):
        os.system('shutdown /h')