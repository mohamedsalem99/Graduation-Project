from PyQt5.QtCore import QEvent, Qt
import sys
from PyQt5 import QtWidgets as qtw
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore as qtc
from win32api import GetSystemMetrics
import PyQt5
from Vertical_Win import Ui_Vertical_Win
from PyQt5 import QtCore
import os


class VerticalWindowMain(qtw.QWidget, Ui_Vertical_Win):
    def __init__(self, *args, **kwargs):
        super(VerticalWindowMain, self).__init__(*args, **kwargs)
        self.ui = Ui_Vertical_Win()
        self.setupUi(self)
        self.setFixedSize(117, 379)
        self.width = GetSystemMetrics(0)
        self.height = GetSystemMetrics(1)
        self.move(self.width - 500, self.height - 800)
        self.setWindowFlag(PyQt5.QtCore.Qt.WindowStaysOnTopHint)
        self.setMaximumSize(QtCore.QSize(117, 379))
        self.show_keyboard_btn.clicked.connect(self.callback)

    def callback(event):
        os.system('wmic process where name="TabTip.exe" delete')
        os.system("C:\\PROGRA~1\\COMMON~1\\MICROS~1\\ink\\tabtip.exe")


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    widget = VerticalWindowMain()
    widget.show()
    sys.exit(app.exec_())
