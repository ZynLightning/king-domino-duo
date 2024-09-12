import cv2 as cv
import numpy as np

BGRimage = cv.imread("2.jpg")
HSVimage = cv.cvtColor(BGRimage,cv.COLOR_BGR2HSV)
board=np.zeros((5,5), dtype=str)
for i in range(5):
    for j in range(5):
        oceanValue=0
        grassLandValue=0
        forestValue=0
        fieldValue=0
        wasteValue=0
        mineValue=0
        for row in HSVimage[100*i:100*(i+1),100*j:100*(j+1)]:
            for pixel in row:
                if 102<pixel[0]<111: #check if the pixel is typical for ocean
                    oceanValue+=1
                elif (53/255*180)<pixel[0]<(79/255*180) and 130<pixel[2]<255:
                    grassLandValue+=1
                elif (49/255*180)<pixel[0]<(87/255*180) and pixel[1]<210 and pixel[2]<85:
                    forestValue+=1
                elif (26/255*180)<pixel[0]<(41/255*180) and 223<pixel[1]<255 and 168<pixel[2]:
                    fieldValue+=1
                elif (16/255*180)<pixel[0]<(34/255*180) and pixel[1]<172 and 51<pixel[2]<151:
                    wasteValue+=1
                elif pixel[0]<(44/255*180) and pixel[1]<113 and pixel[2]<79:
                    mineValue+=1
        if 1000>np.max([oceanValue,grassLandValue,forestValue,fieldValue,wasteValue,mineValue]):
            board[i,j]="Ki"        
        elif oceanValue==np.max([oceanValue,grassLandValue,forestValue,fieldValue,wasteValue,mineValue]):
            board[i,j]="Oc"
        elif grassLandValue==np.max([oceanValue,grassLandValue,forestValue,fieldValue,wasteValue,mineValue]):
            board[i,j]="Gr"
        elif forestValue==np.max([oceanValue,grassLandValue,forestValue,fieldValue,wasteValue,mineValue]):
            board[i,j]="Tr"
        elif fieldValue==np.max([oceanValue,grassLandValue,forestValue,fieldValue,wasteValue,mineValue]):
            board[i,j]="Fi"
        elif wasteValue==np.max([oceanValue,grassLandValue,forestValue,fieldValue,wasteValue,mineValue]):
            board[i,j]="Wa"
        elif mineValue==np.max([oceanValue,grassLandValue,forestValue,fieldValue,wasteValue,mineValue]):
            board[i,j]="Mi"
        
        print(f"[{j+1},{i+1}] oceanVal={oceanValue}, grassVal={grassLandValue}, forestVal={forestValue}, fieldVal={fieldValue}, wasteVal={wasteValue}, mineVal={mineValue}")
print(board)