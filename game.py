import pygame
from entities import *
from map import Map
from interface import *
from rounds import Rounds

LENGTH = 1440
WIDTH = 810

#shape to point conversions
score = {
    "Triangle": 3,
    "Squarelet": 1,
    "Square": 4,
    "Pentagon": 5,
    "Hexagon": 6,
    "Heptagon": 7,
    "Nonagon": 9
}

class Game:
    def __init__(self, id=-1):
        #connection
        self.id = id
        self.ready = False


        self.map = Map()

        self.player_container = [Player()]
        self.bullet_container = []
        self.rounds = Rounds(self.map)

        self.particles = []
        self.emps = []

        self.window = pygame.display.set_mode((LENGTH, WIDTH))
        pygame.display.set_caption("Arcade Game")
        
        self.charge_bar = 0 #max is a thousand
        self.charge_bar_max = 500
        self.screen_shake = 0

        self.game_color = [100,100,100]

    #connection
    def connected(self):
        return self.ready

    def draw(self, n):
        self.window.fill(self.game_color)
        if not self.player_container[n].dead:
            scroll = self.player_container[n].scroll

            if self.screen_shake > 0:
                scroll[0] += random.randint(0,16) - 8
                scroll[1] += random.randint(0,16) - 8

            self.map.draw(self.window, scroll)

            self.rounds.draw(self.window, self.game_color, scroll)

            #charge bar
            bar_length = 1152
            self.window.blit(bar(self.charge_bar, self.charge_bar_max, bar_length, 70, 0), (64*50//2 - bar_length//2 - scroll[0], 64*50//2 + bar_length//2 + 30 - scroll[1]))

            for p in self.player_container:
                if not p.dead:
                    p.draw(self.window)

            for s in self.rounds.shape_container:
                s.draw(self.window, scroll)

            #particles
            for particle in self.particles:
                pygame.draw.circle(self.window, (255,255,255), (int(particle[0][0] - scroll[0]), int(particle[0][1] - scroll[1])), int(particle[2]))
                self.window.blit(circle_surf(particle[2]*2, (20,20,20)), (int(particle[0][0] - scroll[0] - particle[2]*2), int(particle[0][1] - scroll[1]  - particle[2]*2)), special_flags=pygame.BLEND_RGB_ADD)

            #emps
            for emp in self.emps:
                if emp[1] > 0:
                    pygame.draw.circle(self.window, (255,255,255), (int(emp[0][0] - scroll[0]), int(emp[0][1] - scroll[1])), int(emp[1]), 10)

            for b in self.bullet_container:
                b.draw(self.window, scroll)

            self.window.blit(bar(self.player_container[n].hp, 100, 300, 50), (50,50))
        pygame.display.update()

    def update_inputs(self, inputs, n):
        if not self.player_container[n].dead:
            self.player_container[n].update(inputs, self.bullet_container, self.map)

    def update(self):
        self.rounds.update()

        if self.rounds.round_number == 0:
            self.charge_bar = 0

        #screen shake
        self.screen_shake = max(self.screen_shake - 0.5, 0)

        #particles
        self.particles[:] = [p for p in self.particles if p[3]]
        for particle in self.particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.1

            if particle[2] <= 0:
                particle[3] = False

        #emp
        for emp in self.emps:
            emp[1] += 12
            if emp[1] > 1500:
                self.emps.remove(emp)
            self.charge_bar = 0

        for p in self.player_container:
            p.scroll[0] += (self.player_container[0].pos[0] - self.window.get_width()/2 - p.scroll[0]) / 10
            p.scroll[1] += (self.player_container[0].pos[1] - self.window.get_height()/2 - p.scroll[1]) / 10


        #bullets 
        self.bullet_container[:] = [b for b in self.bullet_container if b.active]
        for b in self.bullet_container:
            #bullets that target shapes
            if b.target_shapes:
                for s in self.rounds.shape_container:
                    if b.polygon_collision(s.points):
                        s.health -= 1
                        s.last_hit = pygame.time.get_ticks()
                        if s.health == 0:
                            self.charge_bar += score[s.__class__.__name__]
                            if s.__class__.__name__ == "Square":
                                self.spawn_squarelets(s.pos,s.size/2)
                            elif s.__class__.__name__ == "Nonagon":
                                self.nonagon_death(s.pos, s.size, s.angle_pos)
                            s.active = False
                            self.shape_death(s.pos, s.size)
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
                        p.last_received_damage = pygame.time.get_ticks()
                        if b.__class__.__name__ == "Bullet":
                            b.active = False
                        if b.__class__.__name__ == "Wave":
                            p.add_force((
                                    b.radius /20 * math.cos(b.angle),
                                    b.radius /20 * math.sin(b.angle)
                                ),25,0,0)
                        p.hp -= 2.5

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
            
            for p in self.player_container:
                if p.polygon_collision(s1.points):
                    p.last_received_damage = pygame.time.get_ticks()
                    p.hp -= 0.5

            for emp in self.emps:
                if abs(dist(emp[0], s1.pos) - emp[1]) < 10:
                    s1.active = False
                    self.shape_death(s1.pos, s1.size)

        #charge_bar
        if self.charge_bar > self.charge_bar_max:
            self.player_emp()
            self.charge_bar = 0

        for player in self.player_container:
            if player.hp < 0:
                player.dead = True

    def reset(self):
        self.player_container = [Player()]
        self.bullet_container = []
        self.rounds = Rounds(self.map)
        self.particles = []
        self.game_color = [100,100,100]

    def spawn_squarelets(self, pos, size):
        s1 = Squarelet(pos,2,size)
        s2 = Squarelet(pos,2,size)
        s3 = Squarelet(pos,2,size)
        s4 = Squarelet(pos,2,size)

        scale = 10
        s1.add_force((0,scale),50,200,50)
        s2.add_force((scale,0),50,200,50)
        s3.add_force((0,-scale),50,200,50)
        s4.add_force((-scale,0),50,200,50)

        self.rounds.shape_container.append(s1)
        self.rounds.shape_container.append(s2)
        self.rounds.shape_container.append(s3)
        self.rounds.shape_container.append(s4)

    def nonagon_death(self, pos, size, angle):
        for i in range(9):
            self.bullet_container.append(Bullet(pos, 13, angle + 2*i*math.pi/9, False, size/3))
            self.bullet_container.append(Bullet(pos, 10, angle + 2*i*math.pi/9, False, size/3))
            self.bullet_container.append(Bullet(pos, 8, angle + 2*i*math.pi/9, False, size/3))

    def shape_death(self, pos, size):
        for i in range(40):
            self.particles.append(list([list(pos), ((random.randint(0,20) / 10-1)*3 * (1.5 - 5//size), (random.randint(0,20) / 10-1)*3 * (1.5 - 5//size)), min(random.randint(2,int(size)),6), True]))

    def player_emp(self):
        for p in self.player_container:
            self.emps.append([p.pos, 0])
            self.emps.append([p.pos, -170])
            self.emps.append([p.pos, -300])
        self.screen_shake = 15

    def is_game_over(self):
        game_over = True
        for p in self.player_container:
            if not p.dead:
                game_over = False
        return game_over

def circle_surf(radius, color):
    surf = pygame.Surface((radius*2, radius*2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0,0,0))
    return surf