from robot_systems.robot import HamBot
from robot_systems.camera import Camera
import math
import time

#Initialize robot
Chris_R = HamBot()
camera = Chris_R.camera

#Set goal color & landmark
color = (158,0,255)
camera.set_landmark_colors(color,0.1)

currentLocation = Chris_R.get_heading
print(currentLocation)
#Loop to return current landmark value
"""while(True):
    camera.set_landmark_colors(color,0.1)
    landmarks = camera.find_landmarks()
    print(landmarks)
"""
