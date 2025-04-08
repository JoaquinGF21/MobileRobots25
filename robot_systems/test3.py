from robot_systems.robot import HamBot
from robot_systems.camera import Camera
import math
import time


Chris_R = HamBot()
camera = Chris_R.camera
color = (158,0,255)
while(True):
    camera.set_landmark_colors(color,0.1)
    landmarks = camera.find_landmarks()
    print(landmarks)

