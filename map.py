import pygame
import math

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
    
    #angle in radians
    def raycast(self, start_pos, angle, max_distance):
        dirx = math.cos(angle)
        diry = math.sin(angle)

        unit_step_size = [
            math.sqrt( 1 + (diry/dirx)**2 ),
            math.sqrt( 1 + (dirx/diry)**2 )
        ]

        map_check = [int(i//self.tile_size) for i in start_pos]
        #step in index
        step = [0,0]
        #step in 1-component raylength
        ray_length = [0,0]

        #initlialize raylengths
        if dirx < 0:
            step[0] = -1
            ray_length[0] = (start_pos[0] - map_check[0] * self.tile_size) * unit_step_size[0] / self.tile_size
        else:
            step[0] = 1
            ray_length[0] = ((map_check[0] + 1) * self.tile_size - start_pos[0]) * unit_step_size[0] / self.tile_size
        if diry < 0:
            step[1] = -1
            ray_length[1] = (start_pos[1] - map_check[1] * self.tile_size) * unit_step_size[1] / self.tile_size 
        else:
            step[1] = 1
            ray_length[1] = ((map_check[1] + 1) * self.tile_size - start_pos[1]) * unit_step_size[1] / self.tile_size 

        tileFound = False
        curr_distance = 0
        while not tileFound and curr_distance < max_distance:
            if ray_length[0] < ray_length[1]:
                map_check[0] += step[0]
                curr_distance = ray_length[0]
                ray_length[0] += unit_step_size[0]
            else:
                map_check[1] += step[1]
                curr_distance = ray_length[1]
                ray_length[1] += unit_step_size[1]
            if 0 <= map_check[0] < len(self.map_values) and 0 <= map_check[1] < len(self.map_values[0]):
                if self.map_values[map_check[0]][map_check[1]] == 1:
                    tileFound = True
        
        if tileFound:
            return [
                start_pos[0] + curr_distance * dirx * self.tile_size,
                start_pos[1] + curr_distance * diry * self.tile_size
            ]
    
        return None