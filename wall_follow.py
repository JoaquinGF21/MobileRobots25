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
def corner(dir):
    if dir == 'right':
        Chris_R.run_left_motor_for_rotations(0.61,-50,False)
        Chris_R.run_right_motor_for_rotations(0.61,50,True)
    elif dir == 'left':
        Chris_R.run_left_motor_for_rotations(0.61,50,False)
        Chris_R.run_right_motor_for_rotations(0.61,-50,True)
            

def wall_follow(dir):
    #initialize current and prev distances along with a temp array to hold the lidar readings
    front_dist_curr = 0
    side_dist_curr = 0
    front_dist_prev = 0
    side_dist_prev = 0
    
    temp_array = []
    
    while(True):
        Chris_R.set_left_motor_speed(base_speed)
        Chris_R.set_right_motor_speed(base_speed)
        temp_array = Chris_R.get_range_image()
        front_dist_curr = min(temp_array[Lidar_f[0]],temp_array[Lidar_f[1]],temp_array[Lidar_f[2]])
        if (dir == 'left'):
            side_dist_curr = min(temp_array[Lidar_l[0]],temp_array[Lidar_l[1]],temp_array[Lidar_l[2]])
        if (dir == 'right'):
            side_dist_curr = min(temp_array[Lidar_r[0]],temp_array[Lidar_r[1]],temp_array[Lidar_r[2]])
        if front_dist_curr <= 300:
            Chris_R.stop_motors()
            corner(dir)
wall_follow("left")
            
        
    
