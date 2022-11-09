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
beg_x, beg_y = 0, 0

#Zoom
dis1 = 0

x0, y0 = 0, 0
x1, y1 = 0, 0
x2, y2 = 0, 0
x3, y3 = 0, 0
radius = 0

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
        des_x1, des_y1 = lmList[8][1:]
        #Middle finger
        des_x2, des_y2 = lmList[12][1:]


        #Thumb
        # thump_x, thump_y = lmList[4][1:]




        #Checking finger (Up/Down)
        finger = detector.fingerUP()
        # print(finger)


        #Zoom
        # if finger[0]==True and finger[1]==True and finger[2]==False:
        #     cv2.circle(img, (des_x1, des_y1), 15, drawColor, cv2.FILLED)
        #     cv2.circle(img, (thump_x, thump_y), 15, drawColor, cv2.FILLED)
        #     dis0 = ((thump_x - des_x1) ** 2 + (thump_y - des_y1) ** 2) ** 0.5
        #     if dis1 == 0:
        #         dis1 = dis0
        #     # if dis0 > dis1:#zoom in
        #
        #     scale_percent = (dis0 / dis1) * 100
        #     # print(dis1)
        #     # print(scale_percent)
        #     width = int(1280 * scale_percent / 100)
        #     height = int(720 * scale_percent / 100)
        #     width_crop = (width - 1280)/2
        #     height_crop = (height - 720)/2
        #     cv2.resize(img, (width, height))
        #     cv2.resize(imgCanvas, (width, height))
        #     # img = img[0 + width_crop: width - width_crop, 0 + height_crop: height - height_crop]
        #     # imgCanvas = imgCanvas[0 + width_crop: width - width_crop, 0 + height_crop: height - height_crop]



        #Drawing Mode
        if finger[1]==True and finger[2]==False and finger[0]==False:
            cv2.circle(img, (des_x1, des_y1), 15, drawColor, cv2.FILLED)
            #print("Drawing Mode")
            if beg_x == 0 and beg_y == 0:
                beg_x, beg_y = des_x1, des_y1
            #Draw & Eraser line in img:
            if mode and drawMode == 0:
                if mode == 2:
                    cv2.line(img, (beg_x, beg_y), (des_x1, des_y1), drawColor, eraser)
                    cv2.line(imgCanvas, (beg_x, beg_y), (des_x1, des_y1), drawColor, eraser)
                elif mode == 1:
                    cv2.line(img, (beg_x, beg_y), (des_x1, des_y1), drawColor, brush)
                    cv2.line(imgCanvas, (beg_x, beg_y), (des_x1, des_y1), drawColor, brush)
                beg_x, beg_y = des_x1, des_y1

            #Draw mode
            if drawMode != 0:
                imgCanvas = np.zeros((720, 1280, 3), np.uint8)

                # Line
                if drawMode == 1:
                    cv2.line(img, (beg_x, beg_y), (des_x1, des_y1), drawColor, brush)
                    cv2.line(imgCanvas, (beg_x, beg_y), (des_x1, des_y1), drawColor, brush)
                    x0, y0 = beg_x, beg_y
                    x1, y1 = des_x1, des_y1

                # Triangle
                elif drawMode == 2:
                    pt1 = (int((beg_x + des_x1)/2), beg_y)
                    pt2 = (beg_x, des_y1)
                    pt3 = (des_x1, des_y1)

                    cv2.line(img, pt1, pt2, drawColor, brush)
                    cv2.line(img, pt2, pt3, drawColor, brush)
                    cv2.line(img, pt3, pt1, drawColor, brush)
                    cv2.line(imgCanvas, pt1, pt2, drawColor, brush)
                    cv2.line(imgCanvas, pt2, pt3, drawColor, brush)
                    cv2.line(imgCanvas, pt3, pt1, drawColor, brush)

                    x0, y0 = pt1
                    x1, y1 = pt2
                    x3, y3 = pt3

                # Rectangle
                elif drawMode == 3:
                    cv2.rectangle(img, (beg_x, beg_y), (des_x1, des_y1), drawColor, brush)
                    cv2.rectangle(imgCanvas, (beg_x, beg_y), (des_x1, des_y1), drawColor, brush)

                    x0, y0 = beg_x, beg_y
                    x1, y1 = des_x1, beg_y
                    x2, y2 = beg_x, des_y1
                    x3, y3 = des_x1, des_y1

                # Circle
                elif drawMode == 4:
                    if abs(des_x1 - beg_x) > abs(des_y1 - beg_y):
                        radius = int(abs(des_y1 - beg_y)/2)
                        if des_y1 > beg_y and des_x1 > beg_x:
                            cv2.circle(img, ((beg_x + radius), (beg_y + radius)), radius, drawColor, brush)
                            cv2.circle(imgCanvas, ((beg_x + radius), (beg_y + radius)), radius, drawColor, brush)
                            x0, y0 = ((beg_x + radius), (beg_y + radius))

                        elif des_y1 > beg_y and des_x1 < beg_x:
                            cv2.circle(img, ((des_x1 + radius), (beg_y + radius)), radius, drawColor, brush)
                            cv2.circle(imgCanvas, ((des_x1 + radius), (beg_y + radius)), radius, drawColor, brush)
                            x0, y0 = ((des_x1 + radius), (beg_y + radius))

                        elif des_y1 < beg_y and des_x1 > beg_x:
                            cv2.circle(img, ((beg_x + radius), (des_y1 + radius)), radius, drawColor, brush)
                            cv2.circle(imgCanvas, ((beg_x + radius), (des_y1 + radius)), radius, drawColor, brush)
                            x0, y0 = ((beg_x + radius), (des_y1 + radius))

                        else:
                            cv2.circle(img, ((des_x1 + radius), (des_y1 + radius)), radius, drawColor, brush)
                            cv2.circle(imgCanvas, ((des_x1 + radius), (des_y1 + radius)), radius, drawColor, brush)
                            x0, y0 = ((des_x1 + radius), (des_y1 + radius))

                    else:
                        radius = int(abs(des_x1 - beg_x)/2)
                        if des_y1 > beg_y and des_x1 > beg_x:
                            cv2.circle(img, ((beg_x + radius), (beg_y + radius)), radius, drawColor, brush)
                            cv2.circle(imgCanvas, ((beg_x + radius), (beg_y + radius)), radius, drawColor, brush)
                            x0, y0 = ((beg_x + radius), (beg_y + radius))

                        elif des_y1 > beg_y and des_x1 < beg_x:
                            cv2.circle(img, ((des_x1 + radius), (beg_y + radius)), radius, drawColor, brush)
                            cv2.circle(imgCanvas, ((des_x1 + radius), (beg_y + radius)), radius, drawColor, brush)
                            x0, y0 = ((des_x1 + radius), (beg_y + radius))

                        elif des_y1 < beg_y and des_x1 > beg_x:
                            cv2.circle(img, ((beg_x + radius), (des_y1 + radius)), radius, drawColor, brush)
                            cv2.circle(imgCanvas, ((beg_x + radius), (des_y1 + radius)), radius, drawColor, brush)
                            x0, y0 = ((beg_x + radius), (des_y1 + radius))

                        else:
                            cv2.circle(img, ((des_x1 + radius), (des_y1 + radius)), radius, drawColor, brush)
                            cv2.circle(imgCanvas, ((des_x1 + radius), (des_y1 + radius)), radius, drawColor, brush)
                            x0, y0 = ((des_x1 + radius), (des_y1 + radius))


            # beg_x, beg_y = des_x1, des_y1

        # n = n + 1
        # print(n)

        #Selecting Mode
        if finger[1] and finger[2]:
            #print("Selection Mode")
            beg_x, beg_y = 0, 0
            if 0 < des_y1 < 115: 
                if 237 < des_x1 < 352: 
                    header = overlayList[1]
                    drawColor = (255, 0, 255)
                    mode = 1

                elif 467 < des_x1 < 582: 
                    header = overlayList[2]
                    drawColor = (0, 0, 0)   
                    mode = 2 

                elif 697 < des_x1 < 812: 
                    header = overlayList[3]
                    imgCanvas = cv2.bitwise_xor(imgCanvas, imgCanvas)
                    
                elif 927 < des_x1 < 1042: 
                    header = overlayList[0]
                    pw_r = 'Image/password_record.png'
                    img_r = 'Fail/fail_record.png'
                    cv2.imwrite(pw_r, imgInv)
                    break
                    #Export password screen to file png

            if mode == 1:
                img[605:720, 0:1280] = footer
                if 605 < des_y1 < 720:
                    if 237 < des_x1 < 352:
                        footer = overlayList[5]
                        drawColor = (255, 0, 255)
                        drawMode = 1  # Line

                    elif 467 < des_x1 < 582:
                        footer = overlayList[6]
                        drawColor = (255, 0, 255)
                        drawMode = 2  # Triangle

                    elif 697 < des_x1 < 812:
                        footer = overlayList[7]
                        drawColor = (255, 0, 255)
                        drawMode = 3  # Rectangle

                    elif 927 < des_x1 < 1042:
                        footer = overlayList[8]
                        drawColor = (255, 0, 255)
                        drawMode = 4  # Circle
            
            cv2.rectangle(img, (des_x1, des_y1 - 25), (des_x2, des_y2 + 25), drawColor, cv2.FILLED)

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

print("x0, y0 = ", x0, y0)
print("x1, y1 = ", x1, y1)
print("x2, y2 = ", x2, y2)
print("x3, y3 = ", x3, y3)
print("r = ", radius)

print(image_text)


