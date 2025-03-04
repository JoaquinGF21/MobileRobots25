from robot_systems.robot import HamBot
import math
import time


Chris_R = HamBot()
time.sleep(22)
 #balls
#initialize directions and base speed
Lidar_l = [89,90,91]
Lidar_r = [269,270,271]
Lidar_f = [179,180,181]
Lidar_b = [359,0,1]
base_speed = 50
target = 300

kp = 0.1
ki = 0.005
kd = 0.1


set_dist = 300

def corner(dir):
    temp_array = Chris_R.get_range_image()
    front_dist_curr = min(temp_array[Lidar_f[0]],temp_array[Lidar_f[1]],temp_array[Lidar_f[2]])
    print(dir)
    if (dir == 'left'):
        while (True):
            temp_array = Chris_R.get_range_image()
            front_dist_curr = min(temp_array[Lidar_f[0]],temp_array[Lidar_f[1]],temp_array[Lidar_f[2]])
            Chris_R.set_left_motor_speed(30)
            Chris_R.set_right_motor_speed(-30)
            if (front_dist_curr > 1000):
                break
    if (dir == 'right'):
        while ((temp_array[295]-5 <= temp_array[255] <= temp_array[295]+5) and (front_dist_curr < 350)):
            temp_array = Chris_R.get_range_image()
            front_dist_curr = min(temp_array[Lidar_f[0]],temp_array[Lidar_f[1]],temp_array[Lidar_f[2]])
            Chris_R.set_left_motor_speed(-30)
            Chris_R.set_right_motor_speed(30)
    
    Chris_R.stop_motors()

        

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
    
    
    

def wall_follow(dir):
    #initialize current and prev distances along with a temp array to hold the lidar readings
    front_dist_curr = 0
    side_dist_curr = 0
    front_dist_prev = 0
    side_dist_prev = 0
    adj = 0
    temp_array = []
    prevTime = time.perf_counter()
    integral = 0
    prev_error = 0.0
    while(True):
        currentTime = time.perf_counter()
        
        Chris_R.set_left_motor_speed(max(-75,min(75,base_speed + adj)))
        Chris_R.set_right_motor_speed(base_speed)
        
        temp_array = Chris_R.get_range_image()
        front_dist_curr = min(temp_array[Lidar_f[0]],temp_array[Lidar_f[1]],temp_array[Lidar_f[2]])
        
        
        if (dir == 'left'):
            side_dist_curr = min(temp_array[Lidar_l[0]],temp_array[Lidar_l[1]],temp_array[Lidar_l[2]])
            
        if (dir == 'right'):
            side_dist_curr = min(temp_array[Lidar_r[0]],temp_array[Lidar_r[1]],temp_array[Lidar_r[2]])
        if front_dist_curr <= target + 100:
            Chris_R.stop_motors()
            corner(dir)
            

        dt = currentTime - prevTime
        adj, prev_error, integral = PID(target,side_dist_curr,prev_error,integral,dt)
        
        
            
            
            
        prevTime = currentTime
        
     
wall_follow("left")
            
        
    
