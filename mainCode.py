from findBlobs import blobs, biomes

biome = biomes()
blob=blobs()

boardNumber="1"#input("Which board do you want counted?")
biome.findBiomes(f"boards/{boardNumber}.jpg")
board=biome.findBoard()
bloblist=blob.wildfire()
print(bloblist)
