from robot_systems.robot import HamBot
from robot_systems.camera import Camera

import math
import time

Chris_R = HamBot()
time.sleep(5)
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
    
while True:
    temp = get_lidar("left")
    print(temp)
    time.sleep(0.1)