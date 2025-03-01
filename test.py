from robot_systems.robot import HamBot
import math
import time


Chris_R = HamBot()
time.sleep(20)

Chris_R.set_left_motor_speed(50)
Chris_R.set_right_motor_speed(50)
time.sleep(2)
Chris_R.stop_motors()