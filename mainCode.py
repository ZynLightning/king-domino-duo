import cv2 as cv
from findBlobs import blobs, biomes
from templateSearch import Template_Searcher
biome = biomes()
blob=blobs()
ts = Template_Searcher()


boardNumber="1"#input("Which board do you want counted?")
biome.findBiomes(f"boards/{boardNumber}.jpg")
board=biome.findBoard()
crownList=ts.program(cv.imread(f"boards/{boardNumber}.jpg"),board)
blobList=blob.wildfire()

print(crownList)

print(blobList)
