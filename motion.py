from robot_systems.robot import HamBot
import math
import time
Chris_R = HamBot()
time.sleep(2)

class Movement:
    def rotate(deg):
        axel = 192
        wheel_diameter = 90
        rotations = (axel * deg) / (360 * wheel_diameter)
        Chris_R.run_left_motor_for_rotations(rotations, 25, False)
        Chris_R.run_right_motor_for_rotations(-rotations,25, True)
        
    def forward(rotations):
        Chris_R.run_left_motor_for_rotations(rotations, 35, False)
        Chris_R.run_right_motor_for_rotations(rotations, 35, True)
    
    def face(direction):     
        match(direction):
            case("N"):
                return()
            
            case("E"):
                rotate(-90)
            
            case("S"):
                rotate(90)
                time.sleep(.5)
                rotate(90)
                
            case("W"):
                rotate(-90)
    
    face('W')
    forward(3.5)
    