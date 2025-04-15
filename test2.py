from robot_systems.robot import HamBot
from robot_systems.camera import Camera

import math
import time
base_speed = 30
target = 200

kp = 0.001
ki = 0.002
kd = 0.005
Chris_R = HamBot()
time.sleep(1)

def PID(target, current,prev_error,integral,dt):
    err = target - current
    
    #Proportional
    p_term = kp * err
    
    #integral
    integral += err * dt
    i_term = ki * integral
    #derivative
    derivative = (err -prev_error)/dt
    d_term = kd * derivative
    
    adj = p_term + i_term + d_term
    
    return adj, err, integral
def get_lidar(dir):
    directions= {
        "left" : 90,
        "right": 270,
        "forw" : 180,
        "back" : 0
    }
    center = directions.get(dir)
    temp = []
    sight = Chris_R.get_range_image()
    #sets initial prev to be an array
    for i in range(-10,11):
        idx = center + i
        if sight[idx] != -1:
            temp.append(sight[idx])
        
    if temp:
        return min(temp)
    else:
        return [-1]

def WallFollow(target):
    adj = 0
    while True:
        Chris_R.set_left_motor_speed(max(-50,min(50,base_speed + adj)))
        Chris_R.set_right_motor_speed(base_speed)
        
        left_s = get_lidar("left")
        err = target - left_s
        pterm = kp * err
        adj += err
        time.sleep(0.1)
try:
    WallFollow(target)
except (KeyboardInterrupt):
    Chris_R.disconnect_robot()
