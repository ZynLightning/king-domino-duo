import cv2 as cv
import numpy as np

BGRimage = cv.imread("1.jpg") #choose image
HSVimage = cv.cvtColor(BGRimage,cv.COLOR_BGR2HSV)
board=np.zeros((5,5), dtype=str)


for i in range(5): #Finding the biome of each square: #overvej at lave et threshold billede for hvert biome til troubleshooting og brug af opening, reduction osv.
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
        
        #print(f"[{j+1},{i+1}] oceanVal={oceanValue}, grassVal={grassLandValue}, forestVal={forestValue}, fieldVal={fieldValue}, wasteVal={wasteValue}, mineVal={mineValue}")

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