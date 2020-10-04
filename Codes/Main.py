from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from EM_Classes import *
import sys

from threading import Thread




app = QApplication(sys.argv)



window_login = LoginWindow()

app.exec_()