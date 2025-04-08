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

#Find the starting direction the robot is looking in
currentDirection = Chris_R.get_heading()
print(currentDirection)

#Loop to return current landmark value
while(True):
    camera.set_landmark_colors(color,0.1)
    landmarks = camera.find_landmarks()

    #Actions to take to find target:
    #If target is not visible, rotate 360 degrees until it is detected
    if not landmarks:
        Chris_R.set_left_motor_speed(50)
        Chris_R.set_right_motor_speed(-50)
    if landmarks:
        print("Success")
#We have the robots current direction
#We have the final landmarks position
#If the robot changes angle, it must calculate how to get back
#Have encoders return position!!!!!
#With encoders position and the new angle, we can calculate the distance