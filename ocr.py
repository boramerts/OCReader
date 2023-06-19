import pytesseract
from pytesseract import Output
import argparse
import cv2
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import PySimpleGUI as sg

custom_config = r'--oem 3 --psm 1'

#Tk.withdraw()
image = askopenfilename()

# image = cv2.imread(args["image"])
image = cv2.imread(image)
gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
thresh_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

ocr_output = pytesseract.image_to_data(thresh_img, output_type = Output.DICT, \
                                       config=custom_config, lang='eng')

n_space = 0
for i in ocr_output['text']:
    if i == '' or i == ' ':
        if n_space<2:
            print('')
            n_space+=1
    else:
        print(i,end=" ")
        n_space = 0

n_boxes = len(ocr_output['level'])

for i in range(n_boxes):
    (x,y,w,h) = (ocr_output['left'][i],ocr_output['top'][i],ocr_output['width'][i],ocr_output['height'][i])
    cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)

print(ocr_output.keys())

cv2.imshow('image',image)
cv2.waitKey(0)
cv2.destroyWindow("image")