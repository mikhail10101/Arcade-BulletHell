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
    def __init__(self, id=-2):
        #connection
        self.id = id
        self.ready = False

        self.map = Map()

        self.player_container = [Player()]
        if not id==-2:
            self.player_container.append(Player())

        self.bullet_container = []
        self.rounds = Rounds(self.map)
        self.particles = []
        self.emps = []
        
        self.charge_bar = 0
        self.charge_bar_max = 500
        self.screen_shake = 0

        self.score = 0

        self.game_color = [100,100,100]

        self.player_pers = 0

        self.processed_particles = []

    #connection
    def connected(self):
        return self.ready

    def draw(self, screen, n):
        window = pygame.Surface((LENGTH, WIDTH))
        window.fill(self.game_color)

        scroll = self.player_container[n].scroll
        

        if self.screen_shake > 0:
            scroll[0] += random.randint(0,16) - 8
            scroll[1] += random.randint(0,16) - 8

        self.map.draw(window, scroll)

        self.rounds.draw(window, self.game_color, scroll)

        #charge bar
        bar_length = 1152
        window.blit(bar(self.charge_bar, self.charge_bar_max, bar_length, 70, 0), (64*50//2 - bar_length//2 - scroll[0], 64*50//2 + bar_length//2 + 30 - scroll[1]))

        for i in range(len(self.player_container)):
            if self.player_container[i].alive:
                if self.player_pers == i:
                    self.player_container[i].draw(window, True)
                else:
                    self.player_container[i].draw(window, False, self.player_container[self.player_pers].scroll)

        for s in self.rounds.shape_container:
            s.draw(window, scroll)

        #particles
        for particle in self.processed_particles:
            pygame.draw.circle(window, (200,200,200), (int(particle[0][0] - scroll[0]), int(particle[0][1] - scroll[1])), int(particle[2]))
            window.blit(circle_surf(particle[2]*2, (20,20,20)), (int(particle[0][0] - scroll[0] - particle[2]*2), int(particle[0][1] - scroll[1]  - particle[2]*2)), special_flags=pygame.BLEND_RGB_ADD)

        #emps
        for emp in self.emps:
            if emp[1] > 0:
                pygame.draw.circle(window, (255,255,255), (int(emp[0][0] - scroll[0]), int(emp[0][1] - scroll[1])), int(emp[1]), 10)

        for b in self.bullet_container:
            b.draw(window, scroll)

        #player health
        window.blit(bar(self.player_container[n].hp, 100, 300, 50), (50,50))

        #display score
        f = pygame.font.SysFont("Times New Roman", 80)
        score_text = f.render(str(self.score), True, (255,255,255))
        window.blit(score_text, (LENGTH - score_text.get_width() - 50,20))

        screen.blit(window, (0,0))

    def update_inputs(self, inputs, n):
        if self.player_container[n].alive:
            self.player_container[n].update(inputs, self.bullet_container, self.map)

    def client_update(self):
        for p in self.particles:
            self.processed_particles.append(p)
        
        self.particles = []

        #particles
        self.processed_particles[:] = [p for p in self.processed_particles if p[3]]
        for particle in self.processed_particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.1

            if particle[2] <= 0:
                particle[3] = False

    def update(self):
        alive_players = [p for p in self.player_container if p.alive]

        self.rounds.update()

        if self.rounds.round_number == 0:
            self.charge_bar = 0

        #screen shake
        self.screen_shake = max(self.screen_shake - 0.5, 0)

        #emp
        for emp in self.emps:
            emp[1] += 12
            if emp[1] > 2000:
                self.emps.remove(emp)
            self.charge_bar = 0

        #player
        for p in self.player_container:
            p.scroll[0] += (p.pos[0] - LENGTH/2 - p.scroll[0]) / 10
            p.scroll[1] += (p.pos[1] - WIDTH/2 - p.scroll[1]) / 10

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
                            self.score += score[s.__class__.__name__]
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
                    if p.alive:
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
                s1.update(alive_players, self.bullet_container)
            elif s1.__class__.__name__ == "Pentagon":
                s1.update(alive_players, self.map)
            elif s1.__class__.__name__ == "Nonagon":
                s1.update(self.bullet_container, self.map)
            else:
                s1.update(alive_players)
            
            for p in self.player_container:
                if p.alive:
                    if p.polygon_collision(s1.points):
                        p.last_received_damage = pygame.time.get_ticks()
                        p.hp -= 1

            for emp in self.emps:
                if abs(dist(emp[0], s1.pos) - emp[1]) < 10:
                    s1.active = False
                    self.score += score[s1.__class__.__name__]
                    self.shape_death(s1.pos, s1.size)


        #charge_bar
        if self.charge_bar > self.charge_bar_max:
            self.player_emp()
            self.charge_bar = 0

        for player in self.player_container:
            if player.hp < 0:
                player.alive = False

    def reset(self):
        self.player_container = [Player()]
        self.bullet_container = []
        self.rounds = Rounds(self.map)
        self.particles = []
        self.game_color = [100,100,100]
        self.score = 0

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
        for i in range(10):
            self.particles.append(list([list(pos), ((random.randint(0,20) / 10-1)*3 * (1.5 - 5//size), (random.randint(0,20) / 10-1)*3 * (1.5 - 5//size)), min(random.randint(1,int(size)),4), True]))

    def player_emp(self):
        for p in self.player_container:
            self.emps.append([p.pos, 0])
            self.emps.append([p.pos, -170])
            self.emps.append([p.pos, -300])
        self.screen_shake = 15

    def is_game_over(self):
        game_over = True
        for p in self.player_container:
            if p.alive:
                game_over = False
        return game_over

def circle_surf(radius, color):
    surf = pygame.Surface((radius*2, radius*2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0,0,0))
    return surf