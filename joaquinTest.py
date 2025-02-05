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
<<<<<<< HEAD
def SignalHandler_SIGINT(SignalNumber,Frame):
     print('Stopping Controller')
     controller.set_speed_r(0)
     controller.set_speed_l(0)
     exit(0)

#register the signal with Signal handler
signal.signal(signal.SIGINT,SignalHandler_SIGINT)
=======


# I threw some comments for things to change

>>>>>>> 12719d55b9a11f7bcef8e04d592d14eae222d5de

def move_forward(robot, speed=0.5, duration=2.0):
    #what is this for?
    speed = max(0, min(1, speed))
    
<<<<<<< HEAD
    robot.servo_l.set_speed(-0.54)
=======
    robot.servo_l.set_speed(-speed) #DON'T FLIP THE NEGATIVE
>>>>>>> 12719d55b9a11f7bcef8e04d592d14eae222d5de
    robot.servo_r.set_speed(speed)
    
    time.sleep(duration)
    
    robot.servo_l.set_speed(0)
    robot.servo_r.set_speed(0)

def turn_robot(robot, left_speed, right_speed, duration):

    left_speed = max(-1, min(1, left_speed))
    right_speed = max(-1, min(1, right_speed))


#for this just use the command controller.set_speed_l/speed_r just makes it so you don't have to include the negative
    robot.servo_l.set_speed(-left_speed) #DON'T FLIP THE NEGATIVE
    robot.servo_r.set_speed(right_speed)
    


    time.sleep(duration)


# same here
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