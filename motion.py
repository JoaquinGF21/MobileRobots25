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
        time.sleep(.5)
        
    def forward(rotations):
        Chris_R.run_left_motor_for_rotations(rotations, 35, False)
        Chris_R.run_right_motor_for_rotations(rotations, 35, True)
        time.sleep(.5)
    
    def face(direction):     
        match(direction):
            case "N":
                pass
            
            case "E":
                Movement.rotate(90)
                time.sleep(.5)
            
            case "S":
                Movement.rotate(90)
                time.sleep(.5)
                Movement.rotate(90)
                time.sleep(.5)
                
            case "W":
                Movement.rotate(-90)
                time.sleep(.5)
    
Movement.face('W')
Movement.forward(1.63)
Movement.forward(1.63)
Movement.face('E')
Movement.forward(1.63)
Movement.forward(1.63)
    