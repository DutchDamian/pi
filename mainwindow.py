from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QPixmap, QImage, QPainter, QPen, QBrush, QFont
import sys
import cv2
import threading
import time
import os

class UI_Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        screenWidth = 800
        screenHeight = 480

        # QTimer uses QFrameSlots wherein every video frame from the live preview is encoded.
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)

        scene = QGraphicsScene()
        self.view = QGraphicsView(scene, self)
        layout = QVBoxLayout(self)

        self.openCamera()

        self.label = QLabel()
        self.label.setFixedSize(screenWidth, screenHeight)
        pen = QPen() # QPen is used to change the properties of the middle line drawn in the GUI.
        pen.setWidth(20)
        pen.setColor(Qt.green)
        font = QFont() # QFont is used to change the properties of the text rendered in the GUI.
        font.setPointSize(20) 
        layout.addWidget(self.view)
        scene.addWidget(self.label)
        batteryPixmap = QPixmap.fromImage(QImage('battery_100.png').scaled(40,40))
        rulerPixmap = QPixmap.fromImage(QImage('ruler.png').scaled(40,40))
        self.lineItem = scene.addLine(400,0,400,480, pen)
        self.lengthTextItem = scene.addText("50,1 cm (PLACEHOLDER)", font).setPos(40,90)
        self.rulerPixmapItem = scene.addPixmap(rulerPixmap).setPos(0,90)
        self.batteryTextItem = scene.addText("100% (PLACEHOLDER)", font).setPos(40,40)
        self.batteryPixmapItem = scene.addPixmap(batteryPixmap).setPos(0,40)

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

        self.timer.start(1000./24)
    
    def stopCamera(self):
        '''Stops the camera.'''
        self.timer.stop()

    # https://stackoverflow.com/questions/41103148/capture-webcam-video-using-pyqt
    def nextFrameSlot(self):
        '''Reads the next frame from the OpenCV camera object and outputs it to a QPixmap.'''
        rval, frame = self.vc.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)    
            
def main():
    app = QApplication(sys.argv)
    ex = UI_Window()
    ex.show()
    ex.showMaximized()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()