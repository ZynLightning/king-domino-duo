import cv2 as cv
import numpy as np

BGRimage = cv.imread("1.jpg") #choose image
HSVimage = cv.cvtColor(BGRimage,cv.COLOR_BGR2HSV)
board=np.zeros((5,5), dtype=str)

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
#cv.imshow("oceanOpen",oceanOpen)
#cv.imshow("grassOpen",grassOpen)
#cv.imshow("forestOpen",forestOpen)
#cv.imshow("fieldOpen",fieldOpen)
#cv.imshow("wasteOpen",wasteOpen)
#cv.imshow("mineOpen",mineOpen)

#show the thresholded masks:
#cv.imshow("oceanMask",oceanMask)
#cv.imshow("grassMask",grassMask)
#cv.imshow("forestMask",forestMask)
#cv.imshow("fieldMask",fieldMask)
#cv.imshow("wasteMask",wasteMask)
#cv.imshow("mineMask",mineMask)
#cv.waitKey(0)

#Finding the biome of each square: 
for i in range(5): #for each row
    for j in range(5): #for each square in the row
        oceanValue=0
        grassLandValue=0
        forestValue=0
        fieldValue=0
        wasteValue=0
        mineValue=0
        for y in range(100): #for each pixelrow
            for x in range(100): #for each pixel in row
                if oceanOpen[y+i*100,x+j*100]!=0: #if the pixel looks like ocean
                    oceanValue+=1
                elif grassOpen[y+i*100,x+j*100]!=0: #if the pixel looks like grassLand
                    grassLandValue+=1
                elif forestOpen[y+i*100,x+j*100]!=0: #if the pixel looks like grassLand
                    forestValue+=1
                elif fieldOpen[y+i*100,x+j*100]!=0: #if the pixel looks like grassLand
                    fieldValue+=1
                elif wasteOpen[y+i*100,x+j*100]!=0: #if the pixel looks like grassLand
                    wasteValue+=1
                elif mineOpen[y+i*100,x+j*100]!=0: #if the pixel looks like grassLand
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
        
print(board)





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