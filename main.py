import sys
from PyQt5 import QtWidgets
from app.Controllers.MainController import MainController

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    base_class = MainController()
    base_class.show()
    sys.exit(app.exec_())
