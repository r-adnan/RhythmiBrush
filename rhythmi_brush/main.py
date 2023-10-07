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


def videoCap():
    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        # We should capture frame-by-frame footage
        ret, frame = cap.read()
        if not ret:
            print("Can't recieve frame, Exiting...")
            break

        cv.imshow('videoCap', frame)
        
        if cv.waitKey(1) == ord('q'):
            break
        
    cap.release()
    cv.destroyAllWindows()

def main():
    # print("Hello")
    videoCap()




if __name__ == "__main__":
    main()
