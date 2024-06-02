import pygame
from entities import *

TILESIZE = 64
CENTER = (25*TILESIZE, 25*TILESIZE)

LOWERCOLORBOUND = 100
UPPERCOLORBOUND = 160

class Rounds:
    def __init__(self, map):
        self.shape_container = []
        self.pentagons = []
        self.round_number = 0
        self.mode = 1
        self.round_end_time = pygame.time.get_ticks()
        self.round_interval = 12000
        self.map = map

        self.bg_normalize_time = 2000

        self.id_count = 0

    def update(self, time):
        print(self.id_count, len(self.shape_container))

        #preround
        if self.mode == 0:
            self.start_round()
            self.round_end_time = time
            self.mode = 1
        elif self.mode == 1:
            if time > self.round_end_time + self.round_interval:
                self.mode = 0
                self.round_number += 1
    

    def draw(self,window, offset, time):
        n = time - self.round_end_time
        if n < 1500:
            f = pygame.font.SysFont("MS Gothic", 600)
            text_finish = f.render(str(self.round_number), True, (255,255,255))
            window.blit(text_finish, (CENTER[0] - text_finish.get_width()//2 - offset[0], CENTER[1] - text_finish.get_height()//2 - offset[1]))

        

    def update_color(self, game_color, time):
        n = time - self.round_end_time
        half = self.round_interval//2
        if n <= half:
            val = pygame.math.lerp(UPPERCOLORBOUND,LOWERCOLORBOUND,max(min(n/half, 1),0))
            game_color[0] = val
            game_color[1] = val
            game_color[2] = val
        else:
            val = pygame.math.lerp(LOWERCOLORBOUND,UPPERCOLORBOUND,max(min((n-half)/half,1),0))
            game_color[0] = val
            game_color[1] = val
            game_color[2] = val


    
    def rec(self, pos, speed, size, amount):
        if amount == 1:
            h = Hexagon((pos), speed, size, None, self.get_id())
            self.shape_container.append(h)
            return h
        
        vect = pygame.math.Vector2(CENTER[0]-pos[0], CENTER[1]-pos[1])
        vect.normalize_ip()
        vect.scale_to_length(size*5)
        h = Hexagon((pos[0] - amount*vect[0],pos[1] - amount*vect[1]), speed, size, self.rec(pos, speed, size, amount-1), self.get_id())
        self.shape_container.append(h)
        return h


    def get_id(self):
        self.id_count += 1
        return self.id_count - 1

    def spawn_triangles(self, speed, size, amount):
        tilepos = self.map.random_1()
        for i in range(amount):
            self.shape_container.append(Triangle((tilepos[0] * TILESIZE + random.random()*200 - 100, tilepos[1] * TILESIZE + random.random()*200 - 100), speed, size, self.get_id()))

    def spawn_square(self, speed, size):
        tilepos = self.map.random_1()
        self.shape_container.append(Square(
            (tilepos[0] * TILESIZE + random.randint(0,TILESIZE-1) - TILESIZE, tilepos[1] * TILESIZE + random.randint(0,TILESIZE-1) - TILESIZE), speed, size, self.get_id()
        ))

    def spawn_pentagon(self, size):
        tilepos = self.map.random_1_pentagon()
        self.pentagons.append(Pentagon(
            (tilepos[0] * TILESIZE + random.randint(0,TILESIZE-1) - TILESIZE, tilepos[1] * TILESIZE + random.randint(0,TILESIZE-1) - TILESIZE), size,
            math.atan2(CENTER[1] - tilepos[1] * TILESIZE, CENTER[0] - tilepos[0] * TILESIZE), self.get_id()
        ))
    
    def spawn_hexagons(self, speed, size, amount):
        tilepos = self.map.random_1()
        self.rec((tilepos[0]*TILESIZE + random.randint(0,TILESIZE-1) - TILESIZE, tilepos[1]*TILESIZE + random.randint(0,TILESIZE-1) - TILESIZE), speed, size, amount)

    def spawn_heptagon(self, speed, size):
        tilepos = self.map.random_1()
        self.shape_container.append(Heptagon(
            (tilepos[0] * TILESIZE + random.randint(0,TILESIZE-1) - TILESIZE, tilepos[1] * TILESIZE + random.randint(0,TILESIZE-1) - TILESIZE), speed, size, self.get_id()
        ))
    
    def spawn_nonagon(self, speed, size):
        tilepos = self.map.random_1()
        self.shape_container.append(Nonagon(
            (tilepos[0] * TILESIZE + random.randint(0,TILESIZE-1) - TILESIZE, tilepos[1] * TILESIZE + random.randint(0,TILESIZE-1) - TILESIZE), speed, size,
            math.atan2(CENTER[1] - tilepos[1] * TILESIZE, CENTER[0] - tilepos[0] * TILESIZE), self.get_id()
        ))

    def spawn_squarelets(self, pos, size):
        s1 = Squarelet(pos,2,size, self.get_id())
        s2 = Squarelet(pos,2,size, self.get_id())
        s3 = Squarelet(pos,2,size, self.get_id())
        s4 = Squarelet(pos,2,size, self.get_id())

        scale = 10
        s1.add_force((0,scale),50,200,50)
        s2.add_force((scale,0),50,200,50)
        s3.add_force((0,-scale),50,200,50)
        s4.add_force((-scale,0),50,200,50)

        self.shape_container.append(s1)
        self.shape_container.append(s2)
        self.shape_container.append(s3)
        self.shape_container.append(s4)




    def is_round_done(self):
        return len(self.shape_container) == 0
    
    def start_round(self):
        match self.round_number:
            case 1:
                self.spawn_triangles(3,10,20)
                self.spawn_triangles(3,10,20)
                self.spawn_triangles(3,10,20)

            case 2:
                self.spawn_square(3,40)
                self.spawn_square(3,50)
                self.spawn_square(3,30)
                self.spawn_square(3,30)
                self.spawn_square(3,70)
                self.spawn_square(3,30)
                self.spawn_square(3,30)
                self.spawn_square(3,70)

            case 3:
                self.spawn_triangles(3,10,20)
                self.spawn_triangles(3,10,20)   
                self.spawn_square(3,40)
                self.spawn_square(3,50)
                self.spawn_square(3,30)         

            case 4:
                self.spawn_pentagon(60)
                self.spawn_pentagon(100)
                self.spawn_square(3,30)
                self.spawn_square(3,30)
                self.spawn_square(3,70)
                self.spawn_triangles(3,10,30)
                self.spawn_triangles(3,10,30)
                

            case 5:
                self.spawn_pentagon(80)
                self.spawn_pentagon(120)
                self.spawn_pentagon(120)
                self.spawn_triangles(3,10,20)
                self.spawn_triangles(3,10,20)   
                self.spawn_square(3,40)
                self.spawn_square(3,70)
                self.spawn_triangles(3,10,30)   
                self.spawn_square(3,50)

            case 6:
                self.spawn_hexagons(7,30,10)
                self.spawn_hexagons(7,40,10)
                self.spawn_hexagons(7,20,20)
                self.spawn_square(3,40)
                self.spawn_square(3,70)

            case 7:
                self.spawn_heptagon(3,30)
                self.spawn_heptagon(3,30)
                self.spawn_triangles(3,10,40)
                self.spawn_triangles(3,10,50)

            case 8:
                self.spawn_nonagon(3,30)
                self.spawn_nonagon(5,40)
                self.spawn_square(3,50)
                self.spawn_square(3,30)
                self.spawn_square(3,30)
                self.spawn_pentagon(120)
                self.spawn_pentagon(120)
            
            case 9:
                self.spawn_nonagon(3,30)
                self.spawn_nonagon(5,40)
                self.spawn_square(3,50)
                self.spawn_square(3,30)
                self.spawn_square(3,30)
                self.spawn_pentagon(120)
                self.spawn_pentagon(120)
                self.spawn_triangles(3,10,50)
                self.spawn_triangles(3,10,30)   
                self.spawn_square(3,40)
                self.spawn_square(3,70)
            
            case 10:
                self.spawn_nonagon(5,40)
                self.spawn_square(3,50)
                self.spawn_square(3,30)
                self.spawn_square(3,30)
                # self.spawn_pentagon(120)
                self.spawn_hexagons(7,40,10)
                self.spawn_hexagons(7,20,20)
                self.spawn_square(3,40)

            case _:
                for i in range(int((self.round_number - 8)*0.8)):
                    self.spawn_triangles(3,10,20)
                    self.spawn_square(3,30)
                    # self.spawn_pentagon(120)
                    self.spawn_hexagons(7,15,15)
                    self.spawn_nonagon(3,30)
                    self.spawn_heptagon(3,30)
                    self.spawn_nonagon(5,40)




        # self.spawn_triangles(3,10,50)
        # self.spawn_square(3,30)
        # self.spawn_pentagon(80)
        # self.spawn_hexagons(3,30,10)
        # self.spawn_heptagon(3,30)
        # self.spawn_nonagon(3,30)