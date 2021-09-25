from PyQt5 import QtCore, QtGui, QtWidgets


class MainView(object):
    # разметка интерфейса
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(850, 750)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.main_frame = QtWidgets.QFrame(self.centralwidget)
        self.main_frame.setGeometry(QtCore.QRect(0, 0, 850, 450))
        self.main_frame.setStyleSheet("QFrame{\n"
                                      "    border-radius: 7px;\n"
                                      "    background-color: #1B1D23;\n"
                                      "}")
        self.main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.main_frame.setObjectName("main_frame")
        self.menu_frame = QtWidgets.QFrame(self.main_frame)
        self.menu_frame.setGeometry(QtCore.QRect(0, 0, 850, 40))
        self.menu_frame.setStyleSheet("QFrame{\n"
                                      "    border-bottom-left-radius: 0px;\n"
                                      "    border-bottom-right-radius: 0px;\n"
                                      "    background-color: #2C313C;\n"
                                      "}")
        self.menu_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.menu_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.menu_frame.setObjectName("menu_frame")
        self.chat_list = QtWidgets.QListWidget(self.main_frame)
        self.chat_list.setGeometry(QtCore.QRect(30, 150, 801, 161))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.chat_list.setFont(font)
        self.chat_list.setStyleSheet("color: white;\n"
                                     "border-radius: 20px;\n"
                                     "background-color: #2C313C;\n"
                                     "")
        self.chat_list.setObjectName("chat_list")
        self.chat_list.hide()
        self.send_btn = QtWidgets.QPushButton(self.main_frame)
        self.send_btn.setGeometry(QtCore.QRect(70, 150, 711, 171))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(64)
        font.setBold(False)
        font.setWeight(50)
        self.send_btn.setFont(font)
        self.send_btn.setStyleSheet("QPushButton{\n"
                                    "    color: white;\n"
                                    "    border-radius: 17px;\n"
                                    "    background-color: #595F76;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:hover{\n"
                                    "    background-color: #50566E;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:pressed{\n"
                                    "    background-color: #434965;\n"
                                    "}")
        self.send_btn.setObjectName("send_btn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 850, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Voice_Assistant"))
        self.send_btn.setText(_translate("MainWindow", "Начать разговор"))
