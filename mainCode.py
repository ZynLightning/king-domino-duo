from findBlobs import *
#print(findBlobs("Boards/1.jpg"))

boardNumber=input("Which board do you want counted?")
Blobs=findBlobs("boards/"+str(boardNumber)+".jpg")[0]
print(Blobs)