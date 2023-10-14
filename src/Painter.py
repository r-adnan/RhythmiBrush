
'''
    RhythmiBrush - dynamic airbrush that changes based on music
'''
import cv2 as cv
import numpy as np
import time
import os
import soundcard as sc

from . import HandTracker as ht
from . import spotipyModule as spm

from . import BrushModule as bt

from . api_keys import clientID
from . api_keys import clientSecret
from . api_keys import redirectURI

from . mic import input_mic

cap = cv.VideoCapture(0)

cap.set(3, 1280)
cap.set(4, 720)
detector =  ht.handDetection()
fingers = [0,0,0,0,0]
success, frame = cap.read()
imageCanvas = np.zeros_like(frame)
px, py = 0, 0

sptmModule = spm.spotipyModule( clientID,
                                clientSecret,
                                redirectURI,
                                "user-read-playback-state,user-modify-playback-state")

last_update_time = time.time()

update_interval = 5
brush = bt.Brush((255, 0, 0), 10)
brush_color = None


# Define chunk size
loopback = [mic for mic in sc.all_microphones(include_loopback=True) if input_mic in mic.name.lower()][0]
CHUNK_SIZE = 1024

with loopback.recorder(samplerate=44100) as mic:
    while True:
        success, frame = cap.read()
        
        current_time = time.time()

        data = mic.record(numframes=CHUNK_SIZE)
        rms = np.sqrt(np.mean(data**2))

        if current_time - last_update_time > update_interval:
            sptmModule.updateCurrentSong()
            last_update_time = current_time
        frame = cv.flip(frame, 1)
        
        # 2 Find Hand Landmarks
        frame = detector.findHands(frame)
        lmList = detector.findPosition(frame)
        
        currSongFeatures = sptmModule.getCurrentSongFeatures()
        if currSongFeatures.empty:
            cv.putText(frame, "No song is currently playing.", (30, 50), cv.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 0), 3)
            cv.putText(frame, "No song is currently playing.", (30, 50), cv.FONT_HERSHEY_TRIPLEX, 1, (255, 255, 255), 1)
            cv.imshow("paintDriver", frame)
            if cv.waitKey(1) == ord('q'):
                break
            continue
        
        songDetails = sptmModule.getSongDetails()
        text = f"Now playing {songDetails['item']['name']} from {songDetails['item']['album']['name']} by {songDetails['item']['album']['artists'][0]['name']}"
        cv.putText(frame, text, (30, 50), cv.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 0), 3)
        cv.putText(frame, text, (30, 50), cv.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 1)
        

        brush_color = (int(currSongFeatures['danceability'] * 255 * .5 - int(rms * 1000)*3), 
                    int(currSongFeatures['tempo'] % 255 ) - int(rms * 1000)*2 , 
                    min(int(currSongFeatures['acousticness'] * 255 *4) + int(rms * 1000)*5, 255)
                    )

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
            brush.set_target_color(brush_color)
            brush.update()
            if px == 0 and py == 0:
                px, py = xPointer, yPointer
            
            cv.line(imageCanvas, (px, py), (xPointer, yPointer), brush.color, int(rms * 1000) + 1)
            px, py = xPointer, yPointer
            
        # 5 if Erase mode - 2 fingers up
        elif fingers[1] and fingers[2] and not (fingers[3] or 
                                            fingers[4] or fingers[0]):
            px, py = 0, 0
            # print(np.around(np.sqrt((xPointer - xMiddle)**2 + (yPointer - yMiddle)**2)))
            val = int(np.round(np.sqrt((xMiddle- xPointer)**2 + (yMiddle - yPointer)**2))/1.5)
            rad = max(val, 0)
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

        # Inversely, we could also do this:
        # frame = cv.addWeighted(frame, 1, imageCanvas, 1, 1)
        # However, it will make the actual drawing a bit opaque
        imageGray = cv.cvtColor(imageCanvas, cv.COLOR_BGR2GRAY)
        _, imageInv = cv.threshold(imageGray, 50, 255, cv.THRESH_BINARY_INV)
        ImageInv = cv.cvtColor(imageInv, cv.COLOR_GRAY2BGR)
        frame = cv.bitwise_and(frame, ImageInv)
        frame = cv.bitwise_or(frame, imageCanvas) 
        cv.imshow("paintDriver", frame)

        # cv.imshow("Canvas", imageCanvas)
        if cv.waitKey(1) == ord('q'):
                break

