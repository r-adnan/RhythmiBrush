# standard lib imports
import sys
import os

# Third-party imports
import cv2 as cv
import numpy as np
import mediapipe as mp 
import time

import HandTracker as ht

pTime = 0
cTime = 0
cap = cv.VideoCapture(0)

detector = ht.handDetection()

while True:
    ret, frame = cap.read()
    frame = cv.flip(frame, 1)
    frame = detector.findHands(frame)

    lmList = detector.findPosition(frame, 8)

    if lmList:
        # print(lmList)
        print(detector.fingersUp())

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv.putText(frame, str(int(fps)), (10, 70),0, 2, 
                                                (0, 255, 0), 3)

    cv.imshow("capTest", frame)
    if cv.waitKey(1) == ord('q'):
        break