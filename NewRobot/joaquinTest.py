from robot_systems.robot import HamBot

robot = HamBot()

robot.check_speed(robot, input_speed=25)

robot.run_left_motor_for_seconds(3.0, speed=25, blocking=False)
robot.run_right_motor_for_seconds(3.0, speed=25, blocking=False)

robot.stop_motors()