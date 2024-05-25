import pygame
from entities import *
from map import Map
from interface import *
from rounds import Rounds

class Game:
    def __init__(self, length, width):
        self.enemies = []
        self.map = Map()

        self.player_container = [Player()]
        self.bullet_container = []
        self.rounds = Rounds(self.map)

        self.window = pygame.display.set_mode((length, width))
        pygame.display.set_caption("Arcade Game")

        self.scroll = [0,0]

        self.game_color = [100,100,100]

    
    def draw(self):
        self.window.fill(self.game_color)

        self.map.draw(self.window, self.scroll)

        for p in self.player_container:
            p.draw(self.window, self.scroll)

        for s in self.rounds.shape_container:
            s.draw(self.window, self.scroll)

        for b in self.bullet_container:
            b.draw(self.window, self.scroll)

        self.window.blit(bar(self.player_container[0].hp, 100, 200, 50), (50,50)) 
        self.rounds.draw(self.window)
        pygame.display.update()

    def update(self, inputs):
        self.rounds.update()

        for p in self.player_container:
            p.update(inputs, self.bullet_container, self.map, self.scroll)

        #bullets 
        self.bullet_container[:] = [b for b in self.bullet_container if b.active]
        for b in self.bullet_container:
            #bullets that target shapes
            if b.target_shapes:
                for s in self.rounds.shape_container:
                    if b.polygon_collision(s.points):
                        s.health -= 1
                        if s.health == 0:
                            if s.__class__.__name__ == "Square":
                                self.spawn_squarelets(s.pos,s.size/2)
                            elif s.__class__.__name__ == "Nonagon":
                                self.nonagon_death(s.pos, s.size, s.angle_pos)
                            s.active = False
                        b.active = False
                        break
            #bullets that target players
            else:
                #waves shield shapes from bullets
                if b.__class__.__name__ == "Wave":
                    for newb in self.bullet_container:
                        if newb.__class__.__name__ == "Bullet" and newb.target_shapes:
                            if b.collision(newb.pos, newb.radius):
                                newb.active = False
                for p in self.player_container:
                    if b.collision(p.pos, p.size):
                        if b.__class__.__name__ == "Bullet":
                            b.active = False
                            p.hp -= 1
                        if b.__class__.__name__ == "Wave":
                            p.add_force((
                                    b.radius /20 * math.cos(b.angle),
                                    b.radius /20 * math.sin(b.angle)
                                ),25,0,0)
                            p.hp -= 0.1

            if self.map.is_oob(b.pos):
                b.active = False
            b.update()

        #shapes
        self.rounds.shape_container[:] = [s for s in self.rounds.shape_container if s.active]
        for i in range(len(self.rounds.shape_container)):
            s1 = self.rounds.shape_container[i]
            if s1.__class__.__name__ == "Squarelet" or s1.__class__.__name__ == "Heptagon":
                s1.update(self.player_container, self.bullet_container)
            elif s1.__class__.__name__ == "Pentagon":
                s1.update(self.player_container, self.map)
            elif s1.__class__.__name__ == "Nonagon":
                s1.update(self.bullet_container, self.map)
            else:
                s1.update(self.player_container)

            
            # for j in range(i+1, len(self.rounds.shape_container)):
            #     s2 = self.rounds.shape_container[j]

            #     mult = 1/2
            #     forces = calc_collision(s1.size, s1.pos, s1.disp, s2.size, s2.pos, s2.disp)
            #     if dist(s1.pos, s2.pos) < s1.size + s2.size:
            #         s1.vel = (0,0)
            #         s2.vel = (0,0)
            #         s1.add_force((forces[0][0] * mult, forces[0][1] * mult),50,0,0)
            #         s2.add_force((forces[1][0] * mult, forces[1][1] * mult),50,0,0)
            
            for p in self.player_container:
                if p.polygon_collision(s1.points):
                    p.hp -= 1    

        #update later on
        self.scroll[0] += (self.player_container[0].pos[0] - self.window.get_width()/2 - self.scroll[0]) / 10
        self.scroll[1] += (self.player_container[0].pos[1] - self.window.get_height()/2 - self.scroll[1]) / 10

    def spawn_squarelets(self, pos, size):
        s1 = Squarelet(pos,2,size)
        s2 = Squarelet(pos,2,size)
        s3 = Squarelet(pos,2,size)
        s4 = Squarelet(pos,2,size)

        self.rounds.shape_container.append(s1)
        self.rounds.shape_container.append(s2)
        self.rounds.shape_container.append(s3)
        self.rounds.shape_container.append(s4)

    def nonagon_death(self, pos, size, angle):
        for i in range(9):
            self.bullet_container.append(Bullet(pos, 13, angle + 2*i*math.pi/9, False, size/3))
            self.bullet_container.append(Bullet(pos, 10, angle + 2*i*math.pi/9, False, size/3))
            self.bullet_container.append(Bullet(pos, 8, angle + 2*i*math.pi/9, False, size/3))
