import cv2
import mediapipe as mp
import ctypes
import pyautogui


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if handDetector.noOfHands(self) == 1:


            if self.results.multi_hand_landmarks:
                for handLms in self.results.multi_hand_landmarks:
                    if draw:
                        self.mpDraw.draw_landmarks(img, handLms,
                                                   self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                cx, cy = lm.x, lm.y
                lmList.append([id, cx, cy])
        return lmList
    def noOfHands(self):
        if self.results.multi_hand_landmarks:
            return len(self.results.multi_hand_landmarks)
        return 0


def main():
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    user32 = ctypes.windll.user32
    ScreenX = user32.GetSystemMetrics(0)
    ScreenY = user32.GetSystemMetrics(1)
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if detector.noOfHands() == 1:
            if len(lmList) != 0:
                x, y = pyautogui.size()
                pyautogui.moveTo(x - ScreenX*lmList[8][1], ScreenY*lmList[8][2])
                if lmList[12][2] < lmList[7][2]:
                    pyautogui.mouseDown()
                # elif lmList[12][2] < lmList[7][2] & lmList[16][2] < lmList[7][2]:
                #     pyautogui.click(button = 'left')
                else:
                    pyautogui.mouseUp()
        else:
            hello = 1
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()