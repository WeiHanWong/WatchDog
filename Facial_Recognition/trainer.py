import cv2
import os
import numpy as np
from PIL import Image

def captureUser(face_id):
    print("\n Initializing face capture. Please ensure theres a good lighting. Look the camera and wait ...")
    count = 0
    while(True):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:   
            count += 1
            cv2.imwrite("dataset/User." + str(face_id) + '.' +  
                        str(count) + ".jpg", gray[y:y+h,x:x+w])
            print("Progress " + str(count) + "%", end='\r')
        if count >= 100:
            break
    print("\n Done Capture. Training ...")
    cam.release()

def tagging(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    ids = []
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L')
        img_numpy = np.array(PIL_img,'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)
        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)
    return faceSamples,ids
    
if __name__ == "__main__":
    cam = cv2.VideoCapture(0)
    cam.set(3, 1920)
    cam.set(4, 1080)
    detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    imagePath = 'dataset'
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    captureUser(input('\n Userid: '))
    faces,ids = tagging(imagePath)
    recognizer.train(faces, np.array(ids))
    recognizer.write('model/facemodel.yml')
    print("\n {0} faces trained. Exiting Program".format(len(np.unique(ids))))