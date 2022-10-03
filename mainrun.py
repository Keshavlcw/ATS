import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import temp

path = 'apt'
images = []
names = []
mylist = os.listdir(path)
print(mylist)
for cl in mylist:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    names.append(os.path.splitext(cl)[0])
print(names)

def FindEncodings(images):
    encodelist = []
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist

def Attendance(name):
    with open('data.csv', 'r+') as f:
        mydatalist = f.readlines()
        nameslist = []
        for line in mydatalist:
            entry = line.split(',')
            nameslist.append(entry[0])
        temps = temp.temp
        if name not in nameslist:
            now = datetime.now()
            dtstring = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtstring},{temps}')


encodelistknown = FindEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)


    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodelistknown,encodeFace)
        faceDis = face_recognition.face_distance(encodelistknown,encodeFace)
        #print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = names[matchIndex].upper()
            #print(name)
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img, (x1, y1-35), (x2, y2), (0, 255, 0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,255),1)
            Attendance(name)


    cv2.imshow('Webcam',img)
    cv2.waitKey(1)

