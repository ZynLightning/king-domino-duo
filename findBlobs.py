import cv2 as cv
import numpy as np

BGRimage = cv.imread("1.jpg") #choose image
HSVimage = cv.cvtColor(BGRimage,cv.COLOR_BGR2HSV)
board=np.zeros((5,5), dtype=str)


""" for i in range(5): #Finding the biome of each square: #overvej at lave et threshold billede for hvert biome til troubleshooting og brug af opening, reduction osv.
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
                elif (53/255*180)<pixel[0]<(79/255*180) and 130<pixel[2]<255:#check if the pixel is typical for grassland
                    grassLandValue+=1
                elif (49/255*180)<pixel[0]<(87/255*180) and pixel[1]<210 and pixel[2]<85:#check if the pixel is typical for forest
                    forestValue+=1
                elif (26/255*180)<pixel[0]<(41/255*180) and 223<pixel[1]<255 and 168<pixel[2]:#check if the pixel is typical for field
                    fieldValue+=1
                elif (16/255*180)<pixel[0]<(34/255*180) and pixel[1]<172 and 51<pixel[2]<151:#check if the pixel is typical for wasteland
                    wasteValue+=1
                elif pixel[0]<(44/255*180) and pixel[1]<113 and pixel[2]<79:#check if the pixel is typical for mines
                    mineValue+=1
        if 1000>np.max([oceanValue,grassLandValue,forestValue,fieldValue,wasteValue,mineValue]): #if it is not typical for anything else, it's probably the king piece
            board[i,j]="Ki"#kingpiece      
        elif oceanValue==np.max([oceanValue,grassLandValue,forestValue,fieldValue,wasteValue,mineValue]): #if there are more values for ocean than any other, then it's an ocean piece
            board[i,j]="Oc"#Ocean
        elif grassLandValue==np.max([oceanValue,grassLandValue,forestValue,fieldValue,wasteValue,mineValue]):
            board[i,j]="Gr"#Grassland
        elif forestValue==np.max([oceanValue,grassLandValue,forestValue,fieldValue,wasteValue,mineValue]):
            board[i,j]="Fo"#Forest
        elif fieldValue==np.max([oceanValue,grassLandValue,forestValue,fieldValue,wasteValue,mineValue]):
            board[i,j]="Ag"#Agriculture
        elif wasteValue==np.max([oceanValue,grassLandValue,forestValue,fieldValue,wasteValue,mineValue]):
            board[i,j]="Wa"#Wateland
        elif mineValue==np.max([oceanValue,grassLandValue,forestValue,fieldValue,wasteValue,mineValue]):
            board[i,j]="Mi"#Mines
         """

#thresholds for the different biomes:
oceanMin=np.array([102, 0, 0]) #Lowhue, LowSat, LowVal
oceanMax=np.array([111, 255, 255])#HighHue, HighSat, HighVal

grassMin=np.array([(53/255*180),0,130])
grassMax=np.array([(87/255*180),255,255])

forestMin=np.array([(49/255*180),0,0])
forestMax=np.array([(87/255*180),210,85])

fieldMin=np.array([(26/255*180),223,168])
fieldMax=np.array([(41/255*180),255,255])

wasteMin=np.array([(16/255*180),0,51])
wasteMax=np.array([(34/255*180),172,151])

mineMin=np.array([0,0,0])
mineMax=np.array([31,113,79])

#laver thresholds på alle biomes:
oceanMask=cv.inRange(HSVimage, oceanMin, oceanMax) 
grassMask=cv.inRange(HSVimage,grassMin,grassMax)
forestMask=cv.inRange(HSVimage,forestMin,forestMax)
fieldMask=cv.inRange(HSVimage,fieldMin,fieldMax)
wasteMask=cv.inRange(HSVimage,wasteMin,wasteMax)
mineMask=cv.inRange(HSVimage,mineMin,mineMax)

#create a kernel:
#kernel = cv.getStructuringElement(cv.MORPH_RECT,(5,5)) #laver en rektangulær 5x5 kernel
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(5,5)) # laver en cirkulær 5x5 kernel

