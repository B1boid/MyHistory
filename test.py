import cv2
import pytesseract
from PIL import Image, ImageOps
import re


def test():
    pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'
    #open_img = Image.open("tmp.png")
    #inverted = ImageOps.invert(open_img)
    #inverted.save("inverted.png")
    #to_show = cv2.imread("inverted.png")

    img = cv2.imread("tmp.png", cv2.IMREAD_GRAYSCALE)

    thresh = 100

    img_thresh = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)[1]

    inverted = cv2.bitwise_not(img_thresh)
    to_show = cv2.resize(inverted, (200, 200))

    #img = cv2.imread("tmp.png")


    cv2.imshow("Test", ~img)
    print(pytesseract.image_to_string(~img))
    cv2.waitKey(0)


test()
