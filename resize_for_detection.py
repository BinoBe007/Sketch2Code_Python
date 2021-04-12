import numpy as np
import PIL
from PIL import Image
import os
from Object_detection_image_flask2 import *
mywidth = 960
def resizer(filepath, filename, image):
    img = Image.open(filepath)
    #print(filepath)
    #print(filename)
    #print(img)
    wpercent = (mywidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((mywidth,hsize), PIL.Image.ANTIALIAS)
    img.save(filepath)
    #print(filepath)
    detector(filepath,filename)
def crop(filepath, filename, img):
    img = cv2.imread(filepath)
    
    xmin_val=[]
    xmax_val=[]
    ymin_val=[]
    ymax_val=[]
    edged = cv2.Canny(img, 10, 250)
        
    #applying closing function 
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

    bounding_boxes = []
    #finding_contours 
    (cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(img, cnts, -1, (255, 255, 0), 1)
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)

        if w > 20 and h > 5:
            xmin_val.append(x)
            xmax_val.append(x+w)
            ymin_val.append(y)
            ymax_val.append(y+h)
            start_point = (x, y) 
            end_point = (x+w, y+h) 
            color = (255, 212, 25) 
            thickness = 2
            #imaged = cv2.rectangle(img, start_point, end_point, color, thickness)

    xmin_small = xmin_val[len(xmin_val)-1]
    xmax_large = 0
    ymin_small = ymin_val[len(ymin_val)-1]
    ymax_large = 0
    for i in range(len(xmin_val)):
        if xmin_val[i] < xmin_small:
            #print("true",xmin_val[i])
            xmin_small = xmin_val[i]  

    for i in xmax_val:
        if i > xmax_large:
            xmax_large = i

    for j in range(len(ymin_val)):
        if ymin_val[j] < ymin_small:
            ymin_small = ymin_val[j]

    for j in ymax_val:
        if j > ymax_large:
            ymax_large = j
    if ymin_small > 5:
        ymin_small= ymin_small-5
    if ymin_small > 3:
        ymin_small= ymin_small-2

    img = img[ymin_small:ymax_large+5,xmin_small:xmax_large+2]
    cv2.imwrite(filepath, img)
    '''cv2.imshow("gaus", img)
    #cv2.imwrite("ada.png",gaus)
    cv2.waitKey(0)
    cv2.destroyAllWindows()'''
    #print(filepath)
    resizer(filepath, filename, img)





