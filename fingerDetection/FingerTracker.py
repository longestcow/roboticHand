import math

import cv2
import mediapipe as mp
import serial
import schedule


MIN_DISTANCE = 50
prevs = ""
distances = []


# https://colab.research.google.com/github/googlesamples/mediapipe/blob/main/examples/hand_landmarker/python/hand_landmarker.ipynb
class handDetector():
    def __init__(self, detCon=0.5, trackCon=0.5):
        self.detCon = detCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(False, 1, 1, self.detCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHand(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)
        landmarks = []
        dists = []
        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]

            self.mpDraw.draw_landmarks(img, hand, self.mpHands.HAND_CONNECTIONS,  # drawing onto image
                                       self.mpDraw.DrawingSpec(color=(0, 10, 200), thickness=2, circle_radius=4),
                                       self.mpDraw.DrawingSpec(color=(23, 23, 23), thickness=4))

            for id, lm in enumerate(hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmarks.append([cx, cy])

                if id == 8 or id == 12 or id == 16 or id == 20:
                    ocx, ocy = landmarks[id-3]
                    dist1 = math.hypot(ocx - cx, ocy - cy) < MIN_DISTANCE
                    ocx, ocy = landmarks[id-1]
                    dist2 = math.hypot(ocx - cx, ocy - cy) < MIN_DISTANCE/4
                    dists.append(dist1 or dist2)

                if id == 20:
                    cx, cy = landmarks[0]
                    for i in range(1, 5):
                        ocx, ocy = landmarks[i]
                        if math.hypot(ocx - cx, ocy - cy) < MIN_DISTANCE:
                            dists.insert(0, True)
                            break
                    else:
                        dists.insert(0, False)

        return dists


def sendData(ard):
    global prevs
    if not distances:
        return
    s = ''.join(['1' if value else '0' for value in distances])
    if s == prevs:
        return

    ard.write((s+'\n').encode())
    prevs = s


if __name__ == "__main__":

    video = cv2.VideoCapture(0)
    video.set(3, 1280)
    video.set(4, 720)

    handDetector = handDetector()

    arduino = serial.Serial('COM3', 9600)
    schedule.every(1).seconds.do(sendData,  arduino)

    while True:
        schedule.run_pending()

        success, img = video.read()
        distances = handDetector.findHand(img)

        cv2.imshow('omb', cv2.flip(img, 1))
        cv2.waitKey(1)

        if cv2.getWindowProperty('omb', cv2.WND_PROP_VISIBLE) < 1:
            break

    cv2.destroyAllWindows()
