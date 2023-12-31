import sys
import cv2
import os
import subprocess
import numpy as np
from users import load_names_from_file
from trainer import train_model
from add_person import AddUser
from PySide6.QtCore import QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QTableWidget, QTableWidgetItem, QApplication


CAMERA_WIDTH = 1024
CAMERA_HEIGHT = 576
CAMERA_FPS = 30
TRAINER_PATH = 'assets/trainer/trainer.yml'
CASCADE_PATH = 'assets/cascades/haarcascade_frontalface_default.xml'
NAMES = load_names_from_file('assets/names/names.json')
DATASET_PATH = 'assets/dataset'

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Camera Feed")
        self.initUI()
        self.initCamera()
        self.startCameraFeed()
    
    def initUI(self):
        # Create QLabel to hold everything
        self.background = QLabel(self)
        self.background.setGeometry(0, 0, 1920, 1080)

        # Create a QLabel to display the camera feed
        self.label = QLabel(self)
        self.label.setGeometry(0, 150, 1280, 720)
        
        # Create quit button
        self.quitbutton = QPushButton('Quit', self.background)
        self.quitbutton.setGeometry(1750, 40, 150, 50)
        self.quitbutton.clicked.connect(self.quit_app)

        # Create add user button
        self.add_user_button = QPushButton('Add User', self)
        self.add_user_button.setGeometry(1750, 100, 150, 50)
        self.add_user_button.clicked.connect(self.add_user_button_clicked)

        # Table
        self.table = QTableWidget(self)
        self.table.setRowCount(len(NAMES))
        self.table.setColumnCount(1)
        self.table.setHorizontalHeaderLabels(["Known Users"])
        self.table.setGeometry(1400, 150, 450, 720)
        self.table.setStyleSheet("font-size: 20px;")
        self.table.setColumnWidth(0, 450)
        # Test setting data
        for row, (num, name) in enumerate(NAMES.items()):
            set_name = QTableWidgetItem(name)
            self.table.setItem(row, 0, set_name) # Need to make this scalable

    def startCameraFeed(self):
        # Create a timer to continuously update the camera feed
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_camera_feed)
        self.timer.start(30)  # In milliseconds 

    def initCamera(self):
        # Open the camera
        self.capture = cv2.VideoCapture(0)
        
        # Set the camera's resolution
        self.capture.set(3, CAMERA_WIDTH)  # 3 corresponds to width
        self.capture.set(4, CAMERA_HEIGHT)  # 4 corresponds to height

    def update_label_text(self, text):
        self.textlabel.setText(text)

    def update_camera_feed(self):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(TRAINER_PATH)
        faceCascade = cv2.CascadeClassifier(CASCADE_PATH)
        font = cv2.FONT_HERSHEY_SIMPLEX

        # Load classifier for face detection
        faceCascade = cv2.CascadeClassifier(CASCADE_PATH)

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
                    id = NAMES[str(id)]
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

    def add_user_button_clicked(self):
        self.capture.release()
        self.add_user_dialog = AddUser()
        self.add_user_dialog.exec()

        train_model(DATASET_PATH)
        self.restart_app()
        
    def quit_app(self):
        sys.exit()

    def restart_app(self):
        QApplication.quit() 
        subprocess.Popen([sys.executable, 'main.py'])
    

