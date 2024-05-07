import pygame
import math
from helper import *

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
        self.shot_interval = 333
        

    def draw(self, window, offset=(0,0)):
        pygame.draw.circle(window, (255,255,255), (int(self.pos[0] - offset[0]), int(self.pos[1] - offset[1])), self.size)

    def update(self, inputs, bullets, map, offset=(0,0)):
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
        
        phys_helper(self.curr_vel, target_vel, self.accel, self.deccel)

        self.move([self.pos[0] + self.curr_vel[0], self.pos[1] + self.curr_vel[1]], map)

        #SHOOT
        if inputs["click"]:
            if current_time > self.last_shot + self.shot_interval:
                mx, my = inputs["click_pos"]

                mx += offset[0]
                my += offset[1]

                dx = mx - self.pos[0]
                dy = my - self.pos[1]

                rads = math.atan2(dy,dx)

                bullets.append(Bullet(self.pos, 10, rads))

                self.last_shot = current_time

    def move(self, new_pos, map):
        i = int(self.pos[0] // map.tile_size)
        j = int(self.pos[1] // map.tile_size)
        newI = int(new_pos[0] // map.tile_size)
        newJ = int(new_pos[1] // map.tile_size)

        if 0 <= newI < len(map.map_values) and 0 <= newJ < len(map.map_values[0]):
            if (map.map_values[newI][newJ] == 1):
                if abs(i - newI) == 1 and abs(j - newJ) == 1:
                    print("RAWR")
                    if map.map_values[i][newJ] == 0:
                        self.pos[1] = new_pos[1]
                    elif map.map_values[newI][j] == 0:
                        self.pos[0] = new_pos[0]
                    else:
                        pass
                elif abs(j - newJ) == 1:
                    self.pos[0] = new_pos[0]
                else:
                    self.pos[1] = new_pos[1]
            else:
                self.pos[0] = new_pos[0]
                self.pos[1] = new_pos[1]
        else:
            pass



class Bullet:
    def __init__(self, pos, speed, angle):
        self.pos = list(pos)
        self.speed = speed
        self.angle = float(angle)
        self.radius = 10

        self.active = True
        self.createTime = pygame.time.get_ticks()

    def update(self):
        self.pos[0] += self.speed * math.cos(self.angle)
        self.pos[1] += self.speed * math.sin(self.angle)

    def draw(self, window, offset=(0,0)):
        pygame.draw.circle(window, (255,255,255), (int(self.pos[0] - offset[0]), int(self.pos[1] - offset[1])), self.radius)


class Triangle:
    def __init__(self, pos, speed, size):
        self.pos = list(pos)
        self.speed = speed
        self.size = size

        self.angle_accel = 0.2
        self.curr_angle = 0

        top = (self.pos[0] + self.size*2/3 * math.cos(self.curr_angle), self.pos[1] + self.size*2/3 * math.sin(self.curr_angle))
        b1 = (self.pos[0] + self.size*2/3 * math.cos(self.curr_angle + math.pi*2/3), self.pos[1] + self.size*2/3 * math.sin(self.curr_angle + math.pi*2/3))
        b2 = (self.pos[0] + self.size*2/3 * math.cos(self.curr_angle - math.pi*2/3), self.pos[1] + self.size*2/3 * math.sin(self.curr_angle - math.pi*2/3))

        self.points = [top, b1, b2]

        #force calculations to be added on top
        self.force_accel = 0.1
        self.force_deccel = 0.05
        self.curr_vel = [0,0]
        self.target_vel = [0,0]
        self.last_force_added = -1000
        self.force_duration = 50


    def update(self, players):

        if self.last_force_added + self.force_duration < pygame.time.get_ticks():
            self.target_vel = [0,0]

        top = (self.pos[0] + self.size*2/3 * math.cos(self.curr_angle), self.pos[1] + self.size*2/3 * math.sin(self.curr_angle))
        b1 = (self.pos[0] + self.size*2/3 * math.cos(self.curr_angle + math.pi*2/3), self.pos[1] + self.size*2/3 * math.sin(self.curr_angle + math.pi*2/3))
        b2 = (self.pos[0] + self.size*2/3 * math.cos(self.curr_angle - math.pi*2/3), self.pos[1] + self.size*2/3 * math.sin(self.curr_angle - math.pi*2/3))

        self.points = [top,b1,b2]

        closest = players[0]
        for i in range(1,len(players)):
            if dist(players[i].pos, self.pos) < dist(closest.pos, self.pos):
                closest = players[i]

        target_angle = math.atan2(closest.pos[1] - self.pos[1], closest.pos[0] - self.pos[0])

        #implement angle matching
        self.curr_angle = target_angle

        phys_helper(self.curr_vel, self.target_vel, self.force_accel, self.force_deccel)

        self.pos[0] += self.speed * math.cos(self.curr_angle) + self.curr_vel[0]
        self.pos[1] += self.speed * math.sin(self.curr_angle) + self.curr_vel[1]

    def add_force(self,vector):
        self.target_vel = list(vector)
        self.last_force_added = pygame.time.get_ticks()

    def draw(self, window, offset):
        drawpoints = [ [int(pair[0] - offset[0]), int(pair[1] - offset[1])] for pair in self.points]

        pygame.draw.polygon(window, (255,255,255), drawpoints)
        #pygame.draw.circle(window, (255,255,255), (int(self.pos[0] - offset[0]), int(self.pos[1] - offset[1])), self.size)