#first erode then dilate the masks, creating an opened image:
oceanOpen=cv.morphologyEx(oceanMask,cv.MORPH_OPEN,kernel)
grassOpen=cv.morphologyEx(grassMask,cv.MORPH_OPEN,kernel)
forestOpen=cv.morphologyEx(forestMask,cv.MORPH_OPEN,kernel)
fieldOpen=cv.morphologyEx(fieldMask,cv.MORPH_OPEN,kernel)
wasteOpen=cv.morphologyEx(wasteMask,cv.MORPH_OPEN,kernel)
mineOpen=cv.morphologyEx(mineMask,cv.MORPH_OPEN,kernel)

#show the opened images:
cv.imshow("oceanOpen",oceanOpen)
cv.imshow("grassOpen",grassOpen)
#cv.imshow("forestOpen",forestOpen)
#cv.imshow("fieldOpen",fieldOpen)
#cv.imshow("wasteOpen",wasteOpen)
#cv.imshow("mineOpen",mineOpen)

#show the thresholded masks:
cv.imshow("oceanMask",oceanMask)
cv.imshow("grassMask",grassMask)
#cv.imshow("forestMask",forestMask)
#cv.imshow("fieldMask",fieldMask)
#cv.imshow("wasteMask",wasteMask)
#cv.imshow("mineMask",mineMask)
cv.waitKey(0)
f=0
for i in range(5): #Finding the biome of each square: 
    for j in range(5):
        oceanValue=0
        grassLandValue=0
        forestValue=0
        fieldValue=0
        wasteValue=0
        mineValue=0
        for y, row in enumerate(HSVimage[100*i:100*(i+1),100*j:100*(j+1)]):
            for x, pixel in enumerate(row):
                print(f)
                f+=1
                if oceanOpen[y,x]!=0:
                    print(oceanOpen[y,x])
                    




#brug blob-analyse til at finde sammenhængende biomes i vores matrix:

def WildfireStart(cPos):
    
    blobList=[] #liste som bliver lavet for hver blob og bliver tilføjet til for hvert felt
    burnList=[] #liste over felter som skal brændes. Indeholder også typen af biome, vi leder efter i denne blob
    burnList.append(board[cPos[0],cPos[1]]) #tilføjer typen af biome vi leder efter
    
    while len(burnList)>0: #loop som fortsætter indtil blobben er fuldført og burnList dermed er tom
        board[cPos[0],cPos[1]]="X" #brænder current position
        
        if cPos[0]!=0 and board[cPos[0]-1,cPos[1]]==burnList[0] and not ([cPos[0]-1,cPos[1]] in burnList): #Er feltet over cPos det samme biome?
            burnList.append([cPos[0]-1,cPos[1]]) #Tilføj til burnList
        if cPos[1]!=0 and board[cPos[0],cPos[1]-1]==burnList[0] and not ([cPos[0],cPos[1]-1] in burnList): #Er feltet til venstre for cPos det samme biome?
            burnList.append([cPos[0],cPos[1]-1]) #Tilføj til burnList
        if cPos[0]!=4 and board[cPos[0]+1,cPos[1]]==burnList[0] and not ([cPos[0]+1,cPos[1]+1] in burnList): #Er feltet under cPos det samme biome?
            burnList.append([cPos[0]+1,cPos[1]]) #Tilføj til burnList
        if cPos[1]!=4 and board[cPos[0],cPos[1]+1]==burnList[0] and not ([cPos[0],cPos[1]+1] in burnList): #Er feltet til højre for cPos det samme biome?
            burnList.append([cPos[0],cPos[1]+1]) #Tilføj til burnList
        blobList.append(cPos) #Tilføj til den nuværende blob
        cPos=burnList[len(burnList)-1] #hop til sidst tilføjede koordinat i burnList
        burnList.pop(len(burnList)-1) #fjern sidst tilføjede koordinat fra burnList
    return blobList #returner nuværende blob
        
biomeBlobList=[] #samlet liste over blobs
for i, rowb in enumerate(board):
    for j, pointb in enumerate(rowb):
        cPos=[i,j]
        if pointb!="X": #hvis feltet ikke er brændt
            biomeBlobList.append(WildfireStart(cPos))#bruger WildfireStart til at få en blob som tilføjes til biombeBlobList
print(biomeBlobList)
print(board)

print("done :)")