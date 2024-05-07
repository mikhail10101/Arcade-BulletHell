import math

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

def dist(pos, pos2):
    return math.sqrt((pos[0] - pos2[0])**2 + (pos[1] - pos2[1])**2) 
