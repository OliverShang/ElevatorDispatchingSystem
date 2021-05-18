from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *

from ui import *


class UI(QtWidgets.QMainWindow, UI_MainWindow):
    def __init__(self):
        super(UI, self).__init__()
        self.setupUI(self)
        self.setWindowIcon(QtGui.QIcon(os.curdir + "favicon.ico"))
        self.setWindowTitle("OS Coursework--Elevator Dispatching Sysrem")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = UI()
    main_window.show()
    sys.exit(app.exec())
