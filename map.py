import pygame

TILESIZE = 64

class Map:
    def __init__(self, tile_size = TILESIZE):
        self.tile_size = tile_size
        self.map_values = []

        #initialize map values
        self.map_values.append([1] * 60)
        temp = [1] + [0]*58 + [1]
        for i in range(40):
            self.map_values.append(temp[:])
        self.map_values.append([1] * 60)

    def draw(self, window, offset=(0,0)):
        for r in range(len(self.map_values)):
            for c in range(len(self.map_values[0])):
                if self.map_values[r][c] == 1:
                    pygame.draw.rect(window, (255,255,255), (r*TILESIZE - offset[0], c*TILESIZE - offset[1], TILESIZE, TILESIZE))

    def is_off_grid(self, pos):
        return not (0 <= pos[0] <= self.tile_size * len(self.map_values)
            and (0 <= pos[1] <= self.tile_size * len(self.map_values[0])))

    def is_in_wall(self,pos):
        if not self.is_off_grid(pos):
            x = int(pos[0] // TILESIZE)
            y = int(pos[1] // TILESIZE)
            return self.map_values[x][y] == 1
        return False
        