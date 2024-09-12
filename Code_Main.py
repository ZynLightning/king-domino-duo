import cv2 as cv
import numpy as np

BGRimage = cv.imread("1.jpg")
HSVimage = cv.cvtColor(BGRimage,cv.COLOR_BGR2HSV)
for i in range(5):
    for j in range(5):
        oceanValue=0
        for row in HSVimage[100*i:100*(i+1),100*j:100*(j+1)]:
            for pixel in row:
                if 102<pixel[0]<111:
                    oceanValue+=1
                
        print(oceanValue)