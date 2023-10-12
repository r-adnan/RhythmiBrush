# standard lib imports
import sys
import os

# Third-party imports
import cv2 as cv
import numpy as np
import mediapipe as mp 
import time

# Taking Inspiration from Murtaza's HandTracking (Optimizing FPS so its not laggy)
# https://www.youtube.com/@murtazasworkshop
class handDetection():
    def __init__(self, mode=False, maxHands=2, modelComplexity=1,detectionCon=0.5, trackCon=0.5):
        self.mode = mode 
        self.maxHands = maxHands 
        self.modelComplexity = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon 

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.modelComplexity,
                                    self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

        self.tipIDs = [4, 8, 12, 16, 20]

    # Finds the hands and draws both the landmark nodes and connections 
    # if draw == True
    def findHands(self, frame, draw=True):
        imageRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)
        
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame, handLms, self.mpHands.HAND_CONNECTIONS)
        return frame
    
    # Returns a list of every landmark node location on the screen
    # If draw == True, then it also draws a circle on the specific landmark node you want
    def findPosition(self, frame, landmarkID=8, draw=True):
        self.lmList = []

        if self.results.multi_hand_landmarks:
            for handLMS in self.results.multi_hand_landmarks:
                # print(self.results.multi_hand_landmarks)
                # print(handLMS)
                for id, lm in enumerate(handLMS.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    self.lmList.append([id, cx, cy])
                    
                    if draw and id == landmarkID:
                        cv.circle(frame, (cx, cy), 10, (255, 0, 255), cv.FILLED)
            
                # lm = handLMS.landmark[landmarkID]
                # h, w, c = frame.shape
                # # print(int(lm.x * w), int(lm.y * h))
                # cx, cy = int(lm.x * w), int(lm.y * h)
                # self.lmList.append([id, cx, cy])
                # cv.circle(frame, (cx, cy), 10, (255, 0, 255), cv.FILLED)
            
        return self.lmList
    # HandTracker class method that returns a boolean arr size 5 of which fingers are up
    def fingersUp(self):
        fingers = [0,0,0,0,0]

        # Thumb
        if self.lmList[self.tipIDs[0]][1] < self.lmList[self.tipIDs[0] - 1][1]:
            fingers[0] = 1
        else:
            fingers[0] = 0

        # 4Fingers
        for id in range(1, 5):
            if self.lmList[self.tipIDs[id]][2] < self.lmList[self.tipIDs[id] - 2][2]:
                fingers[id] = 1
            else:
                fingers[id] = 0
        return fingers
    
# Just a tester function
def main():
    pTime = 0
    cTime = 0
    cap = cv.VideoCapture(0)
    
    detector = handDetection()

    while True:
        ret, frame = cap.read()
        frame = cv.flip(frame, 1)
        frame = detector.findHands(frame)

        lmList = detector.findPosition(frame, draw=False)

        if lmList:
            print(lmList)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv.putText(frame, str(int(fps)), (10, 70),0, 2, 
                                                    (0, 255, 0), 3)

        cv.imshow("capTest", frame)
        if cv.waitKey(1) == ord('q'):
            break


if __name__ == "__main__":
    main()