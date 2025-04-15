from robot_systems.robot import HamBot
from robot_systems.camera import Camera

import math
import time
base_speed = 30
target = 250

kp = 0.05
ki = 0
kd = 0.001
Chris_R = HamBot()
time.sleep(1)

def PID(target, current,prev_error,integral,dt):
    err = target - current
    if abs(err) > 5:
        #Proportional
        p_term = kp * err
        
        #integral
        integral += err * dt
        i_term = ki * integral
        #derivative
        derivative = (err -prev_error)/dt
        d_term = kd * derivative
        
        adj = p_term + i_term + d_term
    else:
        adj = 0
    
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
        return -1

def WallFollow(target):
    adj = 0
    perror = 0.0
    integral = 0
    ptime = time.time()
    
    while True:
        ctime = time.time()
        Chris_R.set_left_motor_speed(max(-50,min(50,base_speed + adj)))
        Chris_R.set_right_motor_speed(max(-50,min(50,base_speed - adj)))
        
        left_s = get_lidar("left")
        dt = ctime - ptime
        ptime = ctime
        adj,perror,integral = PID(target,left_s,perror,integral,dt)
        print(adj)
        time.sleep(0.1)
try:
    WallFollow(target)
except (KeyboardInterrupt):
    Chris_R.disconnect_robot()
