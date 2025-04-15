from robot_systems.robot import HamBot
from robot_systems.camera import Camera

import math
import time

Chris_R = HamBot()
time.sleep(22)
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
        if sight[idx] != -1:
            temp.append(sight[idx])
        
    prev = sight.copy()
    if temp:
        return min(temp), prev
    else:
        return None, prev
    
while True:
    prev = None
    temp, prev = get_lidar("left",prev)
    time.sleep(0.1)