from robot_systems.robot import HamBot
from robot_systems.camera import Camera
import math
import time
range = 500
#s
Chris_R = HamBot()
camera = Chris_R.camera
color = (158,0,255)
camera.set_landmark_colors(color,0.1)
while(True):
    camera.set_landmark_colors(color,0.1)
    landmarks = camera.find_landmarks()
    
    if landmarks:
        x_value = landmarks[0].x
        print(x_value)



