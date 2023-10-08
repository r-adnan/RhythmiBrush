#!/usr/bin/env python3

'''
    RhythmiBrush - dynamic airbrush that changes based on music
'''
import cv2 as cv
import numpy as np
import time
import os

import HandTracker as ht
import spotipyModule as spm


cap = cv.VideoCapture(0)

cap.set(3, 1280)
cap.set(4, 720)
detector =  ht.handDetection()
fingers = [0,0,0,0,0]
success, frame = cap.read()
imageCanvas = np.zeros_like(frame)
px, py = 0, 0

sptmModule = spm.spotipyModule("362dc80475a04994834c34e8e9407efa",
                                "e30e2844a83742fd9fd217ae9a8418f7",
                                "http://localhost:8888/callback",
                                "user-read-playback-state,user-modify-playback-state")
while True:
    success, frame = cap.read()
    
    frame = cv.flip(frame, 1)
    
    # 2 Find Hand Landmarks
    frame = detector.findHands(frame, draw=False)
    lmList = detector.findPosition(frame, draw=False)
    
    
    currSongFeatures = sptmModule.getStats()
    normalized_loudness = (currSongFeatures['loudness'] + 60) / 60
    brush_size = int(currSongFeatures['energy'] * 20 + normalized_loudness * 10)
    brush_color = (int(currSongFeatures['danceability'] * 255), 
                   int(currSongFeatures['tempo'] % 255), 
                   int(currSongFeatures['acousticness'] * 255))

    if lmList:
        # print(lmList)
        xPointer, yPointer = lmList[8][1:]
        xMiddle, yMiddle = lmList[12][1:] 
        # print(lmList[8][1:], lmList[12][1:])

        # 3. Check which fingers ure up
        fingers = detector.fingersUp()
        # print(fingers)
    # 4 If Drawing mode - Index finger up
    if fingers[1] and not (fingers[0] or fingers[2] 
                        or fingers[3] or fingers[4]):
        print("Drawing Mode :nerd emoji:")
        if px == 0 and py == 0:
            px, py = xPointer, yPointer
        
        
        cv.line(imageCanvas, (px, py), (xPointer, yPointer), brush_color, brush_size)
        px, py = xPointer, yPointer
        
    # 5 if Erase mode - 2 fingers up
    elif fingers[1] and fingers[2] and not (fingers[3] or 
                                         fingers[4] or fingers[0]):
        px, py = 0, 0
        # print(np.around(np.sqrt((xPointer - xMiddle)**2 + (yPointer - yMiddle)**2)))
        val = int(np.round(np.sqrt((xMiddle- xPointer)**2 + (yMiddle - yPointer)**2)))
        rad = max(val-20, 0)
        cv.circle(frame, ((xPointer + xMiddle)//2, (yPointer + yMiddle)//2),
                   rad, (0, 255, 0), 2)
        cv.circle(imageCanvas, ((xPointer + xMiddle)//2, (yPointer + yMiddle)//2),
                   rad, (0, 0, 0), -1)
        print("Erasing Mode")
    else:
        px, py = 0, 0
         

    # frame = cv.addWeighted(frame, 1, imageCanvas, 1, 1)

    # This huge block is just fancy bitwise and inverse color operations
    # To make the image and drawing Canvas overlayed
    imageGray = cv.cvtColor(imageCanvas, cv.COLOR_BGR2GRAY)
    _, imageInv = cv.threshold(imageGray, 50, 255, cv.THRESH_BINARY_INV)
    ImageInv = cv.cvtColor(imageInv, cv.COLOR_GRAY2BGR)
    frame = cv.bitwise_and(frame, ImageInv)
    frame = cv.bitwise_or(frame, imageCanvas) 
    cv.imshow("paintDriver", frame)

    # cv.imshow("Canvas", imageCanvas)
    if cv.waitKey(1) == ord('q'):
            break

