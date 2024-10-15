import cv2 as cv
from findBlobs import blobs, biomes
from templateSearch import Template_Searcher
biome = biomes()
blob=blobs()
ts = Template_Searcher()
pointList=[]
for n in range(74):
    boardNumber=str(n+1)#input("Which board do you want counted?\n")
    biome.findBiomes(f"boards/{boardNumber}.jpg")
    board=biome.findBoard()
    crownList=ts.program(cv.imread(f"boards/{boardNumber}.jpg"),board)
    blobList=blob.wildfire()
    points = 0
    
#print(crownList)


#print(blobList)

    
    points = 0
    for entry in crownList[1]:# for every entry in the crownList
        for list in blobList: #for every entry in bloblist
            if entry in list: #if the entry from crownlist is in that blob:
                points+=len(list)*crownList[0][entry[0],entry[1]] #points += connected squares times the number of crowns as shown in the crownSquare
    #print("You have "+str(points)+ " points!")
    print(str(points)+ " #"+str(n+1))
