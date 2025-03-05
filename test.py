from robot_systems.robot import HamBot
import math
import time


Chris_R = HamBot()
#time.sleep(22)

# Lidar_l = [89,90,91]
# Lidar_r = [269,270,271]
# Lidar_f = [179,180,181]
# Lidar_b = [359,0,1]

# while(True):
#     temp_array = Chris_R.get_range_image()
#     front_dist_curr = min(temp_array[Lidar_f[0]],temp_array[Lidar_f[1]],temp_array[Lidar_f[2]])
#     print(front_dist_curr)
temp_array = Chris_R.get_range_image()
print(temp_array)
def corner():
    Chris_R.set_right_motor_speed(30)
    Chris_R.set_left_motor_speed(-30)
corner()