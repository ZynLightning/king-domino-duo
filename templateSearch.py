#   1)  Go through each tile, one at a time and check for crown(s)
#   2)  If found, safe tile number, and coordinate of the crown(s).
#   3)  For each tile, make a counter that tells the number of crowns on a tile.
#   4)  When all tiles have been checked, draw a target symbol on the main image.
#   5)  Color the area of the crown instead of a target symbol.

import numpy as np
import cv2 as cv

#   Image setup
img = cv.imread('1.jpg')
edges = cv.Canny(img, 100, 300)   #   Canny version of game map

#   Template setup
template_0 = edges[108:129, 308:335]    #   Template, 0 degree roation
template_90 = cv.rotate(template_0, cv.ROTATE_90_CLOCKWISE)
template_180 = cv.rotate(template_0, cv.ROTATE_180)
template_270 = cv.rotate(template_90, cv.ROTATE_180)
templates = [template_0, template_90, template_180, template_270]   #   All possible templates
method = getattr(cv, 'TM_CCOEFF_NORMED')    #   Method for template matching

def find_coordinates(results):
    
    
    for result in results:
        j,i,l = result.shape
        output = []

        for y in range(j):
            for x in range(i):
                pixel = result[y,x]
                if pixel[0] == 255:
                    coord = [y,x]
                    output.append(coord)
    
    return output



def delete_noice(output):
    j,i,l = output.shape

    for y in range(j):
        for x in range(i):
            pixel = output[y,x]

            if pixel[0] == 255 and pixel[1] == 255 and pixel[2] == 255:

                crown_found = False

                position_list = [[y,x+1], [y+1,x], [y,x-1], [y-1,x]]
                
                for num in range(3):
                    p,q = position_list[num]
                    if p > y:
                        p = y
                    elif q > x:
                        q = x
                    r_pixel = output[p,q]

                    if pixel[0] == r_pixel[0] and pixel[1] == r_pixel[1] and pixel[2] == r_pixel[2]:
                        crown_found = True
                
                if crown_found == False:
                    output[y,x] = (0,0,0)
    return output

def get_threshold(res):
    j,i = res.shape
    output = np.zeros((j,i, 3), np.uint8)

    for y in range(j):
        for x in range(i):
            if 0.21 < res[y,x]:
                output[y,x] = (255,255,255)
    
    return output

def morp_open(threshold):
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(3,3))
    return cv.morphologyEx(threshold,cv.MORPH_OPEN,kernel)


#   To control value of amount of crown(s)
map_tile_values = np.zeros((5,5))
rows, cols = [5,5]
coordinates = []

#   Go through each tile, find crowns, save their correct coordinate.
for row in range(rows):
    # print(f"Row: {row}")

    for col in range(cols):

        # print(f"Column: {col}")
        tile = edges[((row+1)*100)-100:(row+1)*100,((col+1)*100)-100:(col+1)*100]
        tile_results = []
        
        # cv.imshow("Tiles", tile)
        # cv.waitKey()

        for template in templates:
            res = cv.matchTemplate(tile, template, method)
            threshold = get_threshold(res)
            reduced = delete_noice(threshold)
            tile_results.append(reduced)

            cv.imwrite(f"tiles/Reduced[{row+1},{col+1}].png", reduced)
        
        coordinates.append(find_coordinates(tile_results))
        
        print(coordinates)
        # cv.imshow("res", res)
        # cv.waitKey()
        






# cv.waitKey()



