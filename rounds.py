import pygame
from entities import *

TILESIZE = 64
CENTER = (25*TILESIZE, 25*TILESIZE)

class Rounds:
    def __init__(self, map):
        self.shape_container = [

        ]
        self.round_number = 7
        self.mode = 0
        self.round_end_time = 0
        self.map = map

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


    
    def rec(self, pos, speed, size, amount):
        if amount == 1:
            h = Hexagon((pos), speed, size, None)
            self.shape_container.append(h)
            return h
        
        vect = pygame.math.Vector2(CENTER[0]-pos[0], CENTER[1]-pos[1])
        vect.normalize_ip()
        vect.scale_to_length(size*5)
        h = Hexagon((pos[0] - amount*vect[0],pos[1] - amount*vect[1]), speed, size, self.rec(pos, speed, size, amount-1))
        self.shape_container.append(h)
        return h




    def spawn_triangles(self, speed, size, amount):
        tilepos = self.map.random_1()
        for i in range(amount):
            self.shape_container.append(Triangle((tilepos[0] * TILESIZE + random.random()*200, tilepos[1] * TILESIZE + random.random()*200), speed, size))

    def spawn_square(self, speed, size):
        tilepos = self.map.random_1()
        self.shape_container.append(Square(
            (tilepos[0] * TILESIZE, tilepos[1] * TILESIZE), speed, size
        ))

    def spawn_pentagon(self, size):
        tilepos = self.map.random_1()
        self.shape_container.append(Pentagon(
            (tilepos[0] * TILESIZE, tilepos[1] * TILESIZE), size
        ))
    
    def spawn_hexagons(self, speed, size, amount):
        tilepos = self.map.random_1()
        self.rec((tilepos[0]*TILESIZE, tilepos[1]*TILESIZE), speed, size, amount)

    def spawn_heptagon(self, speed, size):
        tilepos = self.map.random_1()
        self.shape_container.append(Square(
            (tilepos[0] * TILESIZE, tilepos[1] * TILESIZE), speed, size
        ))
    
    def spawn_nonagon(self, speed, size):
        tilepos = self.map.random_1()
        self.shape_container.append(Nonagon(
            (tilepos[0] * TILESIZE, tilepos[1] * TILESIZE), speed, size,
            math.atan2(CENTER[1] - tilepos[1] * TILESIZE, CENTER[0] - tilepos[0] * TILESIZE)
        ))





    def is_round_done(self):
        return len(self.shape_container) == 0
    
    def start_round(self):

        if self.round_number == 1:
            self.spawn_triangles(3,10,20)
            self.spawn_triangles(3,10,20)
            self.spawn_triangles(3,10,20)

        elif self.round_number == 2:
            self.spawn_square(3,40)
            self.spawn_square(3,50)
            self.spawn_square(3,40)

        elif self.round_number == 3:
            self.spawn_triangles(3,10,20)
            self.spawn_triangles(3,10,20)   
            self.spawn_square(3,40)
            self.spawn_square(3,50)         

        elif self.round_number == 4:
            self.spawn_pentagon(80)
            self.spawn_pentagon(120)
            self.spawn_pentagon(50)
            self.spawn_pentagon(80)

        elif self.round_number == 5:
            self.spawn_pentagon(80)
            self.spawn_pentagon(120)
            self.spawn_triangles(3,10,20)
            self.spawn_triangles(3,10,20)   
            self.spawn_square(3,40)

        elif self.round_number == 6:
            self.spawn_hexagons(7,30,10)
            self.spawn_hexagons(7,40,10)
            self.spawn_hexagons(7,20,20)

        elif self.round_number == 7:
            self.spawn_nonagon(3,30)
            self.spawn_nonagon(5,40)
            self.spawn_nonagon(4,35)
            self.spawn_nonagon(7,30)


        # self.spawn_triangles(3,10,50)
        # self.spawn_square(3,30)
        # self.spawn_pentagon(80)
        # self.spawn_pentagon(120)
        # self.spawn_hexagons(3,30,10)
        # self.spawn_heptagon(3,30)
        # self.spawn_nonagon(3,30)