import pigpio
import time
import signal
from robot_controller import control 

"""
IMPORTANT TO REMEMBER
LEFT:   BACKWARDS IS +
        FORWARDS IS -

RIGHT:  BACKWARDS IS -
        FORWARDS IS +
        
"""
def SignalHandler_SIGINT(SignalNumber,Frame):
     print('Stopping Controller')
     controller.set_speed_r(0)
     controller.set_speed_l(0)
     exit(0)

#register the signal with Signal handler
signal.signal(signal.SIGINT,SignalHandler_SIGINT)

def move_forward(robot, speed=0.5, duration=2.0):
    speed = max(0, min(1, speed))
    
    robot.servo_l.set_speed(-0.54)
    robot.servo_r.set_speed(speed)
    
    time.sleep(duration)
    
    robot.servo_l.set_speed(0)
    robot.servo_r.set_speed(0)

def turn_robot(robot, left_speed, right_speed, duration):

    left_speed = max(-1, min(1, left_speed))
    right_speed = max(-1, min(1, right_speed))
    
    robot.servo_l.set_speed(-left_speed)
    robot.servo_r.set_speed(right_speed)
    
    time.sleep(duration)
    
    robot.servo_l.set_speed(0)
    robot.servo_r.set_speed(0)

def main():

    pi = pigpio.pi()
    
    robot = control(pi=pi)
    
    try:
        move_forward(robot, speed = 0.5, duration = 5)
    
    finally:
        robot.cancel()
        pi.stop()

if __name__ == "__main__":
    main()