import pygame

class Player:
    def __init__(self):
        self.pos = [300,300]
        self.speed = 2
        self.accel = 0.1

        self.curr_vel = [0,0]

        self.size = 30

    def draw(self, window):
        pygame.draw.circle(window, (255,255,255), self.pos, self.size)

    def update(self, inputs):
        target_vel = [0,0]

        if not (inputs["left"] and inputs["right"]):
            if inputs["left"]:
                target_vel[0] = -self.speed
            if inputs["right"]:
                target_vel[0] = self.speed
        if not (inputs["up"] and inputs["down"]):
            if inputs["up"]:
                target_vel[1] = -self.speed
            if inputs["down"]:
                target_vel[1] = self.speed
        
        if (abs(self.curr_vel[0] - target_vel[0]) < self.accel):
            self.curr_vel[0] = target_vel[0]
        elif (self.curr_vel[0] < target_vel[0]):
            self.curr_vel[0] += self.accel
        else:
            self.curr_vel[0] -= self.accel

        if (abs(self.curr_vel[1] - target_vel[1]) < self.accel):
            self.curr_vel[1] = target_vel[1]
        elif (self.curr_vel[1] < target_vel[1]):
            self.curr_vel[1] += self.accel
        else:
            self.curr_vel[1] -= self.accel

        vect = pygame.math.Vector2(self.curr_vel[0],self.curr_vel[1])

        self.pos[0] += vect[0]
        self.pos[1] += vect[1]
        

class Game:
    def __init__(self):
        self.player = Player()
        self.enemies = []
        self.map = [

        ]

    def draw(self, window):
        self.player.draw(window)

    def update(self, inputs):
        self.player.update(inputs)