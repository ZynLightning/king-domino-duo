import numpy as np
import cv2 as cv

#   Template match class
#   The function of this class is to take in the tile, the number of the tile, and a grid
#   containing which type the tile had.
class Template_Searcher:

    #   Loops through each tile and check for crowns.
    def program(self, game, grid):
        self.grid = np.zeros((5,5), dtype=int)
        self.crown_list = []
        for row in range(5):
            for col in range(5):

                ys, ye, xs, xe = ((row+1)*100)-100, ((row+1)*100), ((col+1)*100)-100, ((col+1)*100)

                tile = game[ys:ye, xs:xe]
                tile_number = [row, col]
                output = self.crown_matching(tile, tile_number, grid)
        
        return output


    #   using tile, tile number and a grid to pick a template type.
    def crown_matching(self, tile, tile_number, grid):
        templates = self.choose_template(tile_number, grid)
        method = getattr(cv, 'TM_CCOEFF_NORMED')
        
        full_sorted = []
        
        #   Goes through choosen templates.
        for template in templates:
            res = cv.matchTemplate(tile, template, method)  #   Result from template matching.
            
            coords = self.get_crown_coords(res)
            sorted = self.sort_coords(coords)

            # if sorted != None:
            for element in sorted:
                full_sorted.append(element) if len(sorted) > 0 else 0
        
        self.insert_crowns_found(full_sorted, tile_number) if len(full_sorted) > 0 else 0

        output = [self.grid, self.crown_list]
        return output
    
    #   Add one to val depending on the amount of crowns found on a tile.
    #   val is then added to a grid containing the games crown and location.
    def insert_crowns_found(self, input, tile_number):
        m = tile_number[0]
        n = tile_number[1]
        val = 0

        for element in input:
            val += 1

        self.grid[m, n] = val
        self.crown_list.append(tile_number)
    
    #   Sorts out repeating crowns from the found coordinates.
    def sort_coords(self, coords):
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

    #   Find all coordinates of pixel with a threshold above 0.7 from the result.
    def get_crown_coords(self, res):
        coords = []
        threshold = 0.7
        rows, cols = res.shape

        #   Goes though each pixel in result, stores pixel coords in coords.
        for y in range(rows):
                for x in range(cols):
                    pixel = res[y,x]
                    
                    if pixel > threshold:
                        coords.append([y,x])
        return coords
        

    #   Inspects the grid using the tile number being looked at to find biome and choose tile type.
    def choose_template(self, tile_number, grid):
        row = tile_number[0]
        col = tile_number[1]
        current_type = grid[row, col]
        output = []

        if current_type == 'O':
            output = self.ocean
        elif current_type == 'G':
            output = self.grass
        elif current_type == 'F':
            output = self.forest
        elif current_type == 'A':
            output = self.field
        elif current_type == 'W':
            output = self.waste
        elif current_type == 'M':
            output = self.mine
        return output
        

    #   From __init__ the template list is created using the templates of each biome.
    def make_templates(self, image_source):
        template_0 = cv.imread(image_source)
        template_90 = cv.rotate(template_0, cv.ROTATE_90_CLOCKWISE)
        template_180 = cv.rotate(template_0, cv.ROTATE_180)
        template_270 = cv.rotate(template_0, cv.ROTATE_90_COUNTERCLOCKWISE)
        return [template_0, template_90, template_180, template_270]
        
    def __init__(self) -> None:
        src = 'templates/'
        self.ocean = self.make_templates(f'{src}ocean.tif')
        self.grass = self.make_templates(f'{src}grass.tif')
        self.forest = self.make_templates(f'{src}forest.tif')
        self.field = self.make_templates(f'{src}agri.tif')
        self.waste = self.make_templates(f'{src}wasteland.tif')
        self.mine = self.make_templates(f'{src}wasteland.tif')

