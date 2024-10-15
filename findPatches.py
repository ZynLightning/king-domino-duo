import cv2 as cv
import numpy as np
import copy
board = np.zeros((5,5), dtype=str)

class biomes:
    def findBiomes(self, ImageName):
        BGRimage = cv.imread(ImageName) #choose image
        HSVimage = cv.cvtColor(BGRimage,cv.COLOR_BGR2HSV)
        board=np.zeros((5,5), dtype=str)

        #thresholds for the different biomes:
        oceanMin=np.array([(144/255*180), 176, 0]) #Lowhue, LowSat, LowVal
        oceanMax=np.array([(157/255*180), 255, 255])#HighHue, HighSat, HighVal

        grassMin=np.array([(53/255*180),0,130])
        grassMax=np.array([(87/255*180),255,255])

        forestMin=np.array([(49/255*180),0,0])
        forestMax=np.array([(87/255*180),210,85])

        fieldMin=np.array([(26/255*180),223,168])
        fieldMax=np.array([(41/255*180),255,255])

        wasteMin=np.array([(16/255*180),60,45])
        wasteMax=np.array([(34/255*180),200,151])

        mineMin1=np.array([0,0,0])
        mineMax1=np.array([(49),113,79]) #Hue=69
        
        mineMin2=np.array([(228/255*180),0,0])
        mineMax2=np.array([(242/255*180),113,79])
        
        #laver thresholds på alle biomes:
        oceanMask=cv.inRange(HSVimage, oceanMin, oceanMax) 
        grassMask=cv.inRange(HSVimage,grassMin,grassMax)
        forestMask=cv.inRange(HSVimage,forestMin,forestMax)
        fieldMask=cv.inRange(HSVimage,fieldMin,fieldMax)
        wasteMask=cv.inRange(HSVimage,wasteMin,wasteMax)
        mineMask1=cv.inRange(HSVimage,mineMin1,mineMax1)
        mineMask2=cv.inRange(HSVimage,mineMin2,mineMax2)
        mineMask=cv.bitwise_or(mineMask1,mineMask2,mask=None) #the mine biome spans over two very different hues, and so two masks are created with the different hues and put together.
        
        #create a kernel:
        #kernel = cv.getStructuringElement(cv.MORPH_RECT,(5,5)) #laver en rektangulær 5x5 kernel
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(7,7)) # laver en cirkulær 7x7 kernel

        #first erode then dilate the masks, creating an opened image:
        self.oceanOpen=cv.morphologyEx(oceanMask,cv.MORPH_OPEN,kernel)
        self.grassOpen=cv.morphologyEx(grassMask,cv.MORPH_OPEN,kernel)
        self.forestOpen=cv.morphologyEx(forestMask,cv.MORPH_OPEN,kernel)
        self.fieldOpen=cv.morphologyEx(fieldMask,cv.MORPH_OPEN,kernel)
        self.wasteOpen=cv.morphologyEx(wasteMask,cv.MORPH_OPEN,kernel)
        self.mineOpen=cv.morphologyEx(mineMask,cv.MORPH_OPEN,kernel)

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
      
    def findBoard(self):
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
                        if self.oceanOpen[y+i*100,x+j*100]!=0: #if the pixel looks like ocean
                                oceanValue+=1
                        elif self.grassOpen[y+i*100,x+j*100]!=0: #if the pixel looks like grassLand
                            grassLandValue+=1
                        elif self.forestOpen[y+i*100,x+j*100]!=0: #if the pixel looks like grassLand
                            forestValue+=1
                        elif self.fieldOpen[y+i*100,x+j*100]!=0: #if the pixel looks like grassLand
                            fieldValue+=1
                        elif self.wasteOpen[y+i*100,x+j*100]!=0: #if the pixel looks like grassLand
                            wasteValue+=1
                        elif self.mineOpen[y+i*100,x+j*100]!=0: #if the pixel looks like grassLand
                            mineValue+=1
                self.values=[oceanValue,grassLandValue,forestValue,fieldValue,wasteValue,mineValue]
                
                if 800>np.max(self.values): #if it is not typical for anything else, it's probably the king piece
                    board[i,j]="Ki"#kingpiece 
                         
                elif self.values[0]==np.max(self.values): #if there are more values for ocean than any other, then it's an ocean piece
                    board[i,j]="Oc"#Ocean
                    
                elif self.values[1]==np.max(self.values):
                    board[i,j]="Gr"#Grassland
                    
                elif self.values[2]==np.max(self.values):
                    board[i,j]="Fo"#Forest
                    
                elif self.values[3]==np.max(self.values):
                    board[i,j]="Ag"#Agriculture
                    
                elif self.values[4]==np.max(self.values):
                    board[i,j]="Wa"#Wasteland
                    
                elif self.values[5]==np.max(self.values):
                    board[i,j]="Mi"#Mines
        return(board)


class Patches: #brug Patch-analyse til at finde sammenhængende biomes i vores matrix
    
    def WildfireStart(self,cPos):#kører for at skabe hver Patch
    
        Patch=[] #liste som bliver lavet for hver Patch og bliver tilføjet til for hvert felt
        burnList=[] #liste over felter som skal brændes. Indeholder også typen af biome, vi leder efter i denne Patch
        burnList.append(board[cPos[0],cPos[1]]) #tilføjer typen af biome vi leder efter
        
        while len(burnList)>0: #loop som fortsætter indtil Patchben er fuldført og burnList dermed er tom
            board[cPos[0],cPos[1]]="X" #brænder current position
            
            if cPos[0]!=0 and board[cPos[0]-1,cPos[1]]==burnList[0] and not ([cPos[0]-1,cPos[1]] in burnList): #Er feltet over cPos det samme biome?
                burnList.append([cPos[0]-1,cPos[1]]) #Tilføj til burnList
            if cPos[1]!=0 and board[cPos[0],cPos[1]-1]==burnList[0] and not ([cPos[0],cPos[1]-1] in burnList): #Er feltet til venstre for cPos det samme biome?
                burnList.append([cPos[0],cPos[1]-1]) #Tilføj til burnList
            if cPos[0]!=4 and board[cPos[0]+1,cPos[1]]==burnList[0] and not ([cPos[0]+1,cPos[1]+1] in burnList): #Er feltet under cPos det samme biome?
                burnList.append([cPos[0]+1,cPos[1]]) #Tilføj til burnList
            if cPos[1]!=4 and board[cPos[0],cPos[1]+1]==burnList[0] and not ([cPos[0],cPos[1]+1] in burnList): #Er feltet til højre for cPos det samme biome?
                burnList.append([cPos[0],cPos[1]+1]) #Tilføj til burnList
            Patch.append(cPos) #Tilføj til den nuværende Patch
            cPos=burnList[len(burnList)-1] #hop til sidst tilføjede koordinat i burnList
            burnList.pop(len(burnList)-1) #fjern sidst tilføjede koordinat fra burnList
        return Patch #returner nuværende Patch
    
    def wildfire(self): #finder bolbs, starter WildfireStart og samler Patchs til en samlet liste.
        biomePatchList=[] #samlet liste over Patches
        for i, rowb in enumerate(board):
            for j, pointb in enumerate(rowb):
                cPos=[i,j]
                if pointb!="X": #hvis feltet ikke er brændt
                    biomePatchList.append(Patches().WildfireStart(cPos))#bruger WildfireStart til at få en blob som tilføjes til biombePatchList
        return(biomePatchList)

