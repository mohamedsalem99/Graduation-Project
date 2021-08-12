import sys
import time
from PyQt5 import QtWidgets as qtw
from PyQt5.QtCore import *
# Importing Libraries
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import cv2
from pop_up_win import Ui_Form
from testMainGUI import MainVideoWindow


class PopUpWin(QWidget, Ui_Form):
    def __init__(self):
        super(PopUpWin,self).__init__()
        self.ui = Ui_Form()
        self.setupUi(self)
        self.setFixedSize(800, 800)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.counter = 0
        self.n = 300  # total instance
        self.thread1 = ThreadClass(400, 300)
        self.thread1.start()  # Signal will be emitted
        # Connect Signal to a Slot
        self.thread1.ImageUpdate.connect(self.image_update_slot)

        self.initUI()

        self.timer = QTimer()
        self.timer.timeout.connect(self.loading)
        self.timer.start(45)

    # Instructions
    # 1- Open Your Eyes
    # 2- Smile Moderately
    # 3- Open Your Mouth
    # 4- All done. You are ready to begin the program

    def initUI(self):
        # center labels
        self.labelTitle.setText('Welcome to HELP ME APPLICATION')
        self.labelTitle.setAlignment(Qt.AlignCenter)

        self.labelDescription.setText('Follow next instructions')
        self.labelDescription.setAlignment(Qt.AlignCenter)

        self.image_lbl.setAlignment(Qt.AlignCenter)

        self.progressBar.setFormat('%p%')
        self.progressBar.setTextVisible(True)
        self.progressBar.setRange(0, self.n)

        self.labelLoading.setAlignment(Qt.AlignCenter)
        self.labelLoading.setText('Open Your Eyes')

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.labelLoading.setText(_translate("Form", "Open Your Eyes"))
        self.labelLoading.setText(_translate("Form", "Smile Moderately"))
        self.labelLoading.setText(_translate("Form", "Open Your Mouth"))
        self.labelLoading.setText(_translate("Form", "All done. You are ready to begin the program"))

    def image_update_slot(self, image):  # Takes the Image as an Input
        self.image_lbl.setPixmap(QPixmap.fromImage(image))

    def loading(self):
        self.progressBar.setValue(self.counter)

        if self.counter == int(self.n * 0.3):
            # self.thread1.labelLoad.connect(self.labelLoading.setText('<strong>Smile Moderately</strong>'))
            text = '<strong>Smile Moderately</strong>'
            self.labelLoading.setText(text)
        elif self.counter == int(self.n * 0.6):
            text = '<strong>Open Your Mouth</strong>'
            # self.thread1.labelLoad.connect(self.labelLoading.setText('<strong>Open Your Mouth</strong>'))
            self.labelLoading.setText(text)
        elif self.counter == int(self.n * 0.9):
            # self.thread1.labelLoad.connect(self.labelLoading.setText('<strong>All done. You are ready to begin the program</strong>'))
            text = '<strong>All done. You are ready to begin the program</strong>'
            self.labelLoading.setText(text)
        elif self.counter >= self.n:
            self.timer.stop()
            self.close()

            time.sleep(1)
            self.load_main()

        self.counter += 1

    def load_main(self):
        self.thread1.stop()
        self.thread1.terminate()
        self.main_win = MainVideoWindow()
        self.main_win.show()


class ThreadClass(QThread):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.ThreadActive = True
    ImageUpdate = pyqtSignal(QImage)
    labelLoad = pyqtSignal(str)
    def run(self):
        capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        while self.ThreadActive:
            ret, frame = capture.read()
            if ret:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert the Frame to rgb image

                flipped_image = cv2.flip(image, 1)  # Flip image
                convert_to_qt_format = QImage(flipped_image.data, flipped_image.shape[1], flipped_image.shape[0],
                                              QImage.Format_RGB888)  # convert image to QT
                picture = convert_to_qt_format.scaled(self.width, self.height, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(picture)
    def stop(self):
        self.ThreadActive = False
        self.quit()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pop_win = PopUpWin()
    pop_win.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
