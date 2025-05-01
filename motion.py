from robot_systems.robot import HamBot
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
        Chris_R.run_right_motor_for_rotations(-rotations, 25, True)
        time.sleep(.5)
        
    def forward(rotations):
        Chris_R.run_left_motor_for_rotations(rotations, 35, False)
        Chris_R.run_right_motor_for_rotations(rotations, 35,True)
        time.sleep(.5)
    
    def face(direction, frw_mv=1.6):
        
        match(direction):
            case "N":
                targetAngle = 90
                
            case "E":
                targetAngle = 0
            
            case "S":
                targetAngle = 270
                
            case "W":
                targetAngle = 180
                
        turnAngle = (targetAngle - Movement.currentDirection) % 360
        
        if turnAngle == 0:
            # print("The current direction is " + direction)
            Movement.forward(frw_mv)
            Movement.currentDirection = targetAngle
        
        elif turnAngle == 270 or turnAngle == -90:
            Movement.rotate(90)
            time.sleep(.5)
            # print("The current direction is " + direction)
            Movement.forward(frw_mv)
            Movement.currentDirection = targetAngle  
               
        elif turnAngle == 90 or turnAngle == -270:
            Movement.rotate(-90)
            time.sleep(.5)
            # print("The current direction is " + direction)
            Movement.forward(frw_mv)
            Movement.currentDirection = targetAngle
            
        elif turnAngle == 180 or turnAngle == -180:
            Movement.rotate(90)
            time.sleep(.5)
            Movement.rotate(90)
            time.sleep(.5)
            # print("The current direction is " + direction)
            Movement.forward(frw_mv)
            Movement.currentDirection = targetAngle
    
    def follow_path(directions):
        """
        Follows a path given as a list of directions ('N', 'S', 'E', 'W')
        
        Parameters:
        directions: list - A list of direction characters ('N', 'S', 'E', 'W')
        """
        print("Starting path following with directions:", directions)
        for direction in directions:
            Movement.face(direction)
        print("Path complete!")
