import pygame
from entities import *

TILESIZE = 64
CENTER = (30*TILESIZE, 30*TILESIZE)

class Rounds:
    def __init__(self):
        self.shape_container = [

        ]
        self.round_number = 0
        self.mode = 0
        self.round_end_time = 0 

    def update(self):
        #preround
        if self.mode == 0:
            self.start_round()
            self.mode = 1
        #in round
        elif self.mode == 1:
            if self.is_round_done():
                self.mode = 2
                self.round_end_time = pygame.time.get_ticks()
        #end round
        elif self.mode == 2:
            if pygame.time.get_ticks() > self.round_end_time + 5000:
                self.mode = 0
                self.round_number += 1


    def spawn_triangles(self, tilepos, speed, size, amount):
        for i in range(amount):
            self.shape_container.append(Triangle((tilepos[0] * TILESIZE + random.random()*200, tilepos[1] * TILESIZE + random.random()*200), speed, size))

    def rec(self, pos, speed, size, amount):
        if amount == 1:
            h = Hexagon((pos), speed, size, None)
            self.shape_container.append(h)
            return h
        
        vect = pygame.math.Vector2(CENTER[0]-pos[0], CENTER[1]-pos[1])
        vect.normalize_ip()
        vect.scale_to_length(100)
        h = Hexagon(pos, speed, size, self.rec((pos[0] + vect[0], pos[1]+vect[1]), speed, size, amount-1))
        self.shape_container.append(h)
        return h

    def spawn_hexagons(self, pos, speed, size, amount):
         
        self.rec((pos[0]*TILESIZE, pos[1]*TILESIZE), speed, size, amount, )
    
    def spawn_pentagon(self, tilepos, size):
        self.shape_container.append(Pentagon(
            (tilepos[0] * TILESIZE, tilepos[1] * TILESIZE), size
        ))

    def is_round_done(self):
        return len(self.shape_container) == 0
    
    def start_round(self):
        self.spawn_triangles((30,30),3,20,self.round_number)
        self.spawn_pentagon((15,15),80)
        self.spawn_pentagon((48,48),120)