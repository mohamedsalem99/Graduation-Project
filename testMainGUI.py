# from PyQt5.uic import loadUi
# Importing Libraries
from math import hypot
from threading import Thread
import numpy as np
import playsound
from scipy.spatial import distance as dist
import imutils
import numpy as np
from PyQt5 import QtWidgets as qtw, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2
import pyautogui as pag
import dlib
import sys
# Importing Modules
from Vertical_Win_Main import VerticalWindowMain
from zoom_main import WindowMain
from utils import *
from read_video_app import Ui_Form
from PyQt5.QtWidgets import *
from imutils import face_utils
import Test2 as ts2
import argparse

# Initialize the frame counters for each action as well as
# booleans used to indicate if action is performed or not
ap = argparse.ArgumentParser()
ap.add_argument("-a", "--alarm", type=str, default="",
                help="TF010.WAV")
args = vars(ap.parse_args())
# Initialize Dlib's face detector (HOG-based) and then create
# the facial landmark predictor
shape_predictor = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(shape_predictor)
# Grab the indexes of the facial landmarks for the left and
# right eye, nose and mouth respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(nStart, nEnd) = face_utils.FACIAL_LANDMARKS_IDXS["nose"]
(mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]
(reStart, reEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eyebrow"]
(leStart, leEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eyebrow"]

resolution_w = int(ts2.w)
resolution_h = int(ts2.h)
cam_w = 600
cam_h = 800
unit_w = resolution_w / cam_w
unit_h = resolution_h / cam_h


# 23.14 of Screen 800,600 >>> 1920 x 1080 >>> 31.0
# 1366 x 768
class MainVideoWindow(Ui_Form, QWidget):
    def __init__(self, *args, **kwargs):
        super(MainVideoWindow, self).__init__(*args, **kwargs)
        self.flag = 0
        self.ui = Ui_Form()
        self.setupUi(self)
        # 1920 * 1080
        screen_size = qApp.desktop().screenGeometry()  # screen_size = (1920,1080) , 1366*768
        self.screen_width, self.screen_height = screen_size.width(), screen_size.height()
        # screen_width = 1920 , screen_height=1080
        self.new_height = ((self.frameGeometry().height() * self.screen_height) / 1080)
        # new_height =   (height of GUI    * 1080  ) /1080
        self.new_width = ((self.frameGeometry().width() * self.screen_width) / 1920)
        self.main_window_res()
        self.setFocus()
        self.zoom_window = WindowMain()
        self.new_zoom_height = ((self.zoom_window.frameGeometry().height() * self.screen_height) / 1080)
        self.new_zoom_width = ((self.zoom_window.frameGeometry().width() * self.screen_width) / 1920)
        self.ui_sec = VerticalWindowMain()
        self.thread1 = ThreadClass(self.new_width, self.new_height - 20)
        self.thread2 = ThreadClass(self.new_zoom_width, self.new_zoom_height - 20)
        self.thread1.start()  # Signal will be emitted
        self.thread1.mouth_thresh_value.connect(self.progressBar.setValue)
        self.thread1.ImageUpdate.connect(self.image_update_slot)
        self.open_vertical_win()
        self.zoom_window_res()
        self.thread1.button_color.connect(self.button_color)
        self.Setting_btn.clicked.connect(self.open_sett)
        self.cancel_btn.clicked.connect(self.cancel_thread)
        self.start_btn.clicked.connect(self.start_thread)

    def button_color(self, color):
        if color == "blue":
            self.ui_sec.rms_btn.setStyleSheet("background-color:" + color)
            self.ui_sec.lms_btn.setStyleSheet("")
        elif color == "red":
            self.ui_sec.lms_btn.setStyleSheet("background-color:" + color)
            self.ui_sec.rms_btn.setStyleSheet("")
        elif color == "green":
            self.ui_sec.scroll_btn.setStyleSheet("background-color:"+color)
            self.ui_sec.scroll_btn.setStyleSheet("")
        """
  def do_something(self):
      self.settin.get_a1_result()
      self.settin.get_a2_result()
      self.settin.get_a3_result()
      print("You closed the second window!")
           """

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
        # self.flag = 1
        # event.ignore()
        print("Minimize event")
        # self.move(0, 0)
        self.hide()
        self.thread1.terminate()
        self.open_zoom_win()
        self.ui_sec.move(self.screen_width - 170, self.screen_height - 850)
        # self.cancel_thread()
        # self.ui_sec.hide()

    def open_zoom_win(self):
        self.zoom_window.show()
        self.thread2.start()
        self.thread2.ImageUpdate.connect(self.zoom_img_update_slot)
        self.thread2.button_color.connect(self.button_color)

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
        self.thread1.terminate()

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

    def open_sett(self):
        from settings_main import SettingWindows
        self.sett = SettingWindows()
        self.sett.window_closed.connect(self.print_choises)
        # self.sett.scroll_slider.connect(self.get_scroll_value)
        print("Values = ", self.thread1.a1, self.thread1.a2, self.thread1.a3, self.thread1.a4)
        self.thread1.a1 = self.sett.a1
        self.thread1.a2 = self.sett.a2
        self.thread1.a3 = self.sett.a3
        # self.sett.setupUi(self.sett)
        self.sett.show()

    def get_scroll_value(self, value):
        self.thread1.sence_scroll = value

    def print_choises(self):
        print(self.sett.a1, self.sett.a2, self.sett.a3)

    @QtCore.pyqtSlot(int)
    def change_func(self, index):
        data = self.comboBox.itemData(index)
        if data:
            self.trans.load(data)
            qtw.QApplication.instance().installTranslator(self.trans)
        else:
            qtw.QApplication.instance().removeTranslator(self.trans)

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.LanguageChange:
            self.retranslateUi(self)

        super(MainVideoWindow, self).changeEvent(event)


# Creating Class Thread
class ThreadClass(QThread, QWidget):
    # Handles retrieving Image from Webcam and convert it to a format that PyQt can understand
    # Signal Image
    def __init__(self, width, height):
        super(ThreadClass, self).__init__()
        from settings_main import SettingWindows
        self.setting = SettingWindows()
        # self.a1 = "left_eye"
        # self.a2 = "right_eye"
        # self.a3 = "smile"
        # self.a4 = "off"
        #
        # self.a1 = self.setting.choose_left_click(self.x1)
        # self.a2 = self.setting.choose_right_click(self.x2)
        # self.a3 = self.setting.choose_scroll_active(self.x3)

        # print(" Value of A1 = ", self.setting.a1)
        # print(" Value of A2 = ", self.setting.a2)
        # print(" Value of A3 = ", self.a3)
        # self.setting.applied.connect(lambda: self.update_choises())
        # self.x1 = self.setting.l_leftEye_rb.toggled.
        # self.a4 = self.setting.get_a4_result()[0]
        # self.setting.setupUi(self.setting)
        self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.width = width
        self.height = height
        self.ThreadActive = True
        self.MOUTH_COUNTER = 0
        self.EYE_COUNTER = 0
        self.WINK_COUNTER = 0
        self.INPUT_MODE = False
        self.EYE_CLICK = False
        self.LEFT_WINK = False
        self.RIGHT_WINK = False
        self.SCROLL_MODE = False
        self.ALARM_ON = False
        self.ANCHOR_POINT = (0, 0)
        self.WHITE_COLOR = (255, 255, 255)
        self.YELLOW_COLOR = (0, 255, 255)
        self.RED_COLOR = (0, 0, 255)
        self.GREEN_COLOR = (0, 255, 0)
        self.BLUE_COLOR = (255, 0, 0)
        self.BLACK_COLOR = (0, 0, 0)

        # Edited
        self.MOUTH_AR_THRESH = 0.6  # تتحكم فى مدى فتحة الفم عند الشخص
        self.MOUTH_AR_CONSECUTIVE_FRAMES = 5  # تتحكم فى مدى فترة ظهور كلمة Reading Input
        self.EYE_AR_THRESH = 0.19  # ده المعدل اللى عليه العينين بيتقفلوا علشان لو زادت عن القيمة ديه معناها ان العين بتتقفل كتير لو
        # لو قلت يبقى العين مفتوحة
        self.EYE_AR_CONSECUTIVE_FRAMES = 15
        self.BROW_AR_CONSECUTIVE_FRAMES = 14.5
        self.WINK_AR_DIFF_THRESH = 0.03
        self.WINK_AR_CLOSE_THRESH = 0.1
        self.WINK_CONSECUTIVE_FRAMES = 1
        self.EYE_AR_CONSEC_FRAMES = 48  # for Alarm
        from settings_main import TestThread
        self.new_thread = TestThread()
        self.new_thread.update_value1.connect(self.update_choises)
        self.new_thread.update_value2.connect(self.update_choises2)
        self.new_thread.update_value3.connect(self.update_choises3)
        self.new_thread.update_value4.connect(self.update_choises4)

    ImageUpdate = pyqtSignal(QImage)
    mouth_thresh_value = pyqtSignal(int)
    button_color = pyqtSignal(str)

    @QtCore.pyqtSlot(str)
    def update_choises(self, choice_1):
        # self.a1 = self.setting.onClicked(self.setting.l_leftEye_rb,"Left Click")
        # self.a1 = self.setting.get_l_click_result(self.setting)
        self.a1 = choice_1
        print("Value of A1 = ", self.a1)

    @QtCore.pyqtSlot(str)
    def update_choises2(self, choice_1):
        self.a2 = choice_1
        print("Value of A2 = ", self.a2)

    @QtCore.pyqtSlot(str)
    def update_choises3(self, choice_1):
        self.a3 = choice_1
        print("Value of A3 = ", self.a3)

    @QtCore.pyqtSlot(str)
    def update_choises4(self, choice_1):
        self.a4 = choice_1
        print("Value of A4 = ", self.a4)

    def run(self):

        # self.a1, self.var2 = self.setting.get_a1_result()
        # self.main = MainVideoWindow()
        # self.main.setupUi(self.main)
        frames = 0
        self.sence_scroll = 100

        while self.ThreadActive:
            self.new_thread.start()
            # self.a1, self.var2 = self.setting.get_a1_result()
            # self.main.print_choises()
            # print("Value of A1 = ", self.a1)
            # print("Value of A2 = ", self.a2)
            # print("Value of A3 = ", self.a3)
            ret, frame = self.capture.read()
            # self.sence_scroll = self.setting.slider_number_changed()
            # print(self.sence_scroll)
            # print(self.a1, self.a2, self.a3, self.a4)
            if ret:
                # 600 *480
                # Convert the Frame to rgb image
                # Resize Image (600*300)
                # Reduce Frame
                # Buy HD CAMERA WITH 30 FPS
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # image = imutils.resize(frame, width=self.width, height=self.height)
                image = cv2.flip(image, 1)
                image = cv2.resize(image, (480, 350))
                frames += 1
                # ----------------------------------------------
                self.oo = 0
                self.length = 0
                faces = detector(image)
                for face in faces:
                    landmarks = predictor(image, face)
                    FACE_LINE = self.face_line([2, 16], landmarks)
                    BROW_SCROLL = self.brow_scroll([20, 39], landmarks)

                    l1 = self.smile_H([52, 58], landmarks)
                    l2 = self.smile_V([49, 55], landmarks)
                    self.oo = l2 / l1
                    self.length = BROW_SCROLL / FACE_LINE
                faces = detector(image, 0)
                if len(faces) > 0:
                    face = faces[0]
                else:
                    continue
                self.detect_img(image, face)
        cv2.destroyAllWindows()
        self.capture.release()

    def detect_img(self, image, face):
        # Determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        shape = predictor(image, face)
        shape = face_utils.shape_to_np(shape)
        # Extract the left and right eye coordinates, then use the
        # coordinates to compute the eye aspect ratio for both eyes
        mouth = shape[mStart:mEnd]
        left_eye = shape[lStart:lEnd]
        right_eye = shape[rStart:rEnd]
        nose = shape[nStart:nEnd]
        right_eyebrow = shape[reStart:reEnd]
        left_eyebrow = shape[leStart:leEnd]
        # Because I flipped the frame, left is right, right is left.
        temp = left_eye
        left_eye = right_eye
        right_eye = temp
        # Average the mouth aspect ratio together for both eyes
        mar = mouth_aspect_ratio(mouth)
        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)
        ear = (left_ear + right_ear) / 2.0
        # ALARM انذار

        # check to see if the eye aspect ratio is below the blink
        # threshold, and if so, increment the blink frame counter

        if ear < self.EYE_AR_THRESH:
            # print(self.COUNTER)
            self.COUNTER += 1

            # if the eyes were closed for a sufficient number of
            # then sound the alarm

            if self.COUNTER >= self.EYE_AR_CONSEC_FRAMES:
                # if the alarm is not on, turn it on
                if not self.ALARM_ON:
                    self.ALARM_ON = True
                    # check to see if an alarm file was supplied,
                    # and if so, start a thread to have the alarm
                    # sound played in the background
                    if args["alarm"] != "":
                        t = Thread(target=self.sound_alarm, args=(args["alarm"],))
                        t.deamon = True
                        t.start()
                # draw an alarm on the frame
                cv2.putText(image, "DROWSINESS ALERT!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                self.sound_alarm("TF010.wav")
        # otherwise, the eye aspect ratio is not below the blink
        # threshold, so reset the counter and alarm
        else:
            self.COUNTER = 0
            self.ALARM_ON = False

        nose_point = (nose[3, 0], nose[3, 1])
        # Compute the convex hull for the left and right eye, then
        # visualize each of the eyes
        mouth_hull = cv2.convexHull(mouth)
        left_eye_hull = cv2.convexHull(left_eye)
        right_eye_hull = cv2.convexHull(right_eye)
        right_eyebrowHull = cv2.convexHull(right_eyebrow)
        left_eyebrowHull = cv2.convexHull(left_eyebrow)

        cv2.drawContours(image, [right_eyebrowHull], -1, self.YELLOW_COLOR, 1)
        cv2.drawContours(image, [left_eyebrowHull], -1, self.YELLOW_COLOR, 1)
        cv2.drawContours(image, [mouth_hull], -1, self.YELLOW_COLOR, 1)
        cv2.drawContours(image, [left_eye_hull], -1, self.YELLOW_COLOR, 1)
        cv2.drawContours(image, [right_eye_hull], -1, self.YELLOW_COLOR, 1)

        # self.progressBar.setValue((diff_ear * 10))
        for (x, y) in np.concatenate((mouth, left_eye, right_eye), axis=0):
            cv2.circle(image, (x, y), 2, self.GREEN_COLOR, -1)
        # self.input_mode()
        # Check to see if the eye aspect ratio is below the blink
        # threshold, and if so, increment the blink frame counter
        mar_temp = mar
        self.mouth_thresh_value.emit(mar_temp * 100)
        # print("A1 at Main = ", self.a1)

        if mar > self.MOUTH_AR_THRESH:
            self.MOUTH_COUNTER += 1
            if self.MOUTH_COUNTER >= self.MOUTH_AR_CONSECUTIVE_FRAMES:
                # if the alarm is not on, turn it on
                self.INPUT_MODE = not self.INPUT_MODE
                # SCROLL_MODE = not SCROLL_MODE
                self.MOUTH_COUNTER = 0
                self.ANCHOR_POINT = nose_point
        else:
            self.MOUTH_COUNTER = 0

        # self.left_click_actions(diff_ear, left_ear, right_ear, self.a1)
        # self.right_click_actions(diff_ear, left_ear, right_ear, self.a2)
        # self.scroll_active_actions(diff_ear, ear, self.a3)
        # self.right_click_actions(diff_ear, left_ear, right_ear)

        if self.INPUT_MODE:
            cv2.putText(image, "READING INPUT!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.RED_COLOR, 2)

            # nx, ny = pag.position()
            # print(x,y)

            # if nx*nx+ny*ny == R*R:
            # w = nx
            # h = ny
            if self.a4 == "on":
                if ear < self.EYE_AR_THRESH:
                    # print(self.COUNTER)
                    self.COUNTER += 1
                    if self.COUNTER >= self.EYE_AR_CONSEC_FRAMES:
                        if not self.ALARM_ON:
                            self.ALARM_ON = True
                            if args["alarm"] != "":
                                t = Thread(rtaget=self.sound_alarm, args=(args["alarm"],))
                                t.deamon = True
                                t.start()
                        cv2.putText(image, "DROWSINESS ALERT!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        self.sound_alarm("TF010.wav")
                else:
                    self.COUNTER = 0
                    self.ALARM_ON = False
            diff_ear = np.abs(left_ear - right_ear)
            nose_point = (nose[3, 0], nose[3, 1])

            # Compute the convex hull for the left and right eye, then
            # visualize each of the eyes
            mouthHull = cv2.convexHull(mouth)
            leftEyeHull = cv2.convexHull(left_eye)
            rightEyeHull = cv2.convexHull(right_eye)
            right_eyebrowHull = cv2.convexHull(right_eyebrow)
            left_eyebrowHull = cv2.convexHull(left_eyebrow)

            cv2.drawContours(image, [right_eyebrowHull], -1, self.YELLOW_COLOR, 1)
            cv2.drawContours(image, [left_eyebrowHull], -1, self.YELLOW_COLOR, 1)
            cv2.drawContours(image, [mouthHull], -1, self.YELLOW_COLOR, 1)
            cv2.drawContours(image, [leftEyeHull], -1, self.YELLOW_COLOR, 1)
            cv2.drawContours(image, [rightEyeHull], -1, self.YELLOW_COLOR, 1)

            for (x, y) in np.concatenate((mouth, left_eye, right_eye), axis=0):
                cv2.circle(image, (x, y), 2, self.RED_COLOR, -1)
            mar_temp = mar
            self.mouth_thresh_value.emit(mar_temp * 100)

            # Check to see if the eye aspect ratio is below the blink
            # threshold, and if so, increment the blink frame counter
            # Left Click
            if diff_ear > self.WINK_AR_DIFF_THRESH:
                if self.a1 == "left_eye":
                    if left_ear < right_ear:
                        if left_ear < self.EYE_AR_THRESH:
                            self.WINK_COUNTER += 1

                            if self.WINK_COUNTER > self.WINK_CONSECUTIVE_FRAMES:
                                pag.click(button='left')
                                self.button_color.emit("red")
                                self.WINK_COUNTER = 0
                elif self.a1 == "right_eye":
                    if left_ear > right_ear:
                        if right_ear < self.EYE_AR_THRESH:
                            self.WINK_COUNTER += 1

                            if self.WINK_COUNTER > self.WINK_CONSECUTIVE_FRAMES:
                                pag.click(button='left')
                                self.button_color.emit("red")
                                self.WINK_COUNTER = 0
                else:
                    self.WINK_COUNTER = 0

            elif self.a1 == "smile":
                if self.oo > 1.7:
                    pag.click(button='left')
                    self.button_color.emit("red")
            elif self.a1 == "brow":
                if self.length > 0.25:
                    pag.click(button='left')
                    self.button_color.emit("red")
            #  Right Click
            if diff_ear > self.WINK_AR_DIFF_THRESH:
                if self.a2 == "left_eye":
                    if left_ear < right_ear:
                        if left_ear < self.EYE_AR_THRESH:
                            self.WINK_COUNTER += 1

                            if self.WINK_COUNTER > self.WINK_CONSECUTIVE_FRAMES:
                                pag.click(button='right')
                                self.button_color.emit("blue")
                                self.WINK_COUNTER = 0
                elif self.a2 == "right_eye":
                    if left_ear > right_ear:
                        if right_ear < self.EYE_AR_THRESH:
                            self.WINK_COUNTER += 1

                            if self.WINK_COUNTER > self.WINK_CONSECUTIVE_FRAMES:
                                pag.click(button='right')
                                self.button_color.emit("blue")
                                self.WINK_COUNTER = 0
                else:
                    self.WINK_COUNTER = 0
            elif self.a2 == "smile":
                if self.oo > 1.7:
                    pag.click(button='right')
                    self.button_color.emit("blue")
            elif self.a2 == "brow":
                if self.length > 0.25:
                    pag.click(button='right')
                    self.button_color.emit("blue")
            #  Active scroll mode
            if self.a3 == "smile":
                if self.oo > 1.666:
                    self.EYE_COUNTER += 1
                    # print(self.EYE_COUNTER)
                    if self.EYE_COUNTER > self.EYE_AR_CONSECUTIVE_FRAMES:
                        self.SCROLL_MODE = not self.SCROLL_MODE
                        # INPUT_MODE = not INPUT_MODE
                        self.EYE_COUNTER = 0
                        #self.button_color.emit("green")
                    # nose point to draw a bounding box around it
                    else:
                        # EYE_COUNTER = 0
                        self.WINK_COUNTER = 0

            elif self.a3 == "brow":
                if self.length > 0.25:
                    self.EYE_COUNTER += 1
                    # print(EYE_COUNTER)
                    if self.EYE_COUNTER > self.EYE_AR_CONSECUTIVE_FRAMES:

                        self.SCROLL_MODE = not self.SCROLL_MODE # not false = True
                        # INPUT_MODE = not INPUT_MODE
                        self.EYE_COUNTER = 0
                        #self.button_color.emit("green")
                    # nose point to draw a bounding box around it

                    else:
                        # EYE_COUNTER = 0
                        self.WINK_COUNTER = 0

            elif self.a3 == "blink":
                if diff_ear > self.WINK_AR_DIFF_THRESH:
                    if ear <= self.EYE_AR_THRESH:
                        self.EYE_COUNTER += 1

                        if self.EYE_COUNTER > self.EYE_AR_CONSECUTIVE_FRAMES:
                            self.SCROLL_MODE = not self.SCROLL_MODE
                            # INPUT_MODE = not INPUT_MODE
                            self.EYE_COUNTER = 0
                            #self.button_color.emit("green")
                    # nose point to draw a bounding box around it

                    else:
                        # EYE_COUNTER = 0
                        self.WINK_COUNTER = 0
            x, y = self.ANCHOR_POINT
            nx, ny = nose_point
            w, h = 30, 30
            w1, h1 = 30, 30
            R = 30
            multiple = 1
            xx = nx - x
            yy = ny - y
            a = yy / xx
            cv2.circle(image, (x, y), R, self.GREEN_COLOR, 2)
            dir = direction(nose_point, self.ANCHOR_POINT, w, h)

            # cv2.rectangle(frame, (x - w, y - h), (x + w, y + h), GREEN_COLOR, 2)
            cv2.line(image, self.ANCHOR_POINT, nose_point, self.BLUE_COLOR, 2)

            # dir = direction(nose_point , ANCHOR_POINT , w , h)
            cv2.putText(image, dir.upper(), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.RED_COLOR, 2)

            # xx, yy = pag.position()

            drag = hypot((x - nx), (y - ny)) - R
            if dir == 'right':
                # if ((nx-x)*(nx-x))+((ny-y)*(ny-y)) == R*R:
                # a = ny/nx
                pag.moveRel(drag, a * drag)

            # pag.moveRel(drag, 0)

            # pag.moveRel(drag, 0)
            # pag.moveTo(xx,yy)
            elif dir == 'left':
                pag.moveRel(-drag, -a * drag)
            # elif nx*nx+ny*ny == R*R:
            # pag.moveRel(drag, drag)
            elif dir == 'up':
                if self.SCROLL_MODE:
                    pag.scroll(self.sence_scroll)
                else:
                    pag.moveRel(0, -drag)
            elif dir == 'down':
                if self.SCROLL_MODE:
                    pag.scroll(-self.sence_scroll)
                else:
                    pag.moveRel(0, drag)

        # x, y = pag.position()
        # print(x, y)
        if self.SCROLL_MODE:
            cv2.putText(image, 'SCROLL MODE IS ON!', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.RED_COLOR, 2)
        convert_to_qt_format = QImage(image.data, image.shape[1], image.shape[0],
                                      QImage.Format_RGB888)  # convert image to QT
        picture = convert_to_qt_format.scaled(self.width, self.height, Qt.KeepAspectRatio)
        self.ImageUpdate.emit(picture)
        # h, w, c = image.shape

    def choose_left_click(self, argument):
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

    def stop(self):
        self.ThreadActive = False
        self.quit()
        cv2.destroyAllWindows()

    def sound_alarm(self, path):
        # play an alarm sound
        playsound.playsound(path)

    def eye_aspect_ratio(self, eye):
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

    def midpoint(self, p1, p2):
        return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)

    def Mouth_action(self, eye_points, facial_landmarks):
        right_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
        l_point = (facial_landmarks.part(eye_points[1]).x, facial_landmarks.part(eye_points[1]).y)
        lenght = hypot((right_point[0] - l_point[0]), (right_point[1] - l_point[1]))
        return lenght

    def eyebrow(self, points, facial_landmarks):
        right_point = (facial_landmarks.part(points[0]).x, facial_landmarks.part(points[0]).y)
        l_point = (facial_landmarks.part(points[1]).x, facial_landmarks.part(points[1]).y)
        lenght = hypot((right_point[0] - l_point[0]), (right_point[1] - l_point[1]))
        return lenght

    def face_line(self, points, facial_landmarks):
        right_point = (facial_landmarks.part(points[0]).x, facial_landmarks.part(points[0]).y)
        l_point = (facial_landmarks.part(points[1]).x, facial_landmarks.part(points[1]).y)
        lenght = hypot((right_point[0] - l_point[0]), (right_point[1] - l_point[1]))
        return lenght

    def brow_scroll(self, points, facial_landmarks):
        right_point = (facial_landmarks.part(points[0]).x, facial_landmarks.part(points[0]).y)
        l_point = (facial_landmarks.part(points[1]).x, facial_landmarks.part(points[1]).y)
        lenght = hypot((right_point[0] - l_point[0]), (right_point[1] - l_point[1]))
        return lenght

    def smile_V(self, points, facial_landmarks):
        right_point = (facial_landmarks.part(points[0]).x, facial_landmarks.part(points[0]).y)
        l_point = (facial_landmarks.part(points[1]).x, facial_landmarks.part(points[1]).y)
        lenght = hypot((right_point[0] - l_point[0]), (right_point[1] - l_point[1]))
        return lenght

    def smile_H(self, points, facial_landmarks):
        right_point = (facial_landmarks.part(points[0]).x, facial_landmarks.part(points[0]).y)
        l_point = (facial_landmarks.part(points[1]).x, facial_landmarks.part(points[1]).y)
        lenght = hypot((right_point[0] - l_point[0]), (right_point[1] - l_point[1]))
        return lenght

    def brow(self, points, facial_landmarks):
        right_point = (facial_landmarks.part(points[0]).x, facial_landmarks.part(points[0]).y)
        l_point = (facial_landmarks.part(points[1]).x, facial_landmarks.part(points[1]).y)
        lenght = hypot((right_point[0] - l_point[0]), (right_point[1] - l_point[1]))
        return lenght


if __name__ == '__main__':
    qApp = QApplication(sys.argv)
    mainWindow = MainVideoWindow()
    button = qtw.QPushButton("")
    mainWindow.show()
    sys.exit(qApp.exec_())

"""
    def onClicked(self, rb, rb_type):
        if self.setting.rb_type == "Left Click":
            if self.setting.rb.text() == "Left eye":
                if self.setting.rb.isChecked():
                    self.a1 = "left_eye"
                    return self.a1
            if self.setting.rb.text() == "Right eye":
                if self.setting.rb.isChecked():
                    self.a1 = "right_eye"
                    return self.a1
            if self.setting.rb.text() == "Smile":
                if self.setting.rb.isChecked():
                    self.a1 = "smile"
                    return self.a1
            if self.setting.rb.text() == "Eye Brows":
                if self.setting.rb.isChecked():
                    self.a1 = "brow"
                    return self.a1
        elif self.setting.rb_type == "Right Click":
            if self.setting.rb.text() == "Left eye":
                if self.setting.rb.isChecked():
                    self.a2 = self.choose_right_click(2)
                    return self.a2
            if self.setting.rb.text() == "Right eye":
                if self.setting.rb.isChecked():
                    self.a2 = self.choose_right_click(1)
                    return self.a2
            if self.setting.rb.text() == "Smile":
                if self.setting.rb.isChecked():
                    self.a2 = self.choose_right_click(3)
                    return self.a2
            if self.setting.rb.text() == "Eye Brows":
                if self.setting.rb.isChecked():
                    self.a2 = self.choose_right_click(4)
                    return self.a2
"""
