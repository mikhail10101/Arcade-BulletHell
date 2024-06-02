import pygame
import math
import random
from physics import *

class Player(ForceObject):
    def __init__(self):
        super().__init__()
        #draw
        self.size = 20

        #movement
        self.pos = [1600,1600]
        self.speed = 6
        self.accel = 0.2
        self.deccel = 0.05
        self.curr_vel = [0,0]

        #angle to mouse
        self.mouse_angle = 0

        #shot in milliseconds
        self.last_shot = -1000
        self.shot_interval = 125

        self.hp = 100

        self.pointer_scale = 1.8

        #healing mechanics
        self.last_received_damage = 0
        self.last_moved = 0

        #scroll
        self.scroll = [0,0]
        self.alive = True


    def draw(self, window, val, new_offset=[0,0]):
        offset = self.scroll
        if not val:
            offset[0] = new_offset[0]
            offset[1] = new_offset[1]


        alias_factor = 4

        #pointer calculations
        scale = 1/4
        diff = (-math.cos(self.mouse_angle) * self.size*alias_factor * scale,-math.sin(self.mouse_angle) * self.size*alias_factor * scale)

        side_scale = 1.5
        side_angle = math.pi/20

        arrow_points = [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]
        arrow_points[0] = (self.size*8 + math.cos(self.mouse_angle) * self.size*alias_factor * self.pointer_scale, self.size*8 + math.sin(self.mouse_angle) * self.size*alias_factor * self.pointer_scale)
        arrow_points[1] = (self.size*8 + math.cos(self.mouse_angle + math.pi*side_angle) * self.size*alias_factor * side_scale, self.size*8 + math.sin(self.mouse_angle + math.pi*side_angle) * self.size*alias_factor * side_scale)
        arrow_points[5] = (self.size*8 + math.cos(self.mouse_angle - math.pi*side_angle) * self.size*alias_factor * side_scale, self.size*8 + math.sin(self.mouse_angle - math.pi*side_angle) * self.size*alias_factor * side_scale)
        arrow_points[2] = (arrow_points[1][0]+diff[0],arrow_points[1][1]+diff[1])
        arrow_points[3] = (arrow_points[0][0]+diff[0],arrow_points[0][1]+diff[1])
        arrow_points[4] = (arrow_points[5][0]+diff[0],arrow_points[5][1]+diff[1])

        #surface
        surf = pygame.Surface((self.size*16, self.size*16), pygame.SRCALPHA)
        pygame.draw.circle(surf, (255,255,255), (self.size*8, self.size*8), self.size*alias_factor, 32)
        pygame.draw.polygon(surf, (255,255,255), arrow_points)

        scaled_surf = pygame.transform.smoothscale_by(surf, 0.25)
        scaled_surf.set_colorkey((0,0,0))

        window.blit(scaled_surf, (int(self.pos[0] - offset[0] - self.size*8/4), int(self.pos[1] - offset[1] - self.size*8/4)), special_flags = pygame.BLEND_PREMULTIPLIED)

        #pygame.draw.circle(window, (255,255,255), (int(self.pos[0] - offset[0]), int(self.pos[1] - offset[1])), self.size, 10)

        

        # drawpoints = [ [int(pair[0] - offset[0]), int(pair[1] - offset[1])] for pair in arrow_points]
        # pygame.draw.polygon(window, (255,255,255), drawpoints)

        


    def update(self, inputs, bullets, map):
        super().update()
        current_time = pygame.time.get_ticks()

        #HEALTH
        if self.last_received_damage + 2000 < current_time:
            self.hp = min(self.hp + 0.1, 100)

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

        if self.curr_vel[0] != 0 or self.curr_vel[1] != 0:
            self.last_moved = current_time

        self.move([self.pos[0] + self.curr_vel[0] + self.fx, self.pos[1] + self.curr_vel[1] + self.fy], map)

        mx, my = inputs["click_pos"]
 
        mx += self.scroll[0]
        my += self.scroll[1]

        dx = mx - self.pos[0]
        dy = my - self.pos[1]

        self.mouse_angle = math.atan2(dy,dx)

        #SHOOT
        if inputs["click"]:
            if current_time > self.last_shot + self.shot_interval:
                bullets.append(Bullet(
                    (self.pos[0] + math.cos(self.mouse_angle) * self.pointer_scale * self.size, self.pos[1] + math.sin(self.mouse_angle) * self.pointer_scale * self.size), 
                    20, self.mouse_angle, True, 7
                ))
                self.last_shot = current_time

    def move(self, new_pos, map):
        i = int(self.pos[0] // map.tile_size)
        j = int(self.pos[1] // map.tile_size)
        newI = int(new_pos[0] // map.tile_size)
        newJ = int(new_pos[1] // map.tile_size)

        if 0 <= newI < len(map.map_values) and 0 <= newJ < len(map.map_values[0]):
            if (map.map_values[newI][newJ] == 1):
                if abs(i - newI) == 1 and abs(j - newJ) == 1:
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

    def polygon_collision(self, points):
        n = len(points)
        p1 = 0
        for i in range(1, n+1):
            p2 = i%n
            if intersect_circle(points[p1],points[p2],self.pos,self.size):
                return True
            p1 = p2
        return point_in_polygon(self.pos, points)



class Bullet:
    def __init__(self, pos, speed, angle, target_shapes, radius=10):
        self.pos = list(pos)
        self.speed = speed
        self.angle = float(angle)
        self.radius = radius

        self.active = True

        self.target_shapes = target_shapes
        
        self.active = True

    def update(self):
        self.pos[0] += self.speed * math.cos(self.angle)
        self.pos[1] += self.speed * math.sin(self.angle)

    def draw(self, window, offset=(0,0)):
        if self.active:
            if self.target_shapes:
                pygame.draw.circle(window, (255,255,255), (int(self.pos[0] - offset[0]), int(self.pos[1] - offset[1])), self.radius)
            else:
                pygame.draw.circle(window, (255,255,255), (int(self.pos[0] - offset[0]), int(self.pos[1] - offset[1])), self.radius, 3)

    #bullet collisions with an ordered set of points (any polygon)
    def polygon_collision(self, points):
        n = len(points)
        p1 = 0
        for i in range(1, n+1):
            p2 = i%n
            if intersect_circle(points[p1],points[p2],self.pos,self.radius):
                return True
            p1 = p2
        return point_in_polygon(self.pos, points)

    def collision(self, center, radius):
        return dist(self.pos, center) <= radius + self.radius


class Wave(Bullet):
    def __init__(self, pos, speed, angle, target_shapes, radius=10):
        super().__init__(pos, speed, angle, target_shapes, radius)
        self.points = [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]
    
    def update(self):
        super().update()

        scale = 1/10
        diff = (-math.cos(self.angle) * self.radius * scale,-math.sin(self.angle) * self.radius * scale)

        self.points[0] = (self.pos[0] + math.cos(self.angle) * self.radius, self.pos[1] + math.sin(self.angle) * self.radius)
        self.points[1] = (self.pos[0] + math.cos(self.angle + math.pi*2/7) * self.radius, self.pos[1] + math.sin(self.angle + math.pi*2/7) * self.radius)
        self.points[5] = (self.pos[0] + math.cos(self.angle - math.pi*2/7) * self.radius, self.pos[1] + math.sin(self.angle - math.pi*2/7) * self.radius)
        self.points[2] = (self.points[1][0]+diff[0],self.points[1][1]+diff[1])
        self.points[3] = (self.points[0][0]+diff[0],self.points[0][1]+diff[1])
        self.points[4] = (self.points[5][0]+diff[0],self.points[5][1]+diff[1])

    def draw(self, window, offset=(0,0)):
        if self.active:
            drawpoints = [ [int(pair[0] - offset[0]), int(pair[1] - offset[1])] for pair in self.points]
            pygame.draw.polygon(window, (255,255,255), drawpoints,3)

    #collision with any circle
    def collision(self, center, radius):
        n = 6
        p1 = 0
        for i in range(1, n+1):
            p2 = i%n
            if intersect_circle(self.points[p1],self.points[p2],center,radius):
                return True
            p1 = p2
        return point_in_polygon(center, self.points)




class Triangle(Shape):
    def __init__(self, pos, speed, size, id, health=1):
        super().__init__(id)

        self.pos = list(pos)
        self.speed = speed
        self.size = size

        self.health = health

        self.angle_pos = 0
        self.angle_vel = 0.08

        self.points = [(0,0),(0,0),(0,0)]

        self.active = True
        self.disp = [0,0]

        self.last_hit = -1000
        self.monocolor = 200

    def update(self, players):
        super().update()

        closest = players[0]
        for i in range(1,len(players)):
            if dist(players[i].pos, self.pos) < dist(closest.pos, self.pos):
                closest = players[i]

        target_angle = math.atan2(closest.pos[1] - self.pos[1], closest.pos[0] - self.pos[0])
        self.angle_pos = move_angle(self.angle_pos, target_angle, self.angle_vel)

        points_modifier(self.points, self.pos, 3, self.size, self.angle_pos)

        if pygame.time.get_ticks()//1000 % 1 == 0:
            rand_scale = self.size/50
            a = random.random() * 2 - 1
            b = random.random() * 2 - 1
            self.add_force((rand_scale*a, rand_scale*b),250,500,250)

        self.disp[0] = self.speed * math.cos(self.angle_pos) + self.fx
        self.disp[1] = self.speed * math.sin(self.angle_pos) + self.fy

        self.pos[0] += self.disp[0]
        self.pos[1] += self.disp[1]




class Square(Shape):
    def __init__(self, pos, speed, size, id, health=4):
        super().__init__(id)
        self.pos = list(pos)
        self.speed = speed
        self.size = size

        self.health = health

        self.angle_pos = 0
        self.angle_vel = 0.08

        self.points = [(0,0),(0,0),(0,0),(0,0)]

        self.active = True
        self.disp = [0,0]

        #charge details
        self.charge_interval = 3000
        self.last_charge = 0
        self.pause_duration = 1000
        self.charge_duration = 2000
        self.charge_strength = 10

        self.mode = 0

        #Shape class
        self.last_hit = -1000

    def update(self, players):
        super().update()
        current_time = pygame.time.get_ticks()

        if self.mode == 0:
            closest = players[0]
            for i in range(1,len(players)):
                if dist(players[i].pos, self.pos) < dist(closest.pos, self.pos):
                    closest = players[i]

            target_angle = math.atan2(closest.pos[1] - self.pos[1], closest.pos[0] - self.pos[0])
            self.angle_pos = move_angle(self.angle_pos, target_angle, self.angle_vel)

            self.disp[0] = self.speed * math.cos(self.angle_pos) + self.fx
            self.disp[1] = self.speed * math.sin(self.angle_pos) + self.fy

            if current_time > self.charge_interval + self.last_charge:
                self.mode = 1
                self.last_charge = current_time
        
        elif self.mode == 1:
            closest = players[0]
            for i in range(1,len(players)):
                if dist(players[i].pos, self.pos) < dist(closest.pos, self.pos):
                    closest = players[i]

            target_angle = math.atan2(closest.pos[1] - self.pos[1], closest.pos[0] - self.pos[0])
            self.angle_pos = move_angle(self.angle_pos, target_angle, self.angle_vel)

            if current_time > + self.pause_duration + self.last_charge:
                self.mode = 2
                self.add_force(( self.charge_strength* math.cos(self.angle_pos), self.charge_strength* math.sin(self.angle_pos) ),
                    100,
                    1500,
                    500
                )

        else:
            self.disp[0] = self.fx
            self.disp[1] = self.fy

            if current_time > self.charge_duration + self.pause_duration + self.last_charge:
                self.mode = 0


        points_modifier(self.points, self.pos, 4, self.size, self.angle_pos)

        self.pos[0] += self.disp[0]
        self.pos[1] += self.disp[1]


class Squarelet(Shape):
    def __init__(self, pos, speed, size, id, health=1):
        super().__init__(id)

        self.pos = list(pos)
        self.speed = speed
        self.size = size

        self.health = 1

        self.angle_pos = 0
        self.angle_vel = 0.08

        self.active = True
        self.disp = [0,0]

        self.points = [(0,0),(0,0),(0,0),(0,0)]

        #shot in milliseconds
        self.last_shot = -1000
        self.shot_interval = 333

        #vel
        self.curr_speed = 0
        self.accel = 0.1
        self.deccel = 0.05

        #Shape class
        self.last_hit = -1000


    def update(self, players, bullets):
        super().update()

        current_time = pygame.time.get_ticks()

        closest = players[0]
        for i in range(1,len(players)):
            if dist(players[i].pos, self.pos) < dist(closest.pos, self.pos):
                closest = players[i]

        target_angle = math.atan2(closest.pos[1] - self.pos[1], closest.pos[0] - self.pos[0])
        self.angle_pos = move_angle(self.angle_pos, target_angle, self.angle_vel)

        points_modifier(self.points, self.pos, 4, self.size, self.angle_pos)

        #control distance
        d = dist(closest.pos, self.pos)
        target_speed = 0
        if d > 250:
            target_speed = self.speed
        else:
            target_speed = -self.speed

        if pygame.time.get_ticks()//1000 % 1 == 0:
            rand_scale = self.size/40
            a = random.random() * 2 - 1
            b = random.random() * 2 - 1
            self.add_force((rand_scale*a, rand_scale*b),250,1250,500)

        self.curr_speed = phys_single_helper(self.curr_speed, target_speed, self.accel, self.deccel)
        self.disp[0] = self.curr_speed * math.cos(self.angle_pos) + self.fx 
        self.disp[1] = self.curr_speed * math.sin(self.angle_pos) + self.fy

        self.pos[0] += self.disp[0]
        self.pos[1] += self.disp[1]

        if current_time > self.last_shot + self.shot_interval:
            dx = closest.pos[0] - self.pos[0]
            dy = closest.pos[1] - self.pos[1]
            rads = math.atan2(dy,dx)
            bullets.append(Bullet(self.pos, 13, rads, False, 5))
            self.last_shot = current_time




class Pentagon(Shape):
    def __init__(self, pos, size, angle, id, health=5):
        super().__init__(id)

        self.pos = list(pos)
        self.size = size

        self.health = health

        self.angle_pos = angle
        self.angle_vel = 0.03

        self.points = [(0,0),(0,0),(0,0),(0,0),(0,0)]

        self.active = True
        self.disp = [0,0]

        self.mode = 0

        #laser details
        self.pause_duration = 1000
        self.laser_interval = 6000
        self.last_laser = pygame.time.get_ticks() - 5500
        self.laser_duration = 2000
        self.lasers = []
        self.bounds = [0,0]

        self.laser_warning = []

        #Shape class
        self.last_hit = -1000
    
    def update(self,players,map):
        super().update()
        current_time = pygame.time.get_ticks()

        if self.mode == 0:
            if len(self.lasers) > 0:
                self.bounds[0] = 0
                self.bounds[1] = 0

            closest = players[0]
            for i in range(1,len(players)):
                if dist(players[i].pos, self.pos) < dist(closest.pos, self.pos):
                    closest = players[i]

            target_angle = math.atan2(closest.pos[1] - self.pos[1], closest.pos[0] - self.pos[0]) 
            self.angle_pos = move_angle(self.angle_pos, target_angle, self.angle_vel)

            if current_time > self.laser_interval + self.last_laser:
                self.mode = 1
                self.last_laser = current_time
        
        if self.mode == 1:
            if len(self.laser_warning) == 0:
                self.laser_warning.append((self.points[0],map.raycast(self.pos,self.angle_pos,10000)))
        
            if current_time > self.pause_duration + self.last_laser:
                self.mode = 2
                self.shoot_laser(map)
                
        if self.mode == 2:
            if len(self.laser_warning) > 0:
                self.laser_warning = []

            #shooting laser mode
            laser_time = self.laser_duration + current_time - (self.laser_duration + self.pause_duration + self.last_laser)
            
            #ratio goes from 0 to 1
            time_ratio = min(laser_time/self.laser_duration,1)
            w_ratio = 0
            if time_ratio < 0.1:
                w_ratio = time_ratio**2 * 10**2
            elif time_ratio >= 0.9:
                time_ratio -= 0.9
                w_ratio = (0.1 - time_ratio)/0.1
            else:
                if current_time%7 == 0:
                    w_ratio = 1
                else:
                    w_ratio = 0.9

            self.bounds[0], self.bounds[1] = middle_bounds(len(self.lasers), w_ratio)

            #player gets hit from laser
            for i in range(self.bounds[0], self.bounds[1]):
                for p in players:
                    if intersect_circle(self.lasers[i][0], self.lasers[i][1], p.pos, p.size):
                        p.hp -= 0.1

            if current_time > self.laser_duration + self.pause_duration + self.last_laser:
                self.mode = 0

        points_modifier(self.points, self.pos, 5, self.size, self.angle_pos)



    def draw(self, window, offset, time):
        super().draw(window, offset, time)

        for i in range(self.bounds[0],self.bounds[1]):
            laser = self.lasers[i]
            pygame.draw.line(window, (255,255,255), 
                (laser[0][0] - offset[0], laser[0][1] - offset[1]), 
                (laser[1][0] - offset[0], laser[1][1] - offset[1]), 
            2)

        for warn in self.laser_warning:
            pygame.draw.line(window, (255,0,0), 
                (warn[0][0] - offset[0], warn[0][1] - offset[1]), 
                (warn[1][0] - offset[0], warn[1][1] - offset[1]), 
            2)

    
    def shoot_laser(self, map):
        self.lasers = []
        s = int(self.size//2)
        for i in range(-s,s+1,1):
            p1 = (
                self.pos[0] - i * math.cos(self.angle_pos + math.pi/2),
                self.pos[1] - i * math.sin(self.angle_pos + math.pi/2)
            )
            p2 = map.raycast(p1, self.angle_pos, 10000)
            self.lasers.append((p1,p2))

        
class Hexagon(Shape):
    def __init__(self, pos, speed, size, follow, id, health=3):
        super().__init__(id)

        self.pos = list(pos)
        self.speed = speed
        self.size = size

        self.health = health

        self.angle_pos = 0
        self.angle_vel = 0.02

        self.points = [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]

        self.active = True
        self.disp = [0,0]

        self.follow = follow

        #Shape class
        self.last_hit = -1000

    def update(self, players):
        super().update()

        points_modifier(self.points, self.pos, 6, self.size, self.angle_pos)

        reach = [0,0]
        if self.follow == None or not self.follow.active:
            reach = players[0].pos
            for i in range(1,len(players)):
                if dist(players[i].pos, self.pos) < dist(reach, self.pos):
                    reach = players[i].pos
        else:
            reach = self.follow.pos

        target_angle = math.atan2(reach[1] - self.pos[1], reach[0] - self.pos[0])
        self.angle_pos = move_angle(self.angle_pos, target_angle, self.angle_vel)

        self.disp[0] = self.speed * math.cos(self.angle_pos) + self.fx
        self.disp[1] = self.speed * math.sin(self.angle_pos) + self.fy

        self.pos[0] += self.disp[0]
        self.pos[1] += self.disp[1]





class Heptagon(Shape):
    def __init__(self, pos, speed, size, id, health=7):
        super().__init__(id)

        self.pos = list(pos)
        self.speed = speed
        self.size = size

        self.health = health

        self.angle_pos = 0
        self.angle_vel = 0.08

        self.active = True
        self.disp = [0,0]

        self.points = [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]

        #shot in milliseconds
        self.extra = random.random() * 1000

        self.last_shot = self.extra
        self.shot_interval = 2000

        #vel
        self.curr_speed = 0
        self.accel = 0.3
        self.deccel = 0.3

        #Shape class
        self.last_hit = -1000


    def update(self, players, bullets):
        super().update()

        current_time = pygame.time.get_ticks()

        closest = players[0]
        for i in range(1,len(players)):
            if dist(players[i].pos, self.pos) < dist(closest.pos, self.pos):
                closest = players[i]

        target_angle = math.atan2(closest.pos[1] - self.pos[1], closest.pos[0] - self.pos[0])
        self.angle_pos = move_angle(self.angle_pos, target_angle, self.angle_vel)

        points_modifier(self.points, self.pos, 7, self.size, self.angle_pos)


        #control distance
        d = dist(closest.pos, self.pos)
        target_speed = 0
        if d > 500:
            target_speed = self.speed
        else:
            target_speed = -self.speed

        if pygame.time.get_ticks()//1000 % 2 == self.extra:
            rand_scale = self.size
            a = random.random() * 2 - 1
            b = random.random() * 2 - 1
            self.add_force((rand_scale*a, rand_scale*b),250,1250,500)

        self.curr_speed = phys_single_helper(self.curr_speed, target_speed, self.accel, self.deccel)
        self.disp[0] = self.curr_speed * math.cos(self.angle_pos) + self.fx 
        self.disp[1] = self.curr_speed * math.sin(self.angle_pos) + self.fy

        self.pos[0] += self.disp[0]
        self.pos[1] += self.disp[1]

        if current_time > self.last_shot + self.shot_interval:
            dx = closest.pos[0] - self.pos[0]
            dy = closest.pos[1] - self.pos[1]
            rads = math.atan2(dy,dx)
            bullets.append(Wave((self.pos[0] - math.cos(self.angle_pos)*self.size,self.pos[1] - math.sin(self.angle_pos)*self.size), self.speed*2, rads, False, self.size*2.5))
            self.forces = []
            self.add_force((-math.cos(rads) * self.size/30, -math.sin(rads) * self.size/30), 250, 750, 1000)
            
            self.last_shot = current_time






class Nonagon(Shape):
    def __init__(self, pos, speed, size, angle, id, health=2):
        super().__init__(id)

        self.pos = list(pos)
        self.size = size

        self.health = health

        self.speed = speed
        self.movement_angle = angle

        self.angle_pos = 0
        self.angle_vel = 0.03

        #shot in milliseconds
        self.last_shot = -1000
        self.shot_interval = 1000

        self.points = [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]

        self.active = True
        self.disp = [0,0]

        #Shape class
        self.last_hit = -1000

    def update(self, bullets, map):
        super().update()
        current_time = pygame.time.get_ticks()

        self.angle_pos += self.angle_vel

        if current_time > self.last_shot + self.shot_interval:
            self.nonagon_shoot(bullets)
            self.last_shot = current_time

        points_modifier(self.points,self.pos,9,self.size,self.angle_pos)

        self.disp[0] = self.fx + self.speed*math.cos(self.movement_angle)
        self.disp[1] = self.fy + self.speed*math.sin(self.movement_angle)
        

        self.bounce((self.pos[0]+self.disp[0], self.pos[1]+self.disp[1]), map)

    def nonagon_shoot(self, bullets):
        for i in range(9):
            bullets.append(Bullet(self.pos, 13, self.angle_pos + 2*i*math.pi/9, False, self.size/3))

    def bounce(self, new_pos, map):
        i = int(self.pos[0] // map.tile_size)
        j = int(self.pos[1] // map.tile_size)
        newI = int(new_pos[0] // map.tile_size)
        newJ = int(new_pos[1] // map.tile_size)

        if 0 <= newI < len(map.map_values) and 0 <= newJ < len(map.map_values[0]):
            if (map.map_values[i][j] == 0 and map.map_values[newI][newJ] == 1):
                    if i-newI == -1:
                        self.movement_angle = math.pi - self.movement_angle
                    elif i-newI == 1:
                        self.movement_angle = math.pi - self.movement_angle
                    elif j-newJ == -1:
                        self.movement_angle = 2*math.pi - self.movement_angle
                    elif j-newJ == 1:
                        self.movement_angle = 2*math.pi - self.movement_angle
            else:
                self.pos[0] += self.fx + self.speed*math.cos(self.movement_angle)
                self.pos[1] += self.fy + self.speed*math.sin(self.movement_angle)
        else:
            self.movement_angle = math.atan2(self.disp[1], self.disp[0])