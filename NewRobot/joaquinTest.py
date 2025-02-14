from robot_systems.robot import HamBot

robot = HamBot

robot.set_left_motor_speed(25)
robot.set_right_motor_speed(25)

robot.run_left_motor_for_seconds(3)

robot.stop_motors()