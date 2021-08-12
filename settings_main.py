from PyQt5 import QtCore
from PyQt5 import QtWidgets as qtw
from PyQt5.QtCore import *
# Importing Libraries
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import sys
from win32api import GetSystemMetrics
from PyQt5.QtWidgets import *

import testMainGUI
from Setting_Win import Ui_MainWindow
from math import hypot
from threading import Thread
import numpy as np
import playsound
from time import sleep
from scipy.spatial import distance as dist
import os


class SettingWindows(QtWidgets.QMainWindow, Ui_MainWindow):
    window_closed = pyqtSignal()
    applied = pyqtSignal(str, str, str, str)
    scroll_slider = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super(SettingWindows, self).__init__(*args, **kwargs)
        self.flag_test = 1
        self.ui = Ui_MainWindow()
        self.setupUi(self)
        self.groupBox_11.setAlignment(QtCore.Qt.AlignCenter)
        self.a1 = "left_eye"
        self.a2 = "right_eye"
        self.a3 = "smile"
        self.a4 = "off"

        # print(self.l_smile_rb.text())

        self.l_leftEye_rb.setChecked(True)
        self.r_rightEye_rb.setChecked(True)
        self.sm_smile_rb.setChecked(True)
        self.off_alarm_rb.setChecked(True)

        self.comboBox.currentIndexChanged.connect(self.change_func)

        self.trans = QtCore.QTranslator(self)
        options = ([('English', ''), ('العربية', 'eng-ar')])

        for i, (text, lang) in enumerate(options):
            self.comboBox.addItem(text)
            self.comboBox.setItemData(i, lang)
        self.retranslateUi(self)

        # Left Click Actions
        self.l_leftEye_rb.clicked.connect(lambda: self.get_l_click_result(self.l_leftEye_rb))
        self.l_rightEye_rb.clicked.connect(lambda: self.get_l_click_result(self.l_rightEye_rb))
        self.l_smile_rb.clicked.connect(lambda: self.get_l_click_result(self.l_smile_rb))
        self.l_eyeBrows_rb.clicked.connect(lambda: self.get_l_click_result(self.l_eyeBrows_rb))

        # Right Click Actions
        self.r_leftEye_rb.toggled.connect(lambda: self.onClicked(self.r_leftEye_rb, "Right Click"))
        self.r_rightEye_rb.toggled.connect(lambda: self.onClicked(self.r_rightEye_rb, "Right Click"))
        self.r_smile_rb.toggled.connect(lambda: self.onClicked(self.r_smile_rb, "Right Click"))
        self.r_eyeBrows_rb.toggled.connect(lambda: self.onClicked(self.r_eyeBrows_rb, "Right Click"))

        # Scroll Mode Actions
        self.sm_smile_rb.toggled.connect(lambda: self.onClicked(self.sm_smile_rb, "Scroll Mode"))
        self.sm_blink_rb.toggled.connect(lambda: self.onClicked(self.sm_blink_rb, "Scroll Mode"))
        self.sm_eyeBrows_rb.toggled.connect(lambda: self.onClicked(self.sm_eyeBrows_rb, "Scroll Mode"))
        self.on_alarm_rb.toggled.connect(lambda: self.onClicked(self.on_alarm_rb, "Alarm mode"))
        self.off_alarm_rb.toggled.connect(lambda: self.onClicked(self.off_alarm_rb, "Alarm mode"))

        self.apply_btn.clicked.connect(lambda: self.onApply())
        self.scroll_speed_slider_2.valueChanged.connect(self.spin_speed_2.setValue)
        self.mo_speed_slider.valueChanged.connect(self.spin_speed.setValue)
        # self.a1 = self.choose_left_click(2)
        """
        self.new = self.get_l_click_result(self.l_leftEye_rb)
        print("New = ",self.new)
        self.a1 = self.choose_left_click(self.new)
        print("A1 Value = ",self.a1)
        self.a2 = self.choose_right_click(3)
        self.a3 = self.choose_scroll_active(2)
        self.a4 = "off"
        """
        self.a1 = "left_eye"
        #self.aS = {2: 'left_eye'}
        #self.aS = self.aS.update(dict([self.get_l_click_result(self.l_rightEye_rb)]))
        #print(self.aS)
        from testMainGUI import ThreadClass
        ThreadClass.a1 = self.a1
        ThreadClass.a2 = self.a2
        ThreadClass.a3 = self.a3
        # self.var = self.get_l_click_result(self.l_leftEye_rb)
        # print("New = ", self.var)
        # self.spin_speed_2.valueChanged.connect(self.scroll_speed_slider_2.value)
        # self.l_click_result = self.get_a1_result()

    def get_l_click_result(self, rb):
        if rb.text() == "Left eye":
            if rb.isChecked():
                self.new = 2
        elif rb.text() == "Right eye":
            if rb.isChecked():
                self.new = 1
        elif rb.text() == "Smile":
            if rb.isChecked():
                self.new = 3
        elif rb.text() == "Eye Brows":
            if rb.isChecked():
                self.new = 4
        self.new_a = self.choose_left_click(self.new)
        print("Value = ", self.new, " Action = ", self.new_a)

        return self.new, self.new_a

    def slider_number_changed(self):
        new_value = self.scroll_speed_slider_2.value()
        return new_value

    def onApply(self):
        self.applied.emit(self.a1, self.a2, self.a3, self.a4)
        self.scroll_slider.emit(self.scroll_speed_slider_2.value())
        print(self.a1, self.a2, self.a3, self.a4, self.scroll_speed_slider_2.value())
        # self.close()

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()
        # return self.a1, self.a2, self.a3
        # event.ignore() # if you want the window to never be closed

    def main_upd(self):
        from testMainGUI import MainVideoWindow
        self.main = MainVideoWindow()
        self.main.close()

    @QtCore.pyqtSlot(int)
    def change_func(self, index):
        data = self.comboBox.itemData(index)
        if data:
            self.trans.load(data)
            QtWidgets.QApplication.instance().installTranslator(self.trans)
        else:
            QtWidgets.QApplication.instance().removeTranslator(self.trans)

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.LanguageChange:
            self.retranslateUi(self)
        super(SettingWindows, self).changeEvent(event)

    def get_a1_result(self):
        # print("A1 at Sett = ", self.a1)
        # testMainGUI.ThreadClass.a1 = self.a1
        # print("A1 at Thread = ", testMainGUI.ThreadClass.a1)
        # os.execl(sys.executable, sys.executable, *sys.argv)
        # self.main_upd()
        return self.a1

    def get_a2_result(self):
        # print("A2 at Sett = ", self.a2)
        # testMainGUI.ThreadClass.a2 = self.a2
        # print("A2 at Thread = ", testMainGUI.ThreadClass.a2)
        # print("A2 at Sett = ", self.a2)
        # os.execl(sys.executable, sys.executable, *sys.argv)
        # self.main_upd()
        return self.a2

    def get_a3_result(self):
        print("A3 at Sett = ", self.a3)
        testMainGUI.ThreadClass.a3 = self.a3
        print("A3 at Thread = ", testMainGUI.ThreadClass.a3)
        # print("A2 at Sett = ", self.a2)
        # os.execl(sys.executable, sys.executable, *sys.argv)
        # self.main_upd()
        return self.a3, testMainGUI.ThreadClass.a3

    def onClicked(self, rb, rb_type):
        if rb_type == "Left Click":
            if rb.text() == "Left eye":
                if rb.isChecked():
                    self.a1 = self.choose_left_click(2)
            elif rb.text() == "Right eye":
                if rb.isChecked():
                    self.a1 = self.choose_left_click(1)
            elif rb.text() == "Smile":
                if rb.isChecked():
                    self.a1 = self.choose_left_click(3)
            elif rb.text() == "Eye Brows":
                if rb.isChecked():
                    self.a1 = self.choose_left_click(4)
        elif rb_type == "Right Click":
            if rb.text() == "Left eye":
                if rb.isChecked():
                    self.a2 = self.choose_left_click(2)
            elif rb.text() == "Right eye":
                if rb.isChecked():
                    self.a2 = self.choose_left_click(1)
            elif rb.text() == "Smile":
                if rb.isChecked():
                    self.a2 = self.choose_left_click(3)
            elif rb.text() == "Eye Brows":
                if rb.isChecked():
                    self.a2 = self.choose_left_click(4)
        elif rb_type == "Scroll Mode":
            if rb.text() == "Smile":
                if rb.isChecked():
                    self.a3 = self.choose_scroll_active(1)
            elif rb.text() == "Blink":
                if rb.isChecked():
                    self.a3 = self.choose_scroll_active(3)
            elif rb.text() == "Eye Brows":
                if rb.isChecked():
                    self.a3 = self.choose_scroll_active(2)
        elif rb_type == "Alarm mode":
            if rb.text() == "ON":
                if rb.isChecked():
                    self.a4 = self.choose_alarm_active("yes")
            elif rb.text() == "OFF":
                if rb.isChecked():
                    self.a4 = self.choose_alarm_active("no")

    def choose_left_click(self, argument):
        self.l_eyeBrows_rb.clicked.connect(lambda: self.get_l_click_result(self.l_eyeBrows_rb))
        switcher = {
            1: "right_eye",
            2: "left_eye",
            3: "smile",
            4: "brow"
        }
        # Get the function from switcher dictionary
        return switcher.get(argument, "invalid choise")

    def choose_right_click(self, argument):
        switcher = {
            1: "right_eye",
            2: "left_eye",
            3: "smile",
            4: "brow"

        }
        # Get the function from switcher dictionary
        return switcher.get(argument, "invalid choise")

    def choose_scroll_active(self, argument):
        switcher = {
            1: "smile",
            2: "brow",
            3: "blink"

        }
        # Get the function from switcher dictionary
        return switcher.get(argument, "invalid choise")

    def choose_alarm_active(self, argument):
        switcher = {
            "yes": "on",
            "no": "off"
        }
        # Get the function from switcher dictionary
        return switcher.get(argument, "invalid choise")


class TestThread(QThread):
    update_value1 = pyqtSignal(str)
    update_value2 = pyqtSignal(str)
    update_value3 = pyqtSignal(str)
    update_value4 = pyqtSignal(str)

    def run(self):
        self.sett = SettingWindows()
        while True:
            QThread.sleep(1)
            value = self.sett.a1
            value2 = self.sett.a2
            value3 = self.sett.a3
            value4 = self.sett.a4
            self.update_value1.emit(value)
            self.update_value2.emit(value2)
            self.update_value3.emit(value3)
            self.update_value4.emit(value4)


def sound_alarm(path):
    # play an alarm sound
    playsound.playsound(path)


def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])
    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)
    # return the eye aspect ratio
    return ear


def midpoint(p1, p2):
    return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)


def Mouth_action(eye_points, facial_landmarks):
    right_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    l_point = (facial_landmarks.part(eye_points[1]).x, facial_landmarks.part(eye_points[1]).y)
    length = hypot((right_point[0] - l_point[0]), (right_point[1] - l_point[1]))
    return length


def eyebrow(points, facial_landmarks):
    right_point = (facial_landmarks.part(points[0]).x, facial_landmarks.part(points[0]).y)
    l_point = (facial_landmarks.part(points[1]).x, facial_landmarks.part(points[1]).y)
    length = hypot((right_point[0] - l_point[0]), (right_point[1] - l_point[1]))
    return length


def face_line(points, facial_landmarks):
    right_point = (facial_landmarks.part(points[0]).x, facial_landmarks.part(points[0]).y)
    l_point = (facial_landmarks.part(points[1]).x, facial_landmarks.part(points[1]).y)
    length = hypot((right_point[0] - l_point[0]), (right_point[1] - l_point[1]))
    return length


def brow_scroll(points, facial_landmarks):
    right_point = (facial_landmarks.part(points[0]).x, facial_landmarks.part(points[0]).y)
    l_point = (facial_landmarks.part(points[1]).x, facial_landmarks.part(points[1]).y)
    length = hypot((right_point[0] - l_point[0]), (right_point[1] - l_point[1]))
    return length


def smile_V(points, facial_landmarks):
    right_point = (facial_landmarks.part(points[0]).x, facial_landmarks.part(points[0]).y)
    l_point = (facial_landmarks.part(points[1]).x, facial_landmarks.part(points[1]).y)
    length = hypot((right_point[0] - l_point[0]), (right_point[1] - l_point[1]))
    return length


def smile_H(points, facial_landmarks):
    right_point = (facial_landmarks.part(points[0]).x, facial_landmarks.part(points[0]).y)
    l_point = (facial_landmarks.part(points[1]).x, facial_landmarks.part(points[1]).y)
    length = hypot((right_point[0] - l_point[0]), (right_point[1] - l_point[1]))
    return length


def brow(points, facial_landmarks):
    right_point = (facial_landmarks.part(points[0]).x, facial_landmarks.part(points[0]).y)
    l_point = (facial_landmarks.part(points[1]).x, facial_landmarks.part(points[1]).y)
    length = hypot((right_point[0] - l_point[0]), (right_point[1] - l_point[1]))
    return length


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = SettingWindows()
    MainWindow.show()
    sys.exit(app.exec_())
