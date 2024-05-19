import pygame
from entities import *
from map import Map

class Game:
    def __init__(self, length, width):
        self.enemies = []
        self.map = Map()

        a = Hexagon((300,300), 4, 30, None)
        b = Hexagon((300,400), 4, 30, a)
        c = Hexagon((300,500), 4, 30, b)
        d = Hexagon((300,600), 4, 30, c)
        e = Hexagon((300,700), 4, 30, d)
        f = Hexagon((300,800), 4, 30, e)
        g = Hexagon((300,900), 4, 30, f)

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
            Square((100,500),3,50),
            Nonagon((800,1200),5,30,3),  
            a,
            b,
            c,
            d,
            e,
            f,
            g
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
                            elif s.__class__.__name__ == "Nonagon":
                                self.nonagon_death(s.pos, s.size, s.angle_pos)
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
            elif s1.__class__.__name__ == "Nonagon":
                s1.update(self.bullet_container, self.map)
            else:
                s1.update(self.player_container)
            for j in range(i+1, len(self.shape_container)):
                s2 = self.shape_container[j]
                # if s1.__class__.__name__ == "Hexagon" and s2.__class__.__name__ == "Hexagon":
                #     continue
                

                mult = 1/7
                forces = calc_collision(s1.size, s1.pos, s1.disp, s2.size, s2.pos, s2.disp)
                if dist(s1.pos, s2.pos) < s1.size + s2.size:
                    if s1.size > s2.size:
                        s2.add_force((forces[1][0] * mult, forces[1][1] * mult),50,100,50)
                    elif s2.size < s1.size:
                        s1.add_force((forces[0][0] * mult, forces[0][1] * mult),50,100,50)
                    else:
                        s1.add_force((forces[0][0] * mult, forces[0][1] * mult),50,100,50)
                        s2.add_force((forces[1][0] * mult, forces[1][1] * mult),50,100,50)
                        

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

    def nonagon_death(self, pos, size, angle):
        for i in range(9):
            self.bullet_container.append(Bullet(pos, 13, angle + 2*i*math.pi/9, False, size/3))
            self.bullet_container.append(Bullet(pos, 10, angle + 2*i*math.pi/9, False, size/3))
            self.bullet_container.append(Bullet(pos, 8, angle + 2*i*math.pi/9, False, size/3))
