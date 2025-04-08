from robot_systems.robot import HamBot
from robot_systems.camera import Camera
from robot_systems.lidar import Lidar
import math
import time

targetDistanceFromWall = 300  # mm
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

#Loop to return current landmark value
while(True):
    image = Chris_R.camera.get_image()
    landmarks = camera.find_landmarks()

    #Actions to take to find target:
    #If target is not visible, rotate 360 degrees until it is detected
    if not landmarks:
        Chris_R.set_left_motor_speed(15)
        Chris_R.set_right_motor_speed(-15)
        
    else:
        print("Success!")
        break
Chris_R.stop_motors()    


while(True):
    currentDistance = getLidarImage(Lidar_f)
    if (targetDistanceFromWall - currentDistance < 5) and (498 <= currentDistance <=502):# If velocity is very small, stop the robot
                print("Hurray!!!") 
                robotStop()
                temp_array = Chris_R.get_range_image()
                front_dist_curr = min(temp_array[Lidar_f[0]], temp_array[Lidar_f[1]], temp_array[Lidar_f[2]])
                print(front_dist_curr)
                break
    else:
                # Convert normalized velocity (-1 to 1) to robot speed commands
                # You might need to adjust this based on your robot's API
                Chris_R.set_left_motor_speed(velocity)
                Chris_R.set_right_motor_speed(velocity)
                # velocity, angular_velocity
            
            # Small delay to prevent CPU overuse
    time.sleep(0.05)
    
        
#We have the robots current direction
#We have the final landmarks position
#If the robot changes angle, it must calculate how to get back
#Have encoders return position!!!!!
#With encoders position and the new angle, we can calculate the distance