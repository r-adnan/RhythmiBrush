# standard lib imports
import sys
import os

# Third-party imports
import cv2
import numpy as np
import mediapipe as mp 
import time

# Taking Inspiration from Murtaza's HandTracking (Optimizing FPS so its not laggy)
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


    def findHands(self, frame, draw=True):
        imageRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imageRGB)
        
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame, handLms, self.mpHands.HAND_CONNECTIONS)
        return frame
def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    
    detect = handDetection()

    while True:
        ret, frame = cap.read()
        frame = detect.findHands(frame)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, 
                                                            (255, 0, 255), 3)
        
        cv2.imshow("capTest", frame)
        if cv2.waitKey(1) == ord('q'):
            break

# def videoCap():
#     cap = cv.VideoCapture(0)

#     cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
#     cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
#     mpHands = mp.solutions.hands
#     hands = mpHands.Hands() 
#     mpDraw = mp.solutions.drawing_utils 

#     if not cap.isOpened():
#         print("Cannot open camera")
#         exit()

#     px, py = 0, 0

#     ret, frame = cap.read()
#     frame = cv.flip(frame, 1)
#     canvas = np.zeros_like(frame)

#     while True:
#         # We should capture frame-by-frame footage
#         ret, frame = cap.read()
#         frame = cv.flip(frame, 1)
#         if not ret:
#             print("Can't recieve frame, Exiting...")
#             break
        
#         imageRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
#         results = hands.process(imageRGB)
        
#         if results.multi_hand_landmarks:
#             for handLms in results.multi_hand_landmarks:
#                 for id, lm in enumerate(handLms.landmark):
#                     h, w, c = frame.shape
#                     cx, cy = int(lm.x * w), int(lm.y * h)
#                     if id == 8:
#                         if px == 0 and py == 0:
#                             px, py = cx, cy
#                         cv.line(canvas, (cx,cy), (px, py), (255, 0, 0), 10)
#                         frame = cv.addWeighted(frame, 1, canvas, 0.5, 0)
#                         px, py = cx, cy
#                         # mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)

#         cv.imshow('HandCap', frame)
#         if cv.waitKey(1) == ord('q'):
#             break
        
#     cap.release()
#     cv.destroyAllWindows()

if __name__ == "__main__":
    main()