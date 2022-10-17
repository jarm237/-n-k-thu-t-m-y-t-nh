import os
# import pytesseract
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import cv2
import numpy as np
from matplotlib import pyplot as plt

Path = "Image"
myImage = os.listdir(Path)
core = "password_record.png"
if core in myImage:
    image = cv2.imread('Image/password_record.png', cv2.IMREAD_UNCHANGED)
else:
    image = cv2.imread('empty_pw/blank.png', cv2.IMREAD_UNCHANGED)

cs_config = r'-c tessedit_char_whitelist=ABCDEFGH123456789 --psm 7 --oem 3'
# image_text = pytesseract.image_to_string(image, lang='eng', config=cs_config)

# reading image
img = cv2.imread('Image/password_record.png')

# converting image into grayscale image
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# setting threshold of gray image
_, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# using a findContours() function
contours, _ = cv2.findContours(
    threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

i = 0

# list for storing names of shapes
for contour in contours:

    # here we are ignoring first counter because
    # findcontour function detects whole image as shape
    if i == 0:
        i = 1
        continue

    # cv2.approxPloyDP() function to approximate the shape
    approx = cv2.approxPolyDP(
        contour, 0.01 * cv2.arcLength(contour, True), True)

    # bounding around the object
    x, y, w, h = cv2.boundingRect(approx)

    # using drawContours() function
    cv2.drawContours(img, [contour], 0, (0, 0, 255), 5)

    # finding center point of shape
    M = cv2.moments(contour)
    if M['m00'] != 0.0:
        x = int(M['m10'] / M['m00'])
        y = int(M['m01'] / M['m00'])

    # putting shape name at center of each shape
    if len(approx) == 3:
        # cv2.putText(img, 'Triangle', (x, y),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        image_text = 'Triangle'

    elif len(approx) == 4:
        # cv2.putText(img, 'Quadrilateral', (x, y),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        # image_text = 'Quadrilateral'
        aspRatio = w / float(h)
        if aspRatio > 0.95 and aspRatio < 1.05:
            image_text = 'Square'
        else:
            image_text = 'Rectangle'

    elif len(approx) == 5:
        # cv2.putText(img, 'Pentagon', (x, y),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        image_text = 'Pentagon'

    elif len(approx) == 6:
        # cv2.putText(img, 'Hexagon', (x, y),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        image_text = 'Hexagon'

    else:
        # cv2.putText(img, 'circle', (x, y),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        image_text = 'circle'

# displaying the image after drawing contours
# cv2.imshow('shapes', img)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()
