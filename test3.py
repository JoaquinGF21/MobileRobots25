from robot_systems.robot import HamBot
from robot_systems.camera import Camera
import math
import time
range = 500

Chris_R = HamBot()
camera = Chris_R.camera
# color = (158,0,255)
# camera.set_landmark_colors(color,0.1)
# while(True):
#     camera.set_landmark_colors(color,0.1)
#     landmarks = camera.find_landmarks()
    
#     print(landmarks)
#     print(landmarks[0])
while True:
    lidar = Chris_R.get_range_image()
    for n in lidar:
        if n < range and n >= 0:
            print(n)
    time.sleep(2)


