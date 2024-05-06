import pygame
import math

class Player:
    def __init__(self):
        #draw
        self.size = 30

        #movement
        self.pos = [300,300]
        self.speed = 4
        self.accel = 0.1
        self.deccel = 0.05
        self.curr_vel = [0,0]

        #shot in milliseconds
        self.last_shot = -1000
        self.shot_interval = 100
        

    def draw(self, window):
        pygame.draw.circle(window, (255,255,255), self.pos, self.size)

    def update(self, inputs, bullets):
        current_time = pygame.time.get_ticks()

        #MOVEMENT
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
        
        if (target_vel[0] != 0):
            if (abs(self.curr_vel[0] - target_vel[0]) < self.accel):
                self.curr_vel[0] = target_vel[0]
            elif (self.curr_vel[0] < target_vel[0]):
                self.curr_vel[0] += self.accel
            else:
                self.curr_vel[0] -= self.accel
        else:
            if (abs(self.curr_vel[0] - target_vel[0]) < self.deccel):
                self.curr_vel[0] = target_vel[0]
            elif (self.curr_vel[0] < target_vel[0]):
                self.curr_vel[0] += self.deccel
            else:
                self.curr_vel[0] -= self.deccel

        if (target_vel[1] != 0):
            if (abs(self.curr_vel[1] - target_vel[1]) < self.accel):
                self.curr_vel[1] = target_vel[1]
            elif (self.curr_vel[1] < target_vel[1]):
                self.curr_vel[1] += self.accel
            else:
                self.curr_vel[1] -= self.accel
        else:
            if (abs(self.curr_vel[1] - target_vel[1]) < self.deccel):
                self.curr_vel[1] = target_vel[1]
            elif (self.curr_vel[1] < target_vel[1]):
                self.curr_vel[1] += self.deccel
            else:
                self.curr_vel[1] -= self.deccel

        self.pos[0] += self.curr_vel[0]
        self.pos[1] += self.curr_vel[1]

        #SHOOT
        if inputs["click"]:
            if  current_time > self.last_shot + self.shot_interval:
                mx, my = inputs["click_pos"]

                dx = mx - self.pos[0]
                dy = my - self.pos[1]
                rads = math.atan2(dy,dx)

                bullets.append(Bullet(self.pos, 15, rads))

                self.last_shot = current_time


class Bullet:
    def __init__(self, pos, speed, angle):
        self.pos = list(pos)
        self.speed = speed
        self.angle = angle
        self.radius = 10

        self.active = True
        self.createTime = pygame.time.get_ticks()

    def update(self):
        self.pos[0] += self.speed * math.cos(self.angle)
        self.pos[1] += self.speed * math.sin(self.angle)

        if self.createTime + 5000 < pygame.time.get_ticks():
            self.active = False

    def draw(self, window):
        pygame.draw.circle(window, (255,255,255), self.pos, self.radius)



