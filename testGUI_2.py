# from PyQt5.uic import loadUi
# Importing Libraries
from math import hypot
import numpy as np
from PyQt5 import QtWidgets as qtw
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

# Initialize the frame counters for each action as well as
# booleans used to indicate if action is performed or not


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
        self.thread1.mouth_thresh_value.connect(self.progressBar.setValue)
        # Connect Signal to a Slot
        self.thread1.ImageUpdate.connect(self.image_update_slot)
        # self.image_lbl.setPixmap(QtGui.QPixmap("cat.jpg"))
        # self.start_btn.clicked.connect(self.thread1.start)
        # Opening the Vertical Window with the Main Window
        self.open_vertical_win()
        self.zoom_window_res()
        # self.vertical_window_res()
        self.thread1.button_color.connect(self.button_color)

    def button_color(self, color):
        if color == "blue":
            self.ui_sec.rms_btn.setStyleSheet("background-color:" + color)
            self.ui_sec.lms_btn.setStyleSheet("")
        elif color == "red":
            self.ui_sec.lms_btn.setStyleSheet("background-color:" + color)
            self.ui_sec.rms_btn.setStyleSheet("")

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
        self.open_zoom_win()
        # self.cancel_thread()
        self.ui_sec.move(self.screen_width - 170, self.screen_height - 850)
        # self.cancel_thread()
        # self.ui_sec.hide()

    def open_zoom_win(self):
        video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        while True:
            ret, frame = video.read()
            if ret:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert the Frame to rgb image
                image = cv2.flip(image, 1)
                rects = detector(image, 0)
                if len(rects) > 0:
                    rect = rects[0]
                else:
                    continue
                self.thread1.detect_img(image, rect)

                convert_to_qt_format = QImage(image.data, image.shape[1], image.shape[0],
                                              QImage.Format_RGB888)  # convert image to QT
                picture = convert_to_qt_format.scaled(400, 300, Qt.KeepAspectRatio)
                self.zoom_window.img_lbl.setPixmap(QPixmap.fromImage(picture))
                key = cv2.waitKey(1) & 0xFF
                # If the `Esc` key was pressed, break from the loop
                if key == 27:
                    break
            self.zoom_window.show()

        cv2.destroyAllWindows()
        video.release()

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
        self.thread2.start()

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
class ThreadClass(QThread, QWidget):
    # Handles retrieving Image from Webcam and convert it to a format that PyQt can understand
    # Signal Image
    def __init__(self, width, height):
        super().__init__()
        self.capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
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
        self.ANCHOR_POINT = (0, 0)
        self.WHITE_COLOR = (255, 255, 255)
        self.YELLOW_COLOR = (0, 255, 255)
        self.RED_COLOR = (0, 0, 255)
        self.GREEN_COLOR = (0, 255, 0)
        self.BLUE_COLOR = (255, 0, 0)
        self.BLACK_COLOR = (0, 0, 0)

        # Edited
        self.MOUTH_AR_THRESH = 0.5  # تتحكم فى مدى فتحة الفم عند الشخص
        self.MOUTH_AR_CONSECUTIVE_FRAMES = 5  # تتحكم فى مدى فترة ظهور كلمة Reading Input
        self.EYE_AR_THRESH = 0.20  # ده المعدل اللى عليه العينين بيتقفلوا علشان لو زادت عن القيمة ديه معناها ان العين بتتقفل كتير لو
        # لو قلت يبقى العين مفتوحة
        self.EYE_AR_CONSECUTIVE_FRAMES = 5
        self.WINK_AR_DIFF_THRESH = 0.001
        self.WINK_AR_CLOSE_THRESH = 0.2
        self.WINK_CONSECUTIVE_FRAMES = 4

    ImageUpdate = pyqtSignal(QImage)
    mouth_thresh_value = pyqtSignal(int)
    button_color = pyqtSignal(str)

    # Run function
    def run(self):
        while self.ThreadActive:
            ret, frame = self.capture.read()
            if ret:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert the Frame to rgb image
                image = cv2.flip(image, 1)
                # ----------------------------------------------
                rects = detector(image, 0)
                if len(rects) > 0:
                    rect = rects[0]
                else:
                    continue
                self.detect_img(image, rect)
        cv2.destroyAllWindows()
        self.capture.release()

    def detect_img(self, image, rect):
        # Determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        shape = predictor(image, rect)
        shape = face_utils.shape_to_np(shape)
        # Extract the left and right eye coordinates, then use the
        # coordinates to compute the eye aspect ratio for both eyes
        mouth = shape[mStart:mEnd]
        left_eye = shape[lStart:lEnd]
        right_eye = shape[rStart:rEnd]
        nose = shape[nStart:nEnd]
        # Because I flipped the frame, left is right, right is left.
        temp = left_eye
        left_eye = right_eye
        right_eye = temp
        # Average the mouth aspect ratio together for both eyes
        mar = mouth_aspect_ratio(mouth)
        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)
        ear = (left_ear + right_ear) / 2.0
        diff_ear = np.abs(left_ear - right_ear)
        nose_point = (nose[3, 0], nose[3, 1])
        # Compute the convex hull for the left and right eye, then
        # visualize each of the eyes
        mouth_hull = cv2.convexHull(mouth)
        left_eye_hull = cv2.convexHull(left_eye)
        right_eye_hull = cv2.convexHull(right_eye)
        cv2.drawContours(image, [mouth_hull], -1, self.YELLOW_COLOR, 1)
        cv2.drawContours(image, [left_eye_hull], -1, self.YELLOW_COLOR, 1)
        cv2.drawContours(image, [right_eye_hull], -1, self.YELLOW_COLOR, 1)
        # print(mar)
        # self.progressBar.setValue((diff_ear * 10))
        for (x, y) in np.concatenate((mouth, left_eye, right_eye), axis=0):
            cv2.circle(image, (x, y), 2, self.GREEN_COLOR, -1)
        # self.input_mode()
        # Check to see if the eye aspect ratio is below the blink
        # threshold, and if so, increment the blink frame counter
        mar_temp = mar
        # print(mar_temp * 100)
        self.mouth_thresh_value.emit(mar_temp * 100)
        # QThread.msleep(100)
        if diff_ear > self.WINK_AR_DIFF_THRESH:

            if left_ear < right_ear:
                if left_ear < self.EYE_AR_THRESH:
                    self.WINK_COUNTER += 1
                    # print(self.WINK_COUNTER)
                    if self.WINK_COUNTER > self.WINK_CONSECUTIVE_FRAMES:
                        pag.doubleClick(button='left')
                        self.button_color.emit("red")
                        self.WINK_COUNTER = 0

            elif left_ear > right_ear:
                if right_ear < self.EYE_AR_THRESH:
                    self.WINK_COUNTER += 1

                    if self.WINK_COUNTER > self.WINK_CONSECUTIVE_FRAMES:
                        self.button_color.emit("blue")
                        pag.click(button='right')
                        self.WINK_COUNTER = 0
            else:
                self.WINK_COUNTER = 0
        else:
            if ear <= self.EYE_AR_THRESH:
                self.EYE_COUNTER += 1

                if self.EYE_COUNTER > self.EYE_AR_CONSECUTIVE_FRAMES:
                    self.SCROLL_MODE = not self.SCROLL_MODE
                    # INPUT_MODE = not INPUT_MODE
                    self.EYE_COUNTER = 0

                    # nose point to draw a bounding box around it

            else:
                self.EYE_COUNTER = 0
                self.WINK_COUNTER = 0
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

        if self.INPUT_MODE:
            cv2.putText(image, "READING INPUT!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.RED_COLOR, 2)
            x, y = self.ANCHOR_POINT
            nx, ny = nose_point
            w, h = 30, 30
            r = 30
            # 3rd (EDITED)
            # w,h = 80,40
            multiple = 1
            # cv2.rectangle(image, (x - w, y - h), (x + w, y + h), self.GREEN_COLOR, 2)
            cv2.circle(image, (x, y), r, self.GREEN_COLOR, 2)
            cv2.line(image, self.ANCHOR_POINT, nose_point, self.BLUE_COLOR, 2)

            dir_ = direction(nose_point, self.ANCHOR_POINT, w, h)
            cv2.putText(image, dir_.upper(), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.RED_COLOR, 2)
            drag = hypot(x - nx, y - ny) - r
            x1 = (x - nx)
            y1 = (y - ny)
            a = y1 / x1
            # print(nx, ny)
            if dir_ == 'right':
                pag.moveRel(drag, a * drag)
            elif dir_ == 'left':
                pag.moveRel(-drag, (-a * drag))

            elif dir_ == 'up':
                # if self.SCROLL_MODE:
                #    pag.scroll(40)
                # else:
                pag.moveRel(0, -drag)

            elif dir_ == 'down':
                # if self.SCROLL_MODE:
                #    pag.scroll(-40)
                # else:
                pag.moveRel(0, drag)

        if self.SCROLL_MODE:
            cv2.putText(image, 'SCROLL MODE IS ON!', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.RED_COLOR, 2)

        # Flip image
        convert_to_qt_format = QImage(image.data, image.shape[1], image.shape[0],
                                      QImage.Format_RGB888)  # convert image to QT
        picture = convert_to_qt_format.scaled(self.width, self.height, Qt.KeepAspectRatio)
        self.ImageUpdate.emit(picture)
        print(image)

    def stop(self):
        self.ThreadActive = False


if __name__ == '__main__':
    qApp = QApplication(sys.argv)
    mainWindow = MainVideoWindow()
    mainWindow.show()
    sys.exit(qApp.exec_())
