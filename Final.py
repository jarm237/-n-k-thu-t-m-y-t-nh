# from typing import overload
import cv2
import numpy as np
import os
import HandTrackingModule as htm
# from playsound import playsound
# import pytesseract
# from datetime import datetime
import colorama
# from colorama import Fore, Back, Style
# colorama.init(autoreset=True)

RED = '\033[31m'
GREEN = '\033[32m'
#Size
brush = 15
eraser = 60
#Color
drawColor = (255, 0, 255) #Pink

#Background Folder
folderPath = "Pic"
myList = os.listdir(folderPath)
#print(myList)
count = 0
mode = 0
drawMode = 0
overlayList = []
#Save image in folderPath to overlayList
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
#print(len(overlayList))

#Setting background
header = overlayList[0]
footer = overlayList[4]

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#Width = 1280
cap.set(3, 1280)
#Height = 720 
cap.set(4, 720)

detector = htm.handDetector(detectionCon = 0.85)
#Previous position
x0, y0 = 0, 0

imgCanvas = np.zeros((720, 1280, 3), np.uint8)

while True:
    #Show camera
    success, img = cap.read()
    #Flip camera 
    img = cv2.flip(img, 1)
    cv2.imwrite('Fail/human.png', img)
    #Draw landmarks
    img = detector.findHands(img)
    lmList = detector.findPos(img, draw=False)

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)

    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)
    #img is camera
    #imgCanvas background black and color pink
    #imgInv background white and color black

    if len(lmList)!=0:
        #print(lmList)

        #Index finger
        x1, y1 = lmList[8][1:]
        #Middle finger
        x2, y2 = lmList[12][1:]

        #Checking finger (Up/Down)
        finger = detector.fingerUP()
        #print(finger)

        #Drawing Mode
        if finger[1]==True and finger[2]==False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            #print("Drawing Mode")
            if x0 == 0 and y0 == 0:
                x0, y0 = x1, y1
            #Draw & Eraser line in img:
            if mode and drawMode == 0:
                if mode == 2:
                    cv2.line(img, (x0, y0), (x1, y1), drawColor, eraser)
                    cv2.line(imgCanvas, (x0, y0), (x1, y1), drawColor, eraser)
                elif mode == 1:
                    cv2.line(img, (x0, y0), (x1, y1), drawColor, brush)
                    cv2.line(imgCanvas, (x0, y0), (x1, y1), drawColor, brush)
                x0, y0 = x1, y1

            #Draw mode
            if drawMode != 0:
                imgCanvas = np.zeros((720, 1280, 3), np.uint8)

                # Line
                if drawMode == 1:
                    cv2.line(img, (x0, y0), (x1, y1), drawColor, brush)
                    cv2.line(imgCanvas, (x0, y0), (x1, y1), drawColor, brush)

                # Triangle
                elif drawMode == 2:
                    pt1 = (int((x0 + x1)/2), y0)
                    pt2 = (x0, y1)
                    pt3 = (x1, y1)

                    cv2.line(img, pt1, pt2, drawColor, brush)
                    cv2.line(img, pt2, pt3, drawColor, brush)
                    cv2.line(img, pt3, pt1, drawColor, brush)
                    cv2.line(imgCanvas, pt1, pt2, drawColor, brush)
                    cv2.line(imgCanvas, pt2, pt3, drawColor, brush)
                    cv2.line(imgCanvas, pt3, pt1, drawColor, brush)

                # Rectangle
                elif drawMode == 3:
                    cv2.rectangle(img, (x0, y0), (x1, y1), drawColor, brush)
                    cv2.rectangle(imgCanvas, (x0, y0), (x1, y1), drawColor, brush)

                # Circle
                elif drawMode == 4:
                    if abs(x1 - x0) > abs(y1 - y0):
                        radius = int(abs(y1 - y0)/2)
                        if y1 > y0 and x1 > x0:
                            cv2.circle(img, ((x0 + radius), (y0 + radius)), radius, drawColor, brush)
                            cv2.circle(imgCanvas, ((x0 + radius), (y0 + radius)), radius, drawColor, brush)
                        elif y1 > y0 and x1 < x0:
                            cv2.circle(img, ((x1 + radius), (y0 + radius)), radius, drawColor, brush)
                            cv2.circle(imgCanvas, ((x1 + radius), (y0 + radius)), radius, drawColor, brush)
                        elif y1 < y0 and x1 > x0:
                            cv2.circle(img, ((x0 + radius), (y1 + radius)), radius, drawColor, brush)
                            cv2.circle(imgCanvas, ((x0 + radius), (y1 + radius)), radius, drawColor, brush)
                        else:
                            cv2.circle(img, ((x1 + radius), (y1 + radius)), radius, drawColor, brush)
                            cv2.circle(imgCanvas, ((x1 + radius), (y1 + radius)), radius, drawColor, brush)

                    else:
                        radius = int(abs(x1 - x0)/2)
                        if y1 > y0 and x1 > x0:
                            cv2.circle(img, ((x0 + radius), (y0 + radius)), radius, drawColor, brush)
                            cv2.circle(imgCanvas, ((x0 + radius), (y0 + radius)), radius, drawColor, brush)
                        elif y1 > y0 and x1 < x0:
                            cv2.circle(img, ((x1 + radius), (y0 + radius)), radius, drawColor, brush)
                            cv2.circle(imgCanvas, ((x1 + radius), (y0 + radius)), radius, drawColor, brush)
                        elif y1 < y0 and x1 > x0:
                            cv2.circle(img, ((x0 + radius), (y1 + radius)), radius, drawColor, brush)
                            cv2.circle(imgCanvas, ((x0 + radius), (y1 + radius)), radius, drawColor, brush)
                        else:
                            cv2.circle(img, ((x1 + radius), (y1 + radius)), radius, drawColor, brush)
                            cv2.circle(imgCanvas, ((x1 + radius), (y1 + radius)), radius, drawColor, brush)

            # x0, y0 = x1, y1

        # n = n + 1
        # print(n)

        #Selecting Mode
        if finger[1] and finger[2]:
            #print("Selection Mode")
            x0, y0 = 0, 0
            if 0 < y1 < 115: 
                if 237 < x1 < 352: 
                    header = overlayList[1]
                    drawColor = (255, 0, 255)
                    mode = 1

                elif 467 < x1 < 582: 
                    header = overlayList[2]
                    drawColor = (0, 0, 0)   
                    mode = 2 

                elif 697 < x1 < 812: 
                    header = overlayList[3]
                    imgCanvas = cv2.bitwise_xor(imgCanvas, imgCanvas)
                    
                elif 927 < x1 < 1042: 
                    header = overlayList[0]
                    pw_r = 'Image/password_record.png'
                    img_r = 'Fail/fail_record.png'
                    cv2.imwrite(pw_r, imgInv)
                    break
                    #Export password screen to file png

            if mode == 1:
                img[605:720, 0:1280] = footer
                if 605 < y1 < 720:
                    if 237 < x1 < 352:
                        footer = overlayList[5]
                        drawColor = (255, 0, 255)
                        drawMode = 1  # Line

                    elif 467 < x1 < 582:
                        footer = overlayList[6]
                        drawColor = (255, 0, 255)
                        drawMode = 2  # Triangle

                    elif 697 < x1 < 812:
                        footer = overlayList[7]
                        drawColor = (255, 0, 255)
                        drawMode = 3  # Rectangle

                    elif 927 < x1 < 1042:
                        footer = overlayList[8]
                        drawColor = (255, 0, 255)
                        drawMode = 4  # Circle
            
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

    #Setting header image
    img[0:115, 0:1280] = header
    #img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)
    cv2.imshow("Console", img)
    key = cv2.waitKey(1)
    if key == ord('s'):
        break
cv2.destroyAllWindows()
#print(image_text)
from read_img import image_text

print(image_text)


