from robot_systems.robot import HamBot
from robot_systems.camera import Camera
import math
import time
range = 500

base_speed = 25
target = 320

kp = 0.05
ki = 0.001
kd = 0.2

#Rotate to find

def PID(target, current,prev_error,integral,dt):
    err = target - current
    
    #Proportional
    p_term = kp * err
    
    #integral
    integral += err * dt
    i_term = ki * integral
    #derivative
    derivative = (err -prev_error)/dt
    d_term = kd * derivative
    
    adj = p_term + i_term + d_term
    
    return adj, err, integral

Chris_R = HamBot()
camera = Chris_R.camera
color = (158,0,255)
camera.set_landmark_colors(color,0.1)

while(True):
    camera.set_landmark_colors(color,0.1)
    landmarks = camera.find_landmarks()
    
    if landmarks:
        print(landmarks[0].x)
        Chris_R.stop_motors
        # Chris_R.set_left_motor_speed(max(-75,min(75,base_speed + adj)))
        # Chris_R.set_right_motor_speed(base_speed)
        
    else:
        Chris_R.set_left_motor_speed(15)
        Chris_R.set_right_motor_speed(-15)




