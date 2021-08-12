# Importing Modules
from PyQt5 import QtWidgets as qtw
# from PyQt5.QtWidgets import qApp
from PyQt5 import QtCore
from PyQt5.QtCore import *
# from qtpy import uic
import PyQt5
import sys, cv2
from Fix_win import Ui_zoom_window
from Vertical_Win_Main import VerticalWindowMain


class WindowMain(Ui_zoom_window, qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super(WindowMain, self).__init__(*args, **kwargs)
        self.flag = 0
        self.ui = Ui_zoom_window()
        self.setupUi(self)
        self.ver = VerticalWindowMain()
        self.setWindowFlag(PyQt5.QtCore.Qt.WindowStaysOnTopHint)
        self.setFocus()
        self.resize(400, 300)

    def open_Main_Vedio_win(self):
        from testMainGUI import MainVideoWindow
        self.gui_main = MainVideoWindow()
        # self.ver.show()
        self.gui_main.thread1.start()
        self.gui_main.show()

    def window_size_resize(self):
        screen_size = app.desktop().screenGeometry()
        width, height = screen_size.width(), screen_size.height()
        print(width, height)
        new_width = ((self.frameGeometry().width() * width) / 1920)
        new_height = ((self.frameGeometry().height() * height) / 1080)
        print(new_width, new_height)
        self.setGeometry(width - new_width, height - new_height, new_width, new_height)

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowMaximized:
                print("WindowMaximized")
                self.hide()
                self.open_Main_Vedio_win()
                self.gui_main.ui_sec.close()
                self.gui_main.thread2.stop()
                # self.ver.hide()

    def closeEvent(self, event):
        if self.flag == 1:
            return
        print("event")
        reply = qtw.QMessageBox.question(self, 'Message', "Are you sure to quit?", qtw.QMessageBox.Yes,
                                         qtw.QMessageBox.No)
        if reply == qtw.QMessageBox.Yes:
            event.accept()
            sys.exit(app.exec_())
        else:
            event.ignore()

    def hideEvent(self, event):
        self.flag = 0
        # self.ver.close()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    widget = WindowMain()
    widget.show()
    sys.exit(app.exec_())
