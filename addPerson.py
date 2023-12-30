import cv2
import os
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton

DATASET_PATH = "assets/Dataset"
CASCADE_PATH = 'assets/Cascades/haarcascade_frontalface_default.xml'

class AddUser(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.label = QLabel("Look at the camera and press ok", self)

        self.ok_button = QPushButton("Ok", self)
        self.ok_button.clicked.connect(self.add_user_button_click)
        

    def add_user_button_click():
        # Check if the dataset directory exists, if not, create it
        if not os.path.exists(DATASET_PATH):
            os.makedirs(DATASET_PATH)

        cam = cv2.VideoCapture(0)
        cam.set(3, 640) # set video width
        cam.set(4, 480) # set video height

        face_detector = cv2.CascadeClassifier(CASCADE_PATH)
        # For each person, enter one numeric face id
        face_id = input('\n enter user id end press <return> ==>  ')
        print("\n [INFO] Initializing face capture. Look the camera and wait ...")

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
                cv2.imwrite("assets/Dataset/user." + str(face_id) + '.' +  
                            str(count) + ".jpg", gray[y:y+h,x:x+w])
                cv2.imshow('image', img)

            k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video

            if k == 27:
                break
            elif count >= 30: # Take 30 face sample and stop video
                break
            
        # Cleanup
        print("\n [INFO] Exiting Program")
        cam.release()
        cv2.destroyAllWindows()