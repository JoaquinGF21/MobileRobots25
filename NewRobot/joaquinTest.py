from robot_systems.robot import HamBot

# Create instance of HamBot
robot = HamBot()

#Inputs: time (float), velocity (int), block (bool)
def moveForward(t, v, blocking):
    robot.run_left_motor_for_seconds(t, speed=v, blocking=blocking)
    robot.run_right_motor_for_seconds(t, speed=v, blocking=blocking)

    robot.stop_motors()

moveForward(5.0, 50, False)