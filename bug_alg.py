from robot_systems.robot import HamBot
import math
import time

Lidar_l = [89,90,91]
Lidar_r = [269,270,271]
Lidar_f = [179,180,181]
Lidar_b = [359,0,1]
base_speed = 50
target = 500

kp = 0.05
ki = 0.001
kd = 0.2

Chris_R = HamBot()
time.sleep(22)



"space to implement line thing"
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
def objectDetection():
    range = target
    objects = []
    sight = Chris_R.get_range_image()
    
    idx = 0
    i = 0
    while( i <= len(sight)):
        if sight[i] < range:
            objects.append((i,sight[i]))
        i+=1
    print(objects)
    
        

def WallFollow(dist_from_line):
    print()
i = 1
while True:
    print(f"interation {i}")
    objectDetection()
    time.sleep(1)
    i = i+1
    