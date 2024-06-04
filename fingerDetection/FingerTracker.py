import cv2
import mediapipe as mp
import serial

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
        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            
            self.mpDraw.draw_landmarks(img, hand, self.mpHands.HAND_CONNECTIONS,  # drawing onto image
               self.mpDraw.DrawingSpec(color=(0, 10, 200), thickness=2, circle_radius=4),
               self.mpDraw.DrawingSpec(color=(23, 23, 23), thickness=4))
            

            for id, lm in enumerate(hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                print(id, cx, cy)
                landmarks.append([id, cx, cy])

        return img


if __name__ == "__main__":
    video = cv2.VideoCapture(0)
    video.set(3, 1280)
    video.set(4, 720)
    handDetector = handDetector()
    arduino = serial.Serial('COM11', 9600)
    arduino.write('aaaa;'.encode())
    while True:    
        success, img = video.read()
        handDetector.findHand(img)
        cv2.imshow('mmmbmm,,, ,,', cv2.flip(img, 1))
        cv2.waitKey(1)
