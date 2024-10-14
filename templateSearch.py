import numpy as np
import cv2 as cv

class Grid:
    def __init__(self) -> None:
        self.values = np.zeros((5,5), dtype=str)
        self.rows = self.values.shape[0]
        self.cols = self.values.shape[1]

class Kernel:
    def __init__(self) -> None:
        self.matrix = cv.getStructuringElement(cv.MORPH_ELLIPSE,(7,7))

class Tile_Type:
    def perform_open(self, kernel):
        self.open = cv.morphologyEx(self.mask, cv.MORPH_OPEN, kernel)

    def create_mask(self, hsv_input):
        self.mask = cv.inRange(hsv_input, self.min, self.max)

    def __init__(self, template_type, min, max) -> None:    #   inputs are max and min value of hsv.
        self.min = np.array(min)
        self.max = np.array(max)
        self.value = 0

        self.template_0 = cv.imread(template_type)
        self.template_90 = cv.rotate(self.template_0, cv.ROTATE_90_CLOCKWISE)
        self.template_180 = cv.rotate(self.template_0, cv.ROTATE_180)
        self.template_270 = cv.rotate(self.template_0, cv.ROTATE_90_COUNTERCLOCKWISE)
        self.templates = [self.template_0, self.template_90, self.template_180, self.template_270]

class Crown_Finder:
    def match(self, tile_input, template_input):
        return cv.matchTemplate(tile_input, template_input, self.method)
    
    def __init__(self) -> None:
        self.method = getattr(cv, 'TM_CCOEFF_NORMED')

class Crown:
    def __init__(self) -> None:
        self.grid = np.zeros((5,5), dtype=int)
        self.crown_list = []

board_source = 'King Domino dataset/Cropped and perspective corrected boards/'
game = cv.imread(f'{board_source}16.jpg')
hsv = cv.cvtColor(game, cv.COLOR_BGR2HSV)

#   Object setup
kernel = Kernel()
grid = Grid()

template_source = 'templates/'  #   Sets a source for template directory.
ocean = Tile_Type(f'{template_source}ocean.tif', [(144/255*180), 176, 0], [(157/255*180), 255, 255])
grass = Tile_Type(f'{template_source}grass.tif', [(53/255*180),0,130], [(87/255*180),255,255])
forest = Tile_Type(f'{template_source}forest.tif', [(49/255*180),0,0], [(87/255*180),210,85])
field = Tile_Type(f'{template_source}agri.tif', [(26/255*180),223,168], [(41/255*180),255,255])
waste = Tile_Type(f'{template_source}wasteland.tif', [(16/255*180),60,45], [(34/255*180),200,151])
mine1 = Tile_Type(None, [0,0,0],[(49),113,79])
mine2 = Tile_Type(None, [(228/255*180),0,0],[(242/255*180), 113,79])
mine = Tile_Type(f'{template_source}mine.tif', [],[])
table = Tile_Type(None, [(25/255*180), 166, 103], [(30/255*180), 255, 255])

finder = Crown_Finder()
crowns = Crown()


def find_tile_value(tile):
    rows = 100
    cols = 100

    ocean.create_mask(tile)
    ocean.perform_open(kernel.matrix)
    grass.create_mask(tile)
    grass.perform_open(kernel.matrix)
    forest.create_mask(tile)
    forest.perform_open(kernel.matrix)
    field.create_mask(tile)
    field.perform_open(kernel.matrix)
    waste.create_mask(tile)
    waste.perform_open(kernel.matrix)
    mine1.create_mask(tile)
    mine1.perform_open(kernel.matrix)
    mine2.create_mask(tile)
    mine2.perform_open(kernel.matrix)
    mine.mask = cv.bitwise_or(mine1.mask, mine2.mask, mask=None)
    table.create_mask(tile)
    table.perform_open(kernel.matrix)

    for y in range(rows):
        for x in range(cols):
            if ocean.open[y,x] != 0:
                ocean.value += 1
            elif grass.open[y,x] != 0:
                grass.value += 1
            elif forest.mask[y,x] != 0:
                forest.value += 1
            elif field.mask[y,x] != 0:
                field.value += 1
            elif waste.mask[y,x] != 0:
                waste.value += 1
            elif mine.mask[y,x] != 0:
                mine.value += 1
            elif table.mask[y,x] != 0:
                table.value += 1
    return [ocean.value, grass.value, forest.value, field.value, waste.value, mine.value]

def find_tile_type(values, row, col):
    if 800>np.max(values):
        grid.values[row, col] = 'K'
    elif ocean.value == np.max(values):
        grid.values[row, col] = 'O'
    elif grass.value == np.max(values):
        grid.values[row, col] = 'G'
    elif forest.value == np.max(values):
        grid.values[row, col] = 'F'
    elif field.value == np.max(values):
        grid.values[row, col] = 'A'
    elif waste.value == np.max(values):
        grid.values[row, col] = 'W'
    elif mine.value == np.max(values):
        grid.values[row, col] = 'M'

def choose_templates(row, col):
    current_type = grid.values[row,col]
    template = 0

    if current_type == 'O':
        template = ocean.templates
    elif current_type == 'G':
        template = grass.templates
    elif current_type == 'F':
        template = grass.templates
    elif current_type == 'A':
        template = field.templates
    elif current_type == 'W':
        template = waste.templates
    elif current_type == 'M':
        template = mine.templates
    
    return template

#   Returns result from each
def crown_matching(tile, tile_number, templates):
    coords = []
    output = []
    
    for template in templates:
        res = finder.match(tile, template)
        # cv.imshow("Res", res)
        # cv.waitKey()
        coords = get_crown_coords(res)
        sorted = sort_coords(coords)
        output.append(sorted) if len(sorted) > 0 else 0
        declare_found_crowns(sorted, tile_number) if len(sorted) > 0 else 0
    return output
        
def declare_found_crowns(sorted, tile):
    m = tile[0]
    n = tile[1]
    val = 0

    for sort in sorted:
        val += 1

    crowns.grid[m, n] = val
    crowns.crown_list.append(tile)

def sort_coords(coords):

    sorted = []
    counter = 0

    #   create to be sorted list.
    for coord in coords:
        yn = coord[0]
        xn = coord[1]

        if len(sorted) == 0:    #   if empty add first element found
            sorted.append(coord)
        elif len(sorted) > 0:
            current = sorted[counter]
            y = current[0]
            x = current[1]

            if xn - x > 10 or yn - y > 10:
                sorted.append(coord)
                counter += 1
        
    return sorted
        
def get_crown_coords(res):
    coords = []
    threshold = 0.7
    rows, cols = res.shape

    for y in range(rows):
            for x in range(cols):
                pixel = res[y,x]
                
                if pixel > threshold:
                    coords.append([y,x])

          
    return coords

def give_tile_coords(row,col):
    return ((row+1)*100)-100, ((row+1)*100), ((col+1)*100)-100, ((col+1)*100)

def reset_values():
    ocean.value = 0
    forest.value = 0
    field.value = 0
    grass.value = 0
    waste.value = 0
    mine.value = 0

def set_final_coordinate(y, x):

    pass


for row in range(grid.rows):
    for col in range(grid.cols):

        ys, ye, xs, xe = give_tile_coords(row, col)

        tile = game[ys:ye, xs:xe]
        hsv_tile = hsv[ys:ye, xs:xe]

        #   Find tile type and insert into tile_type
        values = find_tile_value(hsv_tile)
        find_tile_type(values, row, col)
        choosen_templates = choose_templates(row, col)

        if grid.values[row, col] != 'K':
            found_coords = crown_matching(tile, [row, col], choosen_templates)
        reset_values()  #   Note: important

print(crowns.crown_list)
