from robot_systems.robot import HamBot
from robot_systems.camera import Camera
import math
import time
range = 500


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

base_speed = 25
target = 320

kp = 0.005
ki = 0.001
kd = 0.02
dt = 0
integral = 0
previousError = 0.0
previousTime = time.perf_counter()
adj = 0

while(True):
    camera.set_landmark_colors(color,0.1)
    landmarks = camera.find_landmarks()
    
    if landmarks:
        print(landmarks[0].x)
        if landmarks[0].x > 250:
            break
        # Chris_R.set_left_motor_speed(max(-75,min(75,base_speed + adj)))
        # Chris_R.set_right_motor_speed(base_speed)
        
    else:
        Chris_R.set_left_motor_speed(10)
        Chris_R.set_right_motor_speed(-10)
    time.sleep(0.3)
Chris_R.stop_motors()

time.sleep(0.5)


front_dist_curr = 900
while(True):
    camera.set_landmark_colors(color,0.1)
    landmarks = camera.find_landmarks()
    
    currentTime = time.perf_counter()
    Lidar_f = [179,180,181]
    temp_array = Chris_R.get_range_image()
    front_dist_curr = min(temp_array[Lidar_f[0]], temp_array[Lidar_f[1]], temp_array[Lidar_f[2]])

    Chris_R.set_left_motor_speed(max(-75,min(75,base_speed + adj)))
    Chris_R.set_right_motor_speed(base_speed)
    
    dt = currentTime - previousTime
    if landmarks:
        adj, previousError, integral = PID(320, landmarks[0].x, previousError, integral, dt)
    else:
        print("ello")
    previousTime = currentTime
    
    if front_dist_curr < 600:
        break
    time.sleep(0.7)
    
Chris_R.stop_motors()
print("Robot Stopped!")
