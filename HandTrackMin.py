import cv2
import mediapipe as mp
from pynput.mouse import Button, Controller
import time
import math

def seperation(x1,y1,x2,y2) :
    x = math.pow((x2-x1),2)
    y = math.pow((y2-y1),2)
    return int(math.sqrt((x+y)))

cap  = cv2.VideoCapture(1)      #0 for Internal, 1 for External

mouse = Controller()            #Mouse ka setup
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                #print(id, cx, cy)
                if id == 8: # https://google.github.io/mediapipe/images/mobile/hand_landmarks.png
                    cx = int((cx/650)*3500)     #cx max -> 650, cy max -> 460
                    cy = int((cy/450)*2000)     #Target was 1920*1080 but nobody realistically goes to the edges
                    print(cx, cy)
                    mouse.position = (cx, cy)



            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)