import numpy as np
from PIL import ImageGrab
from collections import deque
from networktables import NetworkTables
import cv2
import time
import imutils
import argparse
import cv2 as CV

x = 0
y = 0

NetworkTables.initialize(server='roborio-8501-frc.local')

table = NetworkTables.getTable("Vision")

colorLower = (0, 180, 90)
colorUpper = (255, 255, 255)

def screen_record():
    x = 0
    y = 0
    r = 0
    last_time = time.time()
    while(True):
        printscreen =  np.array(ImageGrab.grab(bbox=(0,40,1024,768)))
        print('Tekrarlanma süresi : {} saniye'.format(time.time()-last_time))
        last_time = time.time()

        frame = cv2.imread('example.jpg')
        frame = imutils.resize(frame, width=600)
        frame = imutils.rotate(frame, angle=0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, colorLower, colorUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
        else:
            x = 0
            y = 0
        print("x : ")
        print(x)
        print("y : ")
        print(y)
        table.putNumber("X", x)
        table.putNumber("Y", y)

        cv2.imshow('frame', frame)
        cv2.waitKey(1)
screen_record()