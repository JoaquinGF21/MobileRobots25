from robot_systems.robot import HamBot

robot = HamBot

robot.run_left_motor_for_seconds(robot, 3, speed=25, blocking=False)
robot.run_right_motor_for_seconds(robot, 3, speed=25, blocking=False)

robot.stop_motors()