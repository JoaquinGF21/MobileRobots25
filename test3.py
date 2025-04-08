from robot_systems.robot import HamBot
from robot_systems.camera import Camera
import math
import time


Chris_R = HamBot()
camera = Chris_R.camera
color = (158,0,255)
camera.set_landmark_colors(color,0.1)
while(True):
<<<<<<< HEAD:robot_systems/test3.py
    camera.set_landmark_colors(color,0.1)
=======
    image = camera.get_image()
    
>>>>>>> 37030f03f96983dfd4ef677f5da8eab1c2850963:test3.py
    landmarks = camera.find_landmarks()
    print(landmarks)

