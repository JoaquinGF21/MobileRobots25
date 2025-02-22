from HamBot.robot import HamBot
# Create instance of HamBot
robot = HamBot(lidar_enabled=True)

#Inputs: time (float), velocity (int), block (bool)
def moveForward(t, v, blocking):
    robot.run_motors_for_seconds(t, left_speed=v, right_speed=v)

    robot.stop_motors()

#moveForward(5.0, 50, True)
#hi
# Get the current range image from the Lidar
range_image = robot.get_range_image()
print(f"Range image: {range_image[:10]}")  # Print the first 10 values