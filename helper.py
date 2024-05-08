import math
import pygame

def phys_helper(curr_vel, target_vel, accel, deccel):
    if (target_vel[0] != 0):
        if (abs(curr_vel[0] - target_vel[0]) < accel):
            curr_vel[0] = target_vel[0]
        elif (curr_vel[0] < target_vel[0]):
            curr_vel[0] += accel
        else:
            curr_vel[0] -= accel
    else:
        if (abs(curr_vel[0] - target_vel[0]) < deccel):
            curr_vel[0] = target_vel[0]
        elif (curr_vel[0] < target_vel[0]):
            curr_vel[0] += deccel
        else:
            curr_vel[0] -= deccel

    if (target_vel[1] != 0):
        if (abs(curr_vel[1] - target_vel[1]) < accel):
            curr_vel[1] = target_vel[1]
        elif (curr_vel[1] < target_vel[1]):
            curr_vel[1] += accel
        else:
            curr_vel[1] -= accel
    else:
        if (abs(curr_vel[1] - target_vel[1]) < deccel):
            curr_vel[1] = target_vel[1]
        elif (curr_vel[1] < target_vel[1]):
            curr_vel[1] += deccel
        else:
            curr_vel[1] -= deccel

def phys_single_helper(curr_vel, target_vel, accel, deccel):
    if (target_vel != 0):
        if (abs(curr_vel - target_vel) < accel):
            curr_vel = target_vel
        elif (curr_vel < target_vel):
            curr_vel += accel
        else:
            curr_vel -= accel
    else:
        if (abs(curr_vel - target_vel) < deccel):
            curr_vel = target_vel
        elif (curr_vel < target_vel):
            curr_vel += deccel
        else:
            curr_vel -= deccel
    return curr_vel


def dist(pos, pos2):
    return math.sqrt((pos[0] - pos2[0])**2 + (pos[1] - pos2[1])**2) 

def point_in_polygon(point, polygon):
    num_vertices = len(polygon)
    x, y = point[0], point[1]
    inside = False
 
    p1 = polygon[0]
 
    for i in range(1, num_vertices + 1):
        p2 = polygon[i % num_vertices]
 
        if y > min(p1[1], p2[1]):
            if y <= max(p1[1], p2[1]):
                if x <= max(p1[0], p2[0]):
                    x_intersection = (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1]) + p1[0]
                    if p1[0] == p2[0] or x <= x_intersection:
                        inside = not inside
        p1 = p2
    return inside

def intersect_circle(pointA, pointB , center, radius):
    d = pygame.math.Vector2(pointB[0]-pointA[0], pointB[1]-pointA[1])
    f = pygame.math.Vector2(pointA[0]-center[0], pointA[1]-center[1])

    a = d.dot(d)
    b = 2*f.dot(d)
    c = f.dot(f) - radius*radius

    discriminant = b*b - 4*a*c

    if discriminant < 0:
        return False
    
    discriminant = math.sqrt(discriminant)

    t1 = (-b - discriminant)/(2*a)
    t2 = (-b + discriminant)/(2*a)

    if t1 >= 0 and t1 <= 1:
        return True
    if t2 >= 0 and t2 <= 1:
        return True
    return False

