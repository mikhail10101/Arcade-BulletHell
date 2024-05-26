import pygame
from entities import *

TILESIZE = 64
CENTER = (25*TILESIZE, 25*TILESIZE)

class Rounds:
    def __init__(self, map):
        self.shape_container = []
        self.round_number = 0
        self.mode = 2
        self.round_end_time = pygame.time.get_ticks() - 3000
        self.map = map

        self.bg_normalize_time = 2000

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

    def draw(self,window, game_color):
        if self.mode == 2:
            if pygame.time.get_ticks() > self.round_end_time + 3000:
                f = pygame.font.SysFont("Consolas Bold", 600)
                text_finish = f.render(str(self.round_number+1), True, (255,255,255))
                window.blit(text_finish, (window.get_width()//2 - text_finish.get_width()//2, window.get_height()//2 - text_finish.get_height()//2))
                a = (pygame.time.get_ticks() - self.round_end_time - 3000)/2000
                if a <= 1:
                    game_color[0] = pygame.math.lerp(150,255,a)
                    game_color[1] = pygame.math.lerp(150,255,a)
                    game_color[2] = pygame.math.lerp(150,255,a)
            elif pygame.time.get_ticks() > self.round_end_time + 500:
                f = pygame.font.SysFont("Consolas Bold", 250)
                text_finish = f.render("CLEARED", True, (255,255,255))
                window.blit(text_finish, (window.get_width()//2 - text_finish.get_width()//2, window.get_height()//2 - text_finish.get_height()//2))
            elif pygame.time.get_ticks() > self.round_end_time:
                pass

        elif self.mode == 1:
            a = (pygame.time.get_ticks()-self.round_end_time-5000)/4000
            if a <= 1:
                game_color[0] = pygame.math.lerp(255,150,a)
                game_color[1] = pygame.math.lerp(255,150,a)
                game_color[2] = pygame.math.lerp(255,150,a)


    
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
            self.shape_container.append(Triangle((tilepos[0] * TILESIZE + random.random()*200 - 100, tilepos[1] * TILESIZE + random.random()*200 - 100), speed, size))

    def spawn_square(self, speed, size):
        tilepos = self.map.random_1()
        self.shape_container.append(Square(
            (tilepos[0] * TILESIZE + random.randint(0,TILESIZE-1) - TILESIZE, tilepos[1] * TILESIZE + random.randint(0,TILESIZE-1) - TILESIZE), speed, size
        ))

    def spawn_pentagon(self, size):
        tilepos = self.map.random_1_pentagon()
        self.shape_container.append(Pentagon(
            (tilepos[0] * TILESIZE + random.randint(0,TILESIZE-1) - TILESIZE, tilepos[1] * TILESIZE + random.randint(0,TILESIZE-1) - TILESIZE), size,
            math.atan2(CENTER[1] - tilepos[1] * TILESIZE, CENTER[0] - tilepos[0] * TILESIZE)
        ))
    
    def spawn_hexagons(self, speed, size, amount):
        tilepos = self.map.random_1()
        self.rec((tilepos[0]*TILESIZE + random.randint(0,TILESIZE-1) - TILESIZE, tilepos[1]*TILESIZE + random.randint(0,TILESIZE-1) - TILESIZE), speed, size, amount)

    def spawn_heptagon(self, speed, size):
        tilepos = self.map.random_1()
        self.shape_container.append(Heptagon(
            (tilepos[0] * TILESIZE + random.randint(0,TILESIZE-1) - TILESIZE, tilepos[1] * TILESIZE + random.randint(0,TILESIZE-1) - TILESIZE), speed, size
        ))
    
    def spawn_nonagon(self, speed, size):
        tilepos = self.map.random_1()
        self.shape_container.append(Nonagon(
            (tilepos[0] * TILESIZE + random.randint(0,TILESIZE-1) - TILESIZE, tilepos[1] * TILESIZE + random.randint(0,TILESIZE-1) - TILESIZE), speed, size,
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
            self.spawn_square(3,30)

        elif self.round_number == 3:
            self.spawn_triangles(3,10,20)
            self.spawn_triangles(3,10,20)   
            self.spawn_square(3,40)
            self.spawn_square(3,50)         

        elif self.round_number == 4:
            self.spawn_pentagon(60)
            self.spawn_pentagon(60)
            self.spawn_pentagon(60)
            self.spawn_pentagon(60)
            self.spawn_pentagon(60)
            

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
            self.spawn_heptagon(3,30)
            self.spawn_heptagon(3,30)
            self.spawn_heptagon(3,30)
            self.spawn_heptagon(3,30)

        elif self.round_number == 8:
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