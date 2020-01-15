from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QPixmap, QImage, QPainter, QPen, QBrush, QFont, QColor
from typing import Union
import sys
import cv2
import threading
import time
import os
import RPi.GPIO as GPIO
from ctypes import *

class UI_Window(QWidget):
    #schuifmaat = CDLL("./schuifmaat.so")
    #schuifmaat.meassureDistance.restype = c_float
    counterSignal = pyqtSignal(str)
    distanceSignal = pyqtSignal(str)
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(15, GPIO.OUT)
    GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(8, GPIO.IN)
    GPIO.setup(10, GPIO.IN)
    GPIO.setup(9, GPIO.IN)
    GPIO.setup(11, GPIO.IN)
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
        layout = QVBoxLayout(self)

        time.sleep(5)
        self.openCamera()

        self.label = QLabel()
        self.label.setFixedSize(765, 443)

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
        #happyMeasurePixmap = QPixmap.fromImage(QImage('happy_measure.png'))
        #create4CarePixmap = QPixmap.fromImage(QImage('create4care.png'))
        self.batteryEmptyPixmap = QPixmap.fromImage(QImage('battery_empty.png'))
        self.warningPixmap = QPixmap.fromImage(QImage('warning.png'))
        self.warningPlaceholderPixmap = QPixmap.fromImage(QImage('warning_placeholder.png'))
        self.battery100Pixmap = QPixmap.fromImage(QImage('battery_100.png'))
        self.battery80Pixmap = QPixmap.fromImage(QImage('battery_80.png'))
        self.battery60Pixmap = QPixmap.fromImage(QImage('battery_60.png'))
        self.battery40Pixmap = QPixmap.fromImage(QImage('battery_40.png'))
        self.battery20Pixmap = QPixmap.fromImage(QImage('battery_20.png'))
        self.battery0Pixmap = QPixmap.fromImage(QImage('battery_0.png'))

        # Labels
        self.batteryLabel = QLabel()
        self.batteryLabel.setFixedSize(120, 41)
        self.batteryLabel.setGeometry(625,30,0,0)

        self.warningLabel = QLabel()
        self.warningLabel.setFixedSize(129,66)
        self.warningLabel.setGeometry(639,200,0,0)
        self.warningLabel.setPixmap(self.warningPlaceholderPixmap)

        self.emptyLabel = QLabel()
        self.emptyLabel.setFixedSize(209, 219)
        self.emptyLabel.setGeometry(100,110,0,0)
        self.emptyLabel.setStyleSheet("background:transparent")

        # Shapes & Lines
        backgroundRectangle = QGraphicsRectItem(600, 0, 170, 442)
        backgroundRectangle.setBrush(QBrush(QColor(47, 47, 125)))

        # TextItems
        self.lengthTextItem = QGraphicsTextItem("")
        self.lengthTextItem.setFont(font2)
        self.lengthTextItem.setPos(600, 300)
        self.lengthTextItem.setDefaultTextColor(Qt.white)
        self.lengthUnitTextItem = QGraphicsTextItem("cm")
        self.lengthUnitTextItem.setFont(font)
        self.lengthUnitTextItem.setPos(600 + 60, 380)
        self.lengthUnitTextItem.setDefaultTextColor(Qt.white)
        self.batteryTextItem = QGraphicsTextItem("100%")
        self.batteryTextItem.setFont(font)
        self.batteryTextItem.setDefaultTextColor(Qt.white)
        self.batteryTextItem.setPos(630 + 20, 75)

        self.counterSignal.connect(self.batteryTextItem.setPlainText)
        # self.distanceSignal.connect(self.lengthTextItem.setPlaintext)
        threading.Thread(target=self.batteryManageThread).start()
        threading.Thread(target=self.inputHandlerThread).start()
        self.distanceSignal.connect(self.lengthTextItem.setPlainText)
        threading.Thread(target=self.distanceThread).start()

        # Add all widgets - THE ORDER OF THE ADDWIDGETS DECIDES WHICH WIDGETS APPEAR ON THE FOREGROUND
        layout.addWidget(self.view)
        self.scene.addWidget(self.label)
        self.scene.addItem(backgroundRectangle)
        self.scene.addItem(self.lengthTextItem)
        self.scene.addItem(self.batteryTextItem)
        self.scene.addItem(self.lengthUnitTextItem)
        self.scene.addWidget(self.batteryLabel)
        self.scene.addWidget(self.warningLabel)
        self.scene.addWidget(self.emptyLabel)
        #self.happyMeasurePixmapItem = self.scene.addPixmap(
        #    happyMeasurePixmap).setPos(600+38, 327)
        #self.create4CarePixmapItem = self.scene.addPixmap(
        #    create4CarePixmap).setPos(600+38, 406)
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

    def batteryManageThread(self):
     #   eightVal = GPIO.input(8)
     #   tenVal = GPIO.input(10)
     #   nineVal = GPIO.input(9)
     #   elevenVal = GPIO.input(11)
      while True:
        pinValues = [GPIO.input(8), GPIO.input(10), GPIO.input(9), GPIO.input(11)]
        if (pinValues == [GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW]):
          self.batteryLabel.setPixmap(self.battery0Pixmap)
          self.counterSignal.emit("0%")
        elif (pinValues == [GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.HIGH]):
          self.batteryLabel.setPixmap(self.battery20Pixmap)
          self.counterSignal.emit("5%")
        elif (pinValues == [GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.LOW]):
          self.emptyLabel.setPixmap(self.batteryEmptyPixmap)
          self.batteryLabel.setPixmap(self.battery20Pixmap)
          self.counterSignal.emit("10%")
        elif (pinValues == [GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH]):
          self.emptyLabel.setPixmap("")
          self.batteryLabel.setPixmap(self.battery20Pixmap)
          self.counterSignal.emit("15%")
        elif (pinValues == [GPIO.LOW, GPIO.HIGH, GPIO.LOW, GPIO.LOW]):
          self.warningLabel.setPixmap(self.warningPixmap)
          self.batteryLabel.setPixmap(self.battery20Pixmap)
          self.counterSignal.emit("20%")
        elif (pinValues == [GPIO.LOW, GPIO.HIGH, GPIO.LOW, GPIO.HIGH]):
          self.warningLabel.setPixmap("")
          self.batteryLabel.setPixmap(self.battery40Pixmap)
          self.counterSignal.emit("25%")
        elif (pinValues == [GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW]):
          self.batteryLabel.setPixmap(self.battery40Pixmap)
          self.counterSignal.emit("30%")
        elif (pinValues == [GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.HIGH]):
          self.batteryLabel.setPixmap(self.battery40Pixmap)
          self.counterSignal.emit("40%")
        elif (pinValues == [GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.LOW]):
          self.batteryLabel.setPixmap(self.battery60Pixmap)
          self.counterSignal.emit("50%")
        elif (pinValues == [GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH]):
          self.batteryLabel.setPixmap(self.battery60Pixmap)
          self.counterSignal.emit("60%")
        elif (pinValues == [GPIO.HIGH, GPIO.LOW, GPIO.HIGH, GPIO.LOW]):
          self.batteryLabel.setPixmap(self.battery80Pixmap)
          self.counterSignal.emit("70%")
        elif (pinValues == [GPIO.HIGH, GPIO.LOW, GPIO.HIGH, GPIO.HIGH]):
          self.batteryLabel.setPixmap(self.battery80Pixmap)
          self.counterSignal.emit("80%")
        elif (pinValues == [GPIO.HIGH, GPIO.HIGH, GPIO.LOW, GPIO.LOW]):
          self.batteryLabel.setPixmap(self.battery100Pixmap)
          self.counterSignal.emit("90%")
        elif (pinValues == [GPIO.HIGH, GPIO.HIGH, GPIO.LOW, GPIO.HIGH]):
          self.batteryLabel.setPixmap(self.battery100Pixmap)
          self.counterSignal.emit("100%")
        else:
          self.counterSignal.emit("?")
        time.sleep(10)
        #self.batteryLabel.setPixmap(self.battery100Pixmap)

    def distanceThread(self):
        while True:
          schuifmaat = CDLL("./schuifmaat.so")
          schuifmaat.meassureDistance.restype = c_float
          distance = round(schuifmaat.meassureDistance(), 2)
          self.distanceSignal.emit(str(distance))
          time.sleep(2)

    def inputHandlerThread(self):
      screenEnabled = True
      while True:
        buttonHigh = GPIO.input(14)
        if (buttonHigh == 0):
          if(screenEnabled):
            GPIO.output(15, GPIO.LOW)
          else:
            GPIO.output(15, GPIO.HIGH)
          screenEnabled = (not screenEnabled)
          time.sleep(0.5)
        time.sleep(0.1)

    def stopCamera(self):
        '''Stops the camera.'''
        self.timer.stop()

    # https://stackoverflow.com/questions/41103148/capture-webcam-video-using-pyqt
    def nextFrameSlot(self):
        '''Reads the next frame from the OpenCV camera object and outputs it to a QPixmap.'''
        rval, frame = self.vc.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame,-1)
        image = QImage(frame, frame.shape[1],
                       frame.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)


def main():
    app = QApplication(sys.argv)
    ex = UI_Window()
    ex.show()
    ex.showFullScreen()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()