from robot_systems.robot import HamBot
import math
import time


Chris_R = HamBot()
time.sleep(2)

def rotate(deg):
    axel = 192
    wheel_diameter = 90
    rotations = (axel * deg) / (360 * wheel_diameter)
    Chris_R.run_left_motor_for_rotations(rotations, 25, False)
    Chris_R.run_right_motor_for_rotations(-rotations,25, True)
    
def forward(rotations):
    Chris_R.run_left_motor_for_rotations(rotations, 35, False)
    Chris_R.run_right_motor_for_rotations(rotations, 35, True)
    
forward(3.5)