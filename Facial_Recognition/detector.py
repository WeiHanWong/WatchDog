import cv2
import numpy as np
import os 
import requests
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('model/facemodel.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
font = cv2.FONT_HERSHEY_SIMPLEX
id = 0
names = ['Nil', 'Will', 'John', "Admin"]
cam = cv2.VideoCapture(0)
cam.set(3, 1920)
cam.set(4, 1080)
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)
while True:
    ret, img =cam.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )
    for(x,y,w,h) in faces:
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        if (confidence < 100):
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
            
            url = 'http://X/api/cameracapture'
            myobj = {'id': id, 'camera': 1}
            x = requests.post(url, json = myobj)
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
        print(str(id) + " " + str(confidence))
    k = cv2.waitKey(10) & 0xff
    if k == 27:
        cam.release()
        exit(0)
