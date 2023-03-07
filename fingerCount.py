import cv2
import time
import os
import handLMmodule as htm

###############################
wCam, hCam = 640, 480
################################

detector = htm.handDetector(detectionCon=0.75)
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
ptime = 0
folderPath = 'D:\opencv\main/fingerCountProject\FingerImages'
myList = os.listdir(folderPath)
print(myList)
overlayList = []
tipIds = [4, 8, 12, 16, 20]

for imPath in myList:
    img = cv2.imread(f'{folderPath}/{imPath}')
    print(img.shape)
    # print(f'{folderPath}/{imPath}')
    overlayList.append(img)

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)
    # print(lmlist)

    if len(lmlist) !=0:
        fingers = []
        #  for thumb
        if lmlist[tipIds[0]][1] > lmlist [tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # for fingers
        for id in range(1, 5):
            if lmlist [tipIds[id]][2] < lmlist [tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # print(fingers)
        totalFingers = fingers.count(1)
        print(totalFingers)
                

    
        h, w, c  = overlayList[totalFingers-1].shape
        img[0:h, 0:w] = overlayList[totalFingers-1]
        
        cv2.rectangle(img, (20, 255), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45,375), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0),25)


    ctime = time.time()
    fps = 1 / (ctime-ptime)
    ptime = ctime
    
    cv2.putText(img, f'fps{int(fps)}', (400, 30), 2, cv2.FONT_HERSHEY_PLAIN, (0, 255, 0), 2)
    cv2.imshow('image', img)
    cv2.waitKey(1)