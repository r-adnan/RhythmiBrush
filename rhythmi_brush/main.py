#!/usr/bin/env python3

'''
    RhythmiBrush - dynamic airbrush that changes based on music
'''
# standard lib imports
import sys
import os

# Third-party imports
import cv2 as cv
import numpy as np
import mediapipe as mp 


def videoProcess():
    cap = cv.VideoCapture(0)

    mpHands = mp.solutions.hands
    hands = mpHands.Hands() 
    mpDraw = mp.solutions.drawing_utils 

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        # We should capture frame-by-frame footage
        ret, frame = cap.read()
        if not ret:
            print("Can't recieve frame, Exiting...")
            break
        
        imageRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = hands.process(imageRGB)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    if id == 8:
                        cv.circle (frame, (cx, cy), 25, (255, 0, 255), cv.FILLED)
                mpDraw.draw_landmarks (frame, handLms, mpHands.HAND_CONNECTIONS)

        cv.imshow('HandCap', frame)
        
        if cv.waitKey(1) == ord('q'):
            break
        
    cap.release()
    cv.destroyAllWindows()

def main():
    # print("Hello")
    videoProcess()




if __name__ == "__main__":
    main()
