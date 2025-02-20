from robot_systems.robot import HamBot
# Create instance of HamBot
robot = HamBot()

#Inputs: time (float), velocity (int), block (bool)
def moveForward(t, v, blocking):
    robot.run_motors_for_seconds(t, left_speed=v, right_speed=v)

    robot.stop_motors()

#moveForward(5.0, 50, True)
j = 0
while j < 10:
    j = HamBot.get_range_image()
    print(j)
    j = j + 1
