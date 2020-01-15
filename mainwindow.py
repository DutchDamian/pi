from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QPixmap, QImage, QPainter, QPen, QBrush, QFont, QColor
#from typing import Union
import sys
import cv2
import threading
import time
import os
import RPi.GPIO as GPIO

class UI_Window(QWidget):
    counterSignal = pyqtSignal(str)
    distanceSignal = pyqtSignal(str)

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(15,GPIO.OUT)

    def __init__(self):
        QWidget.__init__(self)

        screenWidth = 780
        screenHeight = 480
        GPIO.output(15,GPIO.HIGH)

        # QTimer uses QFrameSlots wherein every video frame from the live preview is encoded.
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        # self.timer.timeout.connect(self.requestPower)
        # self.timer.timeout.connect(self.requestDistance)
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.view.setStyleSheet("border: 0px")
        self.view.setFrameStyle(QFrame.NoFrame)
        layout = QVBoxLayout(self)

        self.openCamera()

        self.label = QLabel()
        self.label.setFixedSize(778, 443)

        # QPen is used to change the properties of the middle line drawn in the GUI.
        pen = QPen()
        pen.setWidth(7)
        pen.setColor(Qt.green)
        # QFont is used to change the properties of the text rendered in the GUI.
        font = QFont('Noto')
        font.setPixelSize(26)

        font2 = QFont('Noto')
        font2.setPixelSize(70)

        # Pixmaps
        happyMeasurePixmap = QPixmap.fromImage(QImage('img/happy_measure.png'))
        create4CarePixmap = QPixmap.fromImage(QImage('img/create4care.png'))
        self.batteryEmptyPixmap = QPixmap.fromImage(QImage('img/battery_empty.png'))
        self.warningPixmap = QPixmap.fromImage(QImage('img/warning.png'))
        self.warningPlaceholderPixmap = QPixmap.fromImage(QImage('img/warning_placeholder.png'))
        self.battery100Pixmap = QPixmap.fromImage(QImage('img/battery_100.png'))
        self.battery80Pixmap = QPixmap.fromImage(QImage('img/battery_80.png'))
        self.battery60Pixmap = QPixmap.fromImage(QImage('img/battery_60.png'))
        self.battery40Pixmap = QPixmap.fromImage(QImage('img/battery_40.png'))
        self.battery20Pixmap = QPixmap.fromImage(QImage('img/battery_20.png'))
        self.battery0Pixmap = QPixmap.fromImage(QImage('img/battery_0.png'))

        # Labels
        self.batteryLabel = QLabel()
        self.batteryLabel.setFixedSize(120, 41)
        self.batteryLabel.setGeometry(39,30,0,0)

        self.warningLabel = QLabel()
        self.warningLabel.setFixedSize(129,66)
        self.warningLabel.setGeometry(39,200,0,0)
        self.warningLabel.setPixmap(self.warningPlaceholderPixmap)

        self.emptyLabel = QLabel()
        self.emptyLabel.setFixedSize(209, 219)
        self.emptyLabel.setGeometry(500,110,0,0)
        self.emptyLabel.setStyleSheet("background:transparent")

        # Shapes & Lines
        backgroundRectangle = QGraphicsRectItem(0, 0, 200, 443)
        backgroundRectangle.setBrush(QBrush(QColor(47, 47, 125)))

        # TextItems
        self.batteryTextItem = QGraphicsTextItem("100%")
        self.batteryTextItem.setFont(font)
        self.batteryTextItem.setDefaultTextColor(Qt.white)
        self.batteryTextItem.setPos(39 + 30, 75)

        self.counterSignal.connect(self.batteryTextItem.setPlainText)
        # self.distanceSignal.connect(self.lengthTextItem.setPlaintext)
        threading.Thread(target=self.counterThread).start()
        threading.Thread(target=self.standbyThread).start()

        # Add all widgets - THE ORDER OF THE ADDWIDGETS DECIDES WHICH WIDGETS APPEAR ON THE FOREGROUND
        layout.addWidget(self.view)
        self.scene.addWidget(self.label)
        self.scene.addItem(backgroundRectangle)
        # self.scene.addItem(lengthTextItem)
        self.scene.addItem(self.batteryTextItem)
        self.scene.addWidget(self.batteryLabel)
        self.scene.addWidget(self.warningLabel)
        self.scene.addWidget(self.emptyLabel)
        # self.batteryPixmapItem = self.scene.addPixmap(battery100Pixmap).setPos(39,30)
        self.happyMeasurePixmapItem = self.scene.addPixmap(
            happyMeasurePixmap).setPos(38, 307)
        self.create4CarePixmapItem = self.scene.addPixmap(
            create4CarePixmap).setPos(38, 386)
        # If lineThickness < 10: startX = 10 - lineThickness & endY = 480 - startX
        self.lineItem = self.scene.addLine(400, 3, 400, 438, pen)

        self.setLayout(layout)
        self.setWindowTitle("EEP71")

    def openCamera(self):
        '''Opens the camera using OpenCV. This method works when only one camera is connected and will default to the first camera it can find.'''
        self.vc = cv2.VideoCapture(0)
        self.vc.set(3, 800)
        self.vc.set(4, 480)

        if not self.vc.isOpened():
            msgBox = QMessageBox()
            msgBox.setText("Failed to open camera.")
            msgBox.exec_()
            return

        self.timer.start(50)

    def requestPower(self):
        print("bla")

    def requestDistance(self):
        print("bla")

    def counterThread(self):
        self.batteryLabel.setPixmap(self.battery80Pixmap)

        for x in range(65, 0, -1):
            if (x == 79):
               self.batteryLabel.setPixmap(self.battery80Pixmap)
            if (x == 59):
                self.batteryLabel.setPixmap(self.battery60Pixmap)
            if (x == 39):
                self.batteryLabel.setPixmap(self.battery40Pixmap)
            if (x == 19):
                self.warningLabel.setPixmap(self.warningPixmap)
                self.batteryLabel.setPixmap(self.battery20Pixmap)
            if (x == 9):
                self.emptyLabel.setPixmap(self.batteryEmptyPixmap)
            if (x == 0):
                self.batteryLabel.setPixmap(self.battery0Pixmap)
            self.counterSignal.emit(str(x)+"%")
            time.sleep(.25)
    
    def standbyThread(self):
        timer = 0
        while True:
            if (timer == 12):
                timer = 0
                GPIO.output(15,GPIO.HIGH)
            else:
                if (timer == 10):
                    timer = 0
                    GPIO.output(15,GPIO.LOW)
                timer += 1
            time.sleep(1)

    def stopCamera(self):
        '''Stops the camera.'''
        self.timer.stop()

    # https://stackoverflow.com/questions/41103148/capture-webcam-video-using-pyqt
    def nextFrameSlot(self):
        '''Reads the next frame from the OpenCV camera object and outputs it to a QPixmap.'''
        rval, frame = self.vc.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1],
                       frame.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)



def main():
    app = QApplication(sys.argv)
    ex = UI_Window()
    ex.setWindowFlags(Qt.FramelessWindowHint)
    ex.show()
    ex.showFullScreen()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
