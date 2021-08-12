# from PyQt5.uic import loadUi
# Importing Modules
from PyQt5 import QtWidgets as qtw
from PyQt5.QtCore import *
# Importing Libraries
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import cv2
import sys
from zoom_main import WindowMain
from Vertical_Win_Main import VerticalWindowMain
from read_video_app import Ui_Form
from win32api import GetSystemMetrics

from PyQt5.QtWidgets import *


# 23.14 of Screen 800,600 >>> 1920 x 1080 >>> 31.0
# 1366 x 768
class MainVideoWindow(Ui_Form, QWidget):
    def __init__(self,  *args, **kwargs):
        super(MainVideoWindow, self).__init__( *args, **kwargs)
        self.flag = 0
        screen_size = qApp.desktop().screenGeometry()
        self.screen_width, self.screen_height = screen_size.width(), screen_size.height()
        # Setting up the main window Ui
        self.ui = Ui_Form()
        self.setupUi(self)

        self.new_height = ((self.frameGeometry().height() * self.screen_height) / 1080)
        self.new_width = ((self.frameGeometry().width() * self.screen_width) / 1920)
        # self.setStyleSheet("background-color:grey;")
        # self.image_lbl.adjustSize()
        self.main_window_res()
        # self.center_main_window()
        self.setFocus()
        # self.showMaximized()
        # self.setFixedSize(800, 600)

        # Setting up the zoom window
        self.zoom_window = WindowMain()
        self.new_zoom_height = ((self.zoom_window.frameGeometry().height() * self.screen_height) / 1080)
        self.new_zoom_width = ((self.zoom_window.frameGeometry().width() * self.screen_width) / 1920)
        # Setting up The buttons Window
        self.ui_sec = VerticalWindowMain()
        # self.vertical_window_res()
        # Starting The video Thread to Capture Image
        # self.thread1 = ThreadClass(GetSystemMetrics(0) * .41, GetSystemMetrics(1) * .55)
        self.thread1 = ThreadClass(self.new_width, self.new_height - 20)
        self.thread2 = ThreadClass(self.new_zoom_width, self.new_zoom_height - 20)
        self.thread1.start()  # Signal will be emitted
        # Connect Signal to a Slot
        self.thread1.ImageUpdate.connect(self.image_update_slot)
        # self.image_lbl.setPixmap(QtGui.QPixmap("cat.jpg"))
        # self.start_btn.clicked.connect(self.thread1.start)
        # Opening the Vertical Window with the Main Window
        self.open_vertical_win()
        self.zoom_window_res()

    # Function to Set the Main window to the Center
    def center_main_window(self):
        # geometry of the main window
        qr = self.frameGeometry()
        # print(self.frameGeometry().width(),self.frameGeometry().height())
        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()
        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)
        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())

    def get_frame_width(self):
        return self.frameGeometry().width()

    def get_frame_height(self):
        return self.frameGeometry().height()

    def get_zoom_frame_width(self):
        # print(self.zoom_window.frameGeometry().width())
        return self.zoom_window.frameGeometry().width()

    def get_zoom_frame_height(self):
        return self.zoom_window.frameGeometry().height()

    # Getting Window Size
    def main_window_res(self):
        print(self.screen_width, self.screen_height)
        print(self.new_width, self.new_height)
        self.setGeometry((self.screen_width - self.new_width) // 2, (self.screen_height - self.new_height) // 2,
                         self.new_width, self.new_height)

    def zoom_window_res(self):
        print(self.screen_width, self.screen_height)
        print(self.new_zoom_width, self.new_zoom_height)
        self.zoom_window.setGeometry(self.screen_width - (self.new_zoom_width + 20),
                                     self.screen_height - (self.new_zoom_height + 20),
                                     self.new_zoom_width, self.new_zoom_height)

    def vertical_window_res(self):
        # print(self.screen_width,self.screen_height)
        self.new_vert_width = ((self.ui_sec.frameGeometry().width() * self.screen_width) / 1920)
        self.new_vert_height = ((self.ui_sec.frameGeometry().height() * self.screen_height) / 1920)
        # print(self.new_vert_width,self.new_vert_height)
        self.ui_sec.setGeometry(self.screen_width - self.new_width, self.screen_height - self.new_height
                                , self.new_vert_width, self.new_vert_height)

    # Minimizing the Main Window
    def hideEvent(self, event):
        self.flag = 1
        # event.ignore()
        print("Minimize event")
        # self.move(0, 0)
        self.close()
        self.ui_sec.move(self.screen_width - 170, self.screen_height - 850)
        self.open_zoom_win()
        # self.ui_sec.hide()

    def open_zoom_win(self):
        self.zoom_window.show()
        self.thread2.start()
        self.thread2.ImageUpdate.connect(self.zoom_img_update_slot)

    def open_vertical_win(self):
        self.ui_sec.show()

    # Defining Slot
    def image_update_slot(self, image):  # Takes the Image as an Input
        self.image_lbl.setPixmap(QPixmap.fromImage(image))

    def zoom_img_update_slot(self, image):
        self.zoom_window.img_lbl.setPixmap(QPixmap.fromImage(image))

    # Define the Cancel Function
    def cancel_thread(self):
        self.thread1.stop()

    def start_thread(self):
        self.thread1.start()

    # Closing Main window Function
    def closeEvent(self, event):
        if self.flag == 1:
            return
        print("event")
        reply = qtw.QMessageBox.question(self, 'Message', "Are you sure to quit?", qtw.QMessageBox.Yes,
                                         qtw.QMessageBox.No)

        if reply == qtw.QMessageBox.Yes:
            event.accept()
            sys.exit(qApp.exec_())
        else:
            event.ignore()


# Creating Class Thread
class ThreadClass(QThread):
    # Handles retrieving Image from Webcam and convert it to a format that PyQt can understand
    # Signal Image
    ImageUpdate = pyqtSignal(QImage)

    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.ThreadActive = True

    # Run function
    def run(self):

        capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        while self.ThreadActive:
            ret, frame = capture.read()
            if ret:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert the Frame to rgb image
                image = cv2.flip(image, 1)  # Flip image
                convert_to_qt_format = QImage(image.data, image.shape[1], image.shape[0],
                                              QImage.Format_RGB888)  # convert image to QT
                picture = convert_to_qt_format.scaled(self.width, self.height,
                                                      Qt.KeepAspectRatio)
                self.ImageUpdate.emit(picture)

    # Stop Function
    def stop(self):
        self.ThreadActive = False
        self.quit()


if __name__ == '__main__':
    qApp = QApplication(sys.argv)
    mainWindow = MainVideoWindow()
    mainWindow.show()
    sys.exit(qApp.exec_())
