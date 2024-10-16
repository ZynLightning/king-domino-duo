import cv2 as cv
from findPatches import Patches, biomes
from templateSearch import Template_Searcher
biome = biomes()
patch=Patches()
ts = Template_Searcher()

#point count for one board:
boardNumber=input("Which board do you want counted?\n")
biome.findBiomes(f"boards/{boardNumber}.jpg")
board=biome.findBoard()
crownList=ts.program(cv.imread(f"boards/{boardNumber}.jpg"),board)
patchList=patch.wildfire()
points = 0
for entry in crownList[1]:# for every entry in the crownList
    for list in patchList: #for every entry in patchList
        if entry in list: #if the entry from crownlist is in that patch:
            points+=len(list)*crownList[0][entry[0],entry[1]] #points += connected squares times the number of crowns as shown in the crownSquare
print("You have "+str(points)+ " points!")
"""
#count points for all 74 boards:
for n in range(74):
    boardNumber=str(n+1)#input("Which board do you want counted?\n")
    biome.findBiomes(f"boards/{boardNumber}.jpg")
    board=biome.findBoard()
    crownList=ts.program(cv.imread(f"boards/{boardNumber}.jpg"),board)
    blobList=patch.wildfire()
    
    points = 0
    for entry in crownList[1]:# for every entry in the crownList
        for list in blobList: #for every entry in bloblist
            if entry in list: #if the entry from crownlist is in that blob:
                points+=len(list)*crownList[0][entry[0],entry[1]] #points += connected squares times the number of crowns as shown in the crownSquare
    #print("You have "+str(points)+ " points!")
    print(str(points)+ " #"+str(n+1))
"""
