import pygame
from entities import *

class Rounds:
    def __init__(self):        
        self.shape_container = [
            Pentagon((2800,3000),80),
            Pentagon((800,800),160),
            Square((2100,200),3,50),
            Nonagon((2400,2400),5,30,3),  
            Heptagon((100,500),8,50)
        ]

        self.spawn_hexagons((-1000,-1000),8,30,7)
        self.spawn_triangles((2400,2400),3,20,15)

    def spawn_triangles(self, pos, speed, size, amount):
        for i in range(amount):
            self.shape_container.append(Triangle(pos, speed, size))

    def spawn_hexagons(self, pos, speed, size, amount):
        if amount == 1:
            h = Hexagon(pos, speed, size, None)
            self.shape_container.append(h)
            return h
        h = Hexagon(pos, speed, size, self.spawn_hexagons((pos[0], pos[1]-80), speed, size, amount-1))
        self.shape_container.append(h)
        return h