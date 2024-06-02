import cv2
import time
import HandTrackingSupport as hts

video = cv2.VideoCapture(0)
video.set(3, 640); video.set(4, 480)
handDetector = hts.handDetector()

while True:
    success, img = video.read()
    img = handDetector.findHands(img)
    cv2.imshow('mmmbmm,,, ,,', cv2.flip(img,1))
    cv2.waitKey(1)



