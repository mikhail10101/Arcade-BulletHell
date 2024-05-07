import pygame

TILESIZE = 64

class Map:
    def __init__(self, tile_size = TILESIZE):
        self.tile_size = tile_size
        self.map_values = [

        ]

        #initialize map values
        self.map_values.append([1] * 60)
        temp = [1] + [0]*58 + [1]
        for i in range(40):
            self.map_values.append(temp[:])
        self.map_values.append([1] * 60)

    def draw(self, window):
        for r in range(len(self.map_values)):
            for c in range(len(self.map_values[0])):
                if self.map_values[r][c] == 1:
                    pygame.draw.rect(window, (255,255,255), (r*TILESIZE, c*TILESIZE, TILESIZE, TILESIZE))
