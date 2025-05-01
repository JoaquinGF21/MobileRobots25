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
                
        turnAngle = (targetAngle - Movement.currentDirection) % 360
        
        if turnAngle == 0:
            print("The current direction is " + direction)
            Movement.forward(1.63)
            Movement.currentDirection = targetAngle
        
        elif turnAngle == 270 or turnAngle == -90:
            Movement.rotate(90)
            time.sleep(.5)
            print("The current direction is " + direction)
            Movement.forward(1.63)
            Movement.currentDirection = targetAngle  
               
        elif turnAngle == 90 or turnAngle == -270:
            Movement.rotate(-90)
            time.sleep(.5)
            print("The current direction is " + direction)
            Movement.forward(1.63)
            Movement.currentDirection = targetAngle
            
        elif turnAngle == 180 or turnAngle == -180:
            Movement.rotate(90)
            time.sleep(.5)
            Movement.rotate(90)
            time.sleep(.5)
            print("The current direction is " + direction)
            Movement.forward(1.63)
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


# Example usage with directions list
# Uncomment to test
test_directions = ['W', 'W', 'N', 'N', 'E', 'S', 'E', 'S']
Movement.follow_path(test_directions)

# Example of how to use with Dijkstra's algorithm output
"""
# Import your Dijkstra implementation
from dijkstra import dijkstra_path_directions

# Define the adjacency list (your maze structure)
adjacency_list = {
    0: [1, 3],
    1: [0, 4],
    2: [5],
    3: [0, 6],
    4: [1, 5],
    5: [2, 8],
    6: [3, 7],
    7: [6, 8],
    8: [5, 7]
}

# Find path from start to end
start = 0  # Top-left
end = 8    # Bottom-right

# Get directions using Dijkstra's algorithm
directions = dijkstra_path_directions(adjacency_list, start, end)

# Follow the path if directions exist
if directions:
    Movement.follow_path(directions)
else:
    print("No path exists from start to end")
"""