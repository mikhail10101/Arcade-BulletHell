import pygame
from entities import *
from map import Map

class Game:
    def __init__(self, length, width):
        self.enemies = []
        self.map = Map()

        self.player_container = [Player()]
        self.bullet_container = []
        self.shape_container = [
            Pentagon((800,800),80),
            Pentagon((2000,2000),160),
            Triangle((400,400),2,20),
            Triangle((450,400),2,20), 
            Triangle((400,450),2,20), 
            Triangle((425,425),2,20), 
            Triangle((500,500),2,20), 
            Triangle((475,400),2,20), 
            Triangle((400,475),2,20), 
            Triangle((475,475),2,20),
            Square((100,500),3,50)
        ]

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
            if b.target_shapes:
                for s in self.shape_container:
                    if b.collision(s.points):
                        s.health -= 1
                        if s.health == 0:
                            if s.__class__.__name__ == "Square":
                                self.spawn_squarelets(s.pos,s.size/2,0,0)
                            s.active = False
                        b.active = False
                        break

            if self.map.is_in_wall(b.pos):
                b.active = False
            b.update()

        self.shape_container[:] = [s for s in self.shape_container if s.active]
        for i in range(len(self.shape_container)):
            s1 = self.shape_container[i]
            if s1.__class__.__name__ == "Squarelet":
                s1.update(self.player_container, self.bullet_container)
            elif s1.__class__.__name__ == "Pentagon":
                s1.update(self.player_container, self.map)
            else:
                s1.update(self.player_container)
            for j in range(i+1, len(self.shape_container)):
                s2 = self.shape_container[j]

                rads = math.atan2(s1.pos[0] - s2.pos[0], s1.pos[1] - s2.pos[1])
                if dist(s1.pos, s2.pos) < s1.size + s2.size:
                    if (s1.size > s2.size):
                        s2.add_force((s1.size/100 * math.cos(rads), s1.size/100 * math.sin(rads)),100,50,200)
                    elif (s2.size < s1.size):
                        s1.add_force((s2.size/100 * math.cos(rads), s2.size/100 * math.sin(rads)),100,50,200)
                    else:
                        s1.add_force((s2.size/100 * math.cos(rads), s2.size/100 * math.sin(rads)),100,50,200)
                        s2.add_force((s1.size/100 * math.cos(rads), -s1.size/100 * math.sin(rads)),100,50,200)

        #update later on
        self.scroll[0] += (self.player_container[0].pos[0] - self.window.get_width()/2 - self.scroll[0]) / 10
        self.scroll[1] += (self.player_container[0].pos[1] - self.window.get_height()/2 - self.scroll[1]) / 10

    def spawn_squarelets(self, pos, size, angle, force):
        s1 = Squarelet(pos,2,size)
        s2 = Squarelet(pos,2,size)
        s3 = Squarelet(pos,2,size)
        s4 = Squarelet(pos,2,size)

        a = 70
        b = 0

        self.shape_container.append(s1)
        self.shape_container.append(s2)
        self.shape_container.append(s3)
        self.shape_container.append(s4)
