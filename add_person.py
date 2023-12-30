import cv2
import os
from users import load_names_from_file, save_names_to_file
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QTextEdit

DATASET_PATH = "assets/dataset"
CASCADE_PATH = 'assets/cascades/haarcascade_frontalface_default.xml'
NAMES = load_names_from_file('assets/names/names.json')

class AddUser(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.label = QLabel("Please enter your name then press ok and look at the camera for 10 seconds\nProgram will restart", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(0, 0, 500, 150)

        self.ok_button = QPushButton("Ok", self)
        self.ok_button.clicked.connect(self.add_user_button_click)
        self.ok_button.setGeometry(225, 115, 50, 25)

        self.name_edit = QTextEdit(self)
        self.name_edit.setGeometry(150, 25, 200, 35)
        self.name_edit.setPlaceholderText("Name")
        

    def add_user_button_click(self, _=None):
        if not os.path.exists(DATASET_PATH):
            os.makedirs(DATASET_PATH)

        cam = cv2.VideoCapture(0)
        cam.set(3, 640) # set video width
        cam.set(4, 480) # set video height

        face_detector = cv2.CascadeClassifier(CASCADE_PATH)
       
        face_id = len(NAMES)
        face_name = self.name_edit.toPlainText()
        save_names_to_file(face_id, face_name)

        # Initialize individual sampling face count
        count = 0
        while(True):
            ret, img = cam.read()
            img = cv2.flip(img, 1) # Mirror flip video image 
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)

            for (x,y,w,h) in faces:
                cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
                count += 1

                # Save the captured image into the datasets folder
                cv2.imwrite("assets/dataset/user." + str(face_id) + '.' +  
                            str(count) + ".jpg", gray[y:y+h,x:x+w])
                cv2.imshow('image', img)
            
            if count >= 30: # Take 30 face sample and stop video
                break

        # Cleanup
        cam.release()
        cv2.destroyAllWindows()
        self.accept()