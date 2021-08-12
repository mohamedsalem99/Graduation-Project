import sys
import time

from PyQt5 import QtCore
from PyQt5.QtCore import *
# Importing Libraries
from PyQt5.QtWidgets import *
import cv2
from pop_up_win import Ui_Form
from popup_main import PopUpWin


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.flag = 0
        self.setWindowTitle('ٍSplash Screen')
        self.setFixedSize(800, 450)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.frame = QFrame()
        self.frame.setObjectName("splash_frame")
        self.labelTitle = QLabel(self.frame)
        self.labelDescription = QLabel(self.frame)
        self.progressBar = QProgressBar(self.frame)
        self.labelLoading = QLabel(self.frame)
        self.counter = 0
        self.n = 300  # total instance

        self.initUI()

        self.timer = QTimer()
        self.timer.timeout.connect(self.loading)
        self.timer.start(30)

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.frame)

        self.labelTitle.setObjectName('LabelTitle')

        # center labels
        self.labelTitle.resize(self.width() - 10, 150)
        self.labelTitle.move(0, 40)  # x, y
        self.labelTitle.setText('Help Me')
        self.labelTitle.setAlignment(Qt.AlignCenter)

        self.labelDescription.resize(self.width() - 10, 50)
        self.labelDescription.move(0, self.labelTitle.height())
        self.labelDescription.setObjectName('LabelDesc')
        self.labelDescription.setText('<strong></strong>')
        self.labelDescription.setAlignment(Qt.AlignCenter)

        self.progressBar.resize(self.width() - 200 - 10, 50)
        self.progressBar.setObjectName("splash_pro_bar")
        self.progressBar.move(100, self.labelDescription.y() + 130)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setFormat('%p%')
        self.progressBar.setTextVisible(True)
        self.progressBar.setRange(0, self.n)
        self.progressBar.setValue(20)

        self.labelLoading.resize(self.width() - 10, 50)
        self.labelLoading.move(0, self.progressBar.y() + 70)
        self.labelLoading.setObjectName('LabelLoading')
        self.labelLoading.setAlignment(Qt.AlignCenter)
        self.labelLoading.setText('loading...')
        self.retranslateUi(self)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Splash Screen"))
        self.labelTitle.setText(_translate("Form", "Help Me"))
        # self.labelDescription.setText(_translate("Form", "Follow next instructions"))

    def loading(self):
        self.progressBar.setValue(self.counter)

        if self.counter == int(self.n * 0.3):
            self.labelDescription.setText('<strong></strong>')
        elif self.counter == int(self.n * 0.6):
            self.labelDescription.setText('<strong></strong>')
        elif self.counter >= self.n:
            self.timer.stop()
            self.close()
            time.sleep(1)
            self.pop_win = PopUpWin()
            self.pop_win.show()
        self.counter += 1


"""
    def closeEvent(self, event):
        if self.flag == 1:
            return

        if self.flag == 0:
            event.accept()
            self.pop_win.show()
        else:
            event.ignore()
"""

if __name__ == '__main__':
    # don't auto scale when drag app to a different monitor.
    # QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        #LabelTitle {
            font-size: 60px;
            color: #FFF;
        }

        #LabelDesc {
            font-size: 30px;
            color: #c2ced1;
        }

        #LabelLoading {
            font-size: 30px;
            color: #FFF;
        }

        #splash_frame {
            background-color: #009688;
            color: rgb(220, 220, 220);
            border-radius: 15px;
        }

        #splash_pro_bar {
            background-color: #FFF;
            color: rgb(200, 200, 200);
            border-style: none;
            border-radius: 10px;
            text-align: center;
            font-size: 30px;
        }

        #splash_pro_bar::chunk {
            border-radius: 10px;
            background-color: qlineargradient(spread:pad x1:0, x2:1, y1:0.511364, y2:0.523, stop:0 #1C3334, stop:1 #376E6F);
        }
    ''')
    splash = SplashScreen()
    splash.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
