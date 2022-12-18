# Python code to find the co-ordinates of
# the contours detected in an image.
# import numpy as np
import cv2

def Find_coordinate():
    coordinate = ['', '', '', '', '', '', '', '', '', '', '', '']

    # Reading image
    # img2 = cv2.imread('images/rectangle2.jpg', cv2.IMREAD_COLOR)
    img = cv2.imread('image.jpg',  cv2.IMREAD_COLOR)

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Converting image to a binary image
    # ( black and white only image).
    # _, threshold = cv2.threshold(img, 110, 255, cv2.THRESH_BINARY)

    imgEdge = cv2.Canny(img, 50, 200)

    # Detecting contours in image.
    contours, _ = cv2.findContours(imgEdge, cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)

    contours = sorted(contours, key=cv2.contourArea, reverse=False)
    # test = contours.ravel()
    # print('test', contours)

    # Going through every contours found in the image.
    # for cnt in contours:

    approx = cv2.approxPolyDP(contours[len(contours) - 1], 0.009 * cv2.arcLength(contours[len(contours) - 1], True), True)

    # draws boundary of contours.
    cv2.drawContours(img, [approx], 0, (0, 0, 255), 5)

    # Used to flatted the array containing
    # the co-ordinates of the vertices.
    n = approx.ravel()
    i = 0
    # print('approx', approx)
    # print('n', n)
    # for j in n:
    #     if (i % 2 == 0):
    #         x = n[i]
    #         y = n[i + 1]
    #         print('x ', x, ' y ', y)
    #     i = i + 1

    if len(n) <= 12:
        coordinate = n
    else:
        for j in n:
            if i < 12:
                coordinate[i] = j
            i = i + 1

    return coordinate

# Showing the final image.
# print('coordinate', coordinate)
# img = cv2.resize(img, (634, 936), interpolation=cv2.INTER_AREA)
# imgEdge = cv2.resize(imgEdge, (634, 936), interpolation=cv2.INTER_AREA)
# cv2.imshow('image2', img)

# Exiting the window if 'q' is pressed on the keyboard.
# cv2.waitKey(0)