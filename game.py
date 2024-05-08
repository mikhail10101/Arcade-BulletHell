import pygame
from entities import *
from map import Map

class Game:
    def __init__(self, length, width):
        self.enemies = []
        self.map = Map()

        self.player_container = [Player()]
        self.bullet_container = []
        #self.shape_container = [Squarelet((300,300),3,25),Triangle((400,400),2,30), Triangle((450,400),2,30), Triangle((400,450),2,30), Triangle((425,425),2,30), Triangle((500,500),2,30), Triangle((475,400),2,30), Triangle((400,475),2,30), Triangle((475,475),2,30)]
        self.shape_container = [Squarelet((300,300),3,25)]

        self.window = pygame.display.set_mode((length, width))
        pygame.display.set_caption("Arcade Game")

        self.scroll = [0,0]

    def draw(self):
        self.window.fill((0,0,0))

        self.map.draw(self.window, self.scroll)

        for p in self.player_container:
            p.draw(self.window, self.scroll)

        for b in self.bullet_container:
            b.draw(self.window, self.scroll)

        for s in self.shape_container:
            s.draw(self.window, self.scroll)

        pygame.display.update()

    def update(self, inputs):
        for p in self.player_container:
            p.update(inputs, self.bullet_container, self.map, self.scroll)

        self.bullet_container[:] = [b for b in self.bullet_container if b.active]
        for b in self.bullet_container:
            for s in self.shape_container:
                if b.collision(s.points):
                    b.active = False

            if self.map.is_in_wall(b.pos):
                b.active = False
            b.update()

        for i in range(len(self.shape_container)):
            #temp
            self.shape_container[i].update(self.player_container, self.bullet_container)

            for j in range(i+1, len(self.shape_container)):
                s1 = self.shape_container[i]
                s2 = self.shape_container[j]

                rads = math.atan2(s1.pos[0] - s2.pos[0], s1.pos[1] - s2.pos[1])
                if dist(s1.pos, s2.pos) < max(s1.size, s2.size):
                    if (s1.size < s2.size):
                        strength = s1.size/10
                        s1.add_force((strength * math.cos(rads), strength * math.sin(rads)))
                    elif (s2.size > s1.size):
                        strength = s2.size/10
                        s2.add_force((-strength * math.cos(rads), -strength * math.sin(rads)))
                    else:
                        strength = s1.size/10
                        s1.add_force((strength * math.cos(rads), strength * math.sin(rads)))
                        s2.add_force((-strength * math.cos(rads), -strength * math.sin(rads)))

        #update later on
        self.scroll[0] += (self.player_container[0].pos[0] - self.window.get_width()/2 - self.scroll[0]) / 10
        self.scroll[1] += (self.player_container[0].pos[1] - self.window.get_height()/2 - self.scroll[1]) / 10
