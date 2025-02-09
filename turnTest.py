import time
import robot_controller
import pigpio
import signal
import threading
import math

adjl = .0466
pigpi = pigpio.pi()
Default_accel = (0,0,0)
controller = robot_controller.control(pi=pigpi)

def SignalHandler_SIGINT(SignalNumber,Frame):
     print('Stopping Controller')
     controller.set_speed_r(0)
     controller.set_speed_l(0)
     exit(0)
     
signal.signal(signal.SIGINT,SignalHandler_SIGINT)

def reset_distance():
    global velocity, distance
    velocity = 0
    distance = 0

def stop():
    controller.set_speed_r(0)
    controller.set_speed_l(0)
    return None

def turnTest():
    duration = 5
    end_time = time.perf_counter() + duration

    while time.perf_counter() < end_time:
        # Your code here
        #This should turn left for 5 seconds
        controller.set_speed_r(.5)
        controller.set_speed_l(-.5)
        print("Still running...")
        time.sleep(0.5)

    print("Time's up!")
