from robot_systems.robot import HamBot
import math
import time
Chris_R = HamBot()
time.sleep(2)

class Movement:
    currentDirection = 90
    
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
                targetAngle = 90
                
            case "E":
                targetAngle = 0
            
            case "S":
                targetAngle = 270
                
            case "W":
                targetAngle = 180
                
        turnAngle = targetAngle - Movement.currentDirection
        
        if turnAngle == 0:
            print("The current direction is " + direction)
            Movement.forward(1.63)
        
        elif turnAngle == 270:
            Movement.rotate(90)
            time.sleep(.5)
            print("The current direction is " + direction)
            Movement.forward(1.63)
            Movement.currentDirection = 270  
               
        elif turnAngle == 90:
            Movement.rotate(-90)
            time.sleep(.5)
            print("The current direction is " + direction)
            Movement.forward(1.63)
            Movement.currentDirection = 90
            
        elif turnAngle == 180:
            Movement.rotate(90)
            time.sleep(.5)
            Movement.rotate(90)
            time.sleep(.5)
            print("The current direction is " + direction)
            Movement.forward(1.63)
            Movement.currentDirection = 180
        

Movement.face('W')
Movement.face('W')
Movement.face('N')
Movement.face('S')
Movement.face('E')

"""
Hard coded maze from cell 8 through entire thing and back to cell 8
Movement.face('W')
Movement.forward(1.63)
Movement.forward(1.63)
Movement.face('E')
Movement.forward(1.63)
Movement.forward(1.63)
Movement.face('E')
Movement.forward(1.63)
Movement.face('E')
Movement.forward(1.63)
Movement.face('W')
Movement.forward(1.63)
Movement.face('W')
Movement.forward(1.63)
Movement.face('S')
Movement.forward(1.63)
Movement.forward(1.63)
Movement.face('S')
"""
    