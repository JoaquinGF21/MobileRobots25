from robot_systems.robot import HamBot
from robot_systems.camera import Camera

import math
import time

Chris_R = HamBot()
time.sleep(22)

while True:
    test = Chris_R.get_range_image()
    for i in test:
        if i < 300:
            print(i)
    time.sleep(1)