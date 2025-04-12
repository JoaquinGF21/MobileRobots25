from robot_systems.robot import HamBot
from robot_systems.camera import Camera

import math
import time
base_speed = 30
target = 500

kp = 0.05
ki = 0.001
kd = 0.2
target = 500
Chris_R = HamBot()
time.sleep(22)

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
def get_lidar(dir,prev):
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
    if prev == None:
        prev = [0] * len(sight)
    for i in range(-10,11):
        idx = center + i
        if prev[idx] != sight[idx] and sight[idx] != -1:
            temp.append(sight[idx])
        
    prev = sight.copy()
    return min(temp),prev
    

def WallFollow(target):
    tprev = time.perf_counter()
    prev = None
    left_s, prev = get_lidar("left",prev)
    adj = 0
    dt = 0
    integral = 0
    p_error = 0.0
    while True:
        Chris_R.set_left_motor_speed(max(-75,min(75,base_speed + adj)))
        Chris_R.set_right_motor_speed(base_speed)
        
        left_s, prev = get_lidar("left",prev)
        tcurrent = time.perf_counter()
        dt = tcurrent - tprev
        adj, p_error, integral  = PID(target,left_s,p_error,integral,dt)
        tprev = tcurrent
        time.sleep(0.7)

WallFollow(target)
