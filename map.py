import pygame
import math
import random

TILESIZE = 64
OUTERSIZE = 50
INNERSIZE = 18

class Map:
    def __init__(self, tile_size = TILESIZE):
        self.tile_size = tile_size

        #initalize map
        start_index = (OUTERSIZE - INNERSIZE) // 2
        end_index = start_index + INNERSIZE

        self.map_values = [[2 if i == 0 or i == OUTERSIZE - 1 or j == 0 or j == OUTERSIZE - 1 else 0 if start_index <= i < end_index and start_index <= j < end_index else 1 for j in range(OUTERSIZE)] for i in range(OUTERSIZE)]

    def draw(self, window, offset=(0,0)):
        for r in range(len(self.map_values)):
            for c in range(len(self.map_values[0])):
                if self.map_values[r][c] == 0:
                    x = 20
                    pygame.draw.rect(window, (x,x,x), (r*TILESIZE - offset[0], c*TILESIZE - offset[1], TILESIZE, TILESIZE))

    def is_off_grid(self, pos):
        return not (0 <= pos[0] <= self.tile_size * len(self.map_values)
            and (0 <= pos[1] <= self.tile_size * len(self.map_values[0])))

    def is_oob(self,pos):
        if not self.is_off_grid(pos):
            x = int(pos[0] // TILESIZE)
            y = int(pos[1] // TILESIZE)
            return self.map_values[x][y] == 2
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
                if self.map_values[map_check[0]][map_check[1]] == 2:
                    tileFound = True
        
        if tileFound:
            return [
                start_pos[0] + curr_distance * dirx * self.tile_size,
                start_pos[1] + curr_distance * diry * self.tile_size
            ]
    
        return None
    
    def random_1(self):
        while True:
            a = random.randint(0, OUTERSIZE-1)
            b = random.randint(0, OUTERSIZE-1)

            if abs(a - OUTERSIZE//2) >= INNERSIZE//2 + 2 and abs(b - OUTERSIZE//2) >= INNERSIZE//2 + 2:
                if self.map_values[a][b] == 1:
                    return (a,b)
                
    def random_1_pentagon(self):
        while True:
            a = random.randint(0, OUTERSIZE-1)
            b = random.randint(0, OUTERSIZE-1)
            if (abs(a - OUTERSIZE//2) <= 5 + INNERSIZE//2) and (abs(b - OUTERSIZE//2) <= 5 + INNERSIZE//2) and not (
                (abs(a - OUTERSIZE//2) <= 2 + INNERSIZE//2) and (abs(b - OUTERSIZE//2) <= 2 + INNERSIZE//2)
            ):
                if self.map_values[a][b] == 1:
                    return (a,b)