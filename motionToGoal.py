from robot_systems.robot import HamBot
from robot_systems.camera import Camera
import math
import time

targetDistanceFromGoal = 500  # mm
Lidar_f = [179, 180, 181]

#Initialize robot
Chris_R = HamBot()
camera = Chris_R.camera

#Set goal color & landmark
color = (158,0,255)
camera.set_landmark_colors(color,0.1)

#Find the starting direction the robot is looking in

currentDirection = Chris_R.get_heading()
print(currentDirection)

def getLidarImage(lidar_angles):
    temp_array = Chris_R.get_range_image()
    front_dist_curr = min(temp_array[lidar_angles[0]], temp_array[lidar_angles[1]], temp_array[lidar_angles[2]])
    return front_dist_curr

        
#We have the robots current direction
#We have the final landmarks position
#If the robot changes angle, it must calculate how to get back
#Have encoders return position!!!!!
#With encoders position and the new angle, we can calculate the distance

#Within the loop
#The robot checks for landmark
#If it sees it, go to Continue
#If it does not see it, then rotate around, until it sees it

#Continue: 
#Check the lidar_f for distance to target
#Begin going in a straight line towards target

#while should actually be until robot reaches target distance from objective

while(True):
    #sets base landmark found state
    landmark_found = False
    
    #gets images
    image = Chris_R.camera.get_image()
    landmarks = camera.find_landmarks()
    currentDistance = getLidarImage(Lidar_f)
    time.sleep(.5)
    
    #while it has not found the landmark
    while(landmark_found == False):
        
        if  landmarks:
            landmark_found = True
            Chris_R.stop_motors()
            break
        else:
            #robot rotates to find the landmark
            Chris_R.set_left_motor_speed(10)
            Chris_R.set_right_motor_speed(-10) 
        
    Chris_R.set_left_motor_speed(25)
    Chris_R.set_right_motor_speed(25)