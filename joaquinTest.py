import pigpio
import time
from robot_controller import control 

def move_forward(robot, speed=0.5, duration=2.0):
    # Ensure speed is between 0 and 1
    speed = max(0, min(1, speed))
    
    # Set both wheels to move forward
    robot.servo_l.set_speed(-speed)  # Negative for forward
    robot.servo_r.set_speed(speed)   # Positive for forward
    
    time.sleep(duration)
    
    robot.servo_l.set_speed(0)
    robot.servo_r.set_speed(0)

def main():

    pi = pigpio.pi()
    
    robot = control(pi=pi)
    
    try:
        move_forward(robot, speed=0.5, duration=2.0)
    
    finally:
        robot.cancel()
        pi.stop()

if __name__ == "__main__":
    main()