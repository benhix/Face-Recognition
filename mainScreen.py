import sys
import cv2
import numpy as np
import os
from PySide6.QtCore import Qt, QTimer, Slot, Signal
from PySide6.QtGui import QImage, QPixmap, QPainter 
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QFrame


 # Names related to ids
# Make it read from file (todo)
names = ['None']

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set window properties
        self.setWindowTitle("Camera Feed")

        # Create QLabel to hold everything
        self.background = QLabel(self)
        self.background.setGeometry(0, 0, 1920, 1080)
        self.bg = QPixmap('black.jpg')
        self.background.setPixmap(self.bg)

        # Create a QLabel to display the camera feed
        self.label = QLabel(self)
        self.label.setGeometry(0, 150, 1280, 720)
        
        # Create quit button
        self.quitbutton = QPushButton('Quit', self.background)
        self.quitbutton.setGeometry(1750, 40, 150, 50)
        self.quitbutton.clicked.connect(self.quit_app)
        
        # Open the camera
        self.capture = cv2.VideoCapture(0)
        
        # Set the camera's resolution
        self.capture.set(3, 1024)  # 3 corresponds to width
        self.capture.set(4, 576)  # 4 corresponds to height
        
        # Create a timer to continuously update the camera feed
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_camera_feed)
        self.timer.start(30)  # In milliseconds
        
        # Create a frame with a border
        frame = QFrame(self)
        frame.setFrameShape(QFrame.Box)  # You can use QFrame.Box for a solid border
        frame.setFrameShadow(QFrame.Sunken)
        frame.setGeometry(1400, 150, 450, 720)
        
        # Text Label
        self.textlabel = QLabel(frame)
        self.textlabel.setGeometry(50, 0, 450, 720)
        self.textlabel.setStyleSheet("color: white")
        self.update_label_text("Event Log:  Coming Soon")

    def update_label_text(self, text):
        self.textlabel.setText(text)
 

    def update_camera_feed(self):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('assets/Trainer/trainer.yml')
        cascadePath = "assets/Cascades/haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascadePath)
        font = cv2.FONT_HERSHEY_SIMPLEX
        # Load classifier for face detection
        faceCascade = cv2.CascadeClassifier('assets/Cascades/haarcascade_frontalface_default.xml')
        # Initiate id counter
        id = 0

       

        # Take frame capture 
        ret, frame = self.capture.read()

        if ret:
            # Mirror flip camera
            frame = cv2.flip(frame, 1)
            # Convert from BGR to gray for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,     
                scaleFactor=1.2,
                minNeighbors=5,     
                minSize=(20, 20)
            )

            for(x,y,w,h) in faces:
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
                id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
                
                # If confidence is less them 100 ==> "0" : perfect match 
                if (confidence < 90 ):
                    id = names[id]
                    confidence = "  {0}%".format(round(100 - confidence))
                else:
                    id = "Unknown"
                    confidence = "  "
                
                cv2.putText(frame, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
                cv2.putText(frame, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
                    
            # Convert the OpenCV frame from BGR to RGB format
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert the OpenCV frame to a QImage for displaying in PySide6
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            qt_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)

            # Convert the QImage to a QPixmap
            frame_pixmap = QPixmap.fromImage(qt_image)

            # Update Pixmap on QLabel
            self.label.setPixmap(frame_pixmap)

    def closeEvent(self, event):
        self.capture.release()
        event.accept()
    
    def update_label(self, frame_pixmap):
        # Update the QLabel with the frame
        self.label.setPixmap(frame_pixmap)

    def quit_app(self):
        sys.exit()

