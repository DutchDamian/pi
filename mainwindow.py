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

        # create timer for video feed
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)

        scene = QGraphicsScene()
        self.view = QGraphicsView(scene, self)
        layout = QVBoxLayout(self)

        self.openCamera()

        self.label = QLabel()
        self.label.setFixedSize(800, 480)
        pen = QPen()
        font = QFont()
        font.setPointSize(20)
        pen.setWidth(5)
        pen.setColor(Qt.red)
        layout.addWidget(self.view)
        proxy = scene.addWidget(self.label)
        batteryPixmap = QPixmap.fromImage(QImage('battery_100.png').scaled(40,40))
        rulerPixmap = QPixmap.fromImage(QImage('ruler.png').scaled(40,40))
        self.lineItem = scene.addLine(400,0,400,480, pen)
        self.batteryTextItem = scene.addText("100%", font).setPos(40,40)
        self.lengthTextItem = scene.addText("50,12 cm", font).setPos(40,90)
        self.batteryPixmapItem = scene.addPixmap(batteryPixmap).setPos(0,40)
        self.rulerPixmapItem = scene.addPixmap(rulerPixmap).setPos(0,90)

        # Layout necessary?
        self.setLayout(layout)
        self.setWindowTitle("EEP71")

    '''def closeEvent(self, event):
    
        msg = "Are you sure?"
        reply = QMessageBox.question(self, 'Message', 
                        msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            self.stopCamera()
        else:
            event.ignore()'''

    def resizeImage(self, filename):
        pixmap = QPixmap(filename)
        lwidth = self.label.maximumWidth()
        pwidth = pixmap.width()
        lheight = self.label.maximumHeight()
        pheight = pixmap.height()

        wratio = pwidth * 1.0 / lwidth
        hratio = pheight * 1.0 / lheight

        if pwidth > lwidth or pheight > lheight:
            if wratio > hratio:
                lheight = pheight / wratio
            else:
                lwidth = pwidth / hratio

            scaled_pixmap = pixmap.scaled(lwidth, lheight)
            return scaled_pixmap
        else:
            return pixmap

    def openCamera(self):
        self.vc = cv2.VideoCapture(0)
        # vc.set(5, 30)  #set FPS
        print(self.geometry)
        self.vc.set(3, 800) #set width
        self.vc.set(4, 480) #set height

        if not self.vc.isOpened(): 
            msgBox = QMessageBox()
            msgBox.setText("Failed to open camera.")
            msgBox.exec_()
            return

        self.timer.start(1000./24)
    
    def stopCamera(self):
        self.timer.stop()

    # https://stackoverflow.com/questions/41103148/capture-webcam-video-using-pyqt
    def nextFrameSlot(self):
        rval, frame = self.vc.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        '''self.painterInstance = QPainter(pixmap)
        self.penRectangle = QPen(Qt.red)
        self.penRectangle.setWidth
        self.painterInstance.drawRect(0,0,200,200)'''
        self.label.setPixmap(pixmap)    
            
def main():
    app = QApplication(sys.argv)
    ex = UI_Window()
    ex.show()
    ex.showMaximized()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()