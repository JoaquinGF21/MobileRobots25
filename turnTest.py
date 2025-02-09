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

def straightTest(duration):
    # Set speeds once before the loop
    controller.set_speed_r(0.5)
    controller.set_speed_l(0.5 + adlj)
    
    end_time = time.perf_counter() + duration
    print(time.perf_counter())
    while time.perf_counter() < end_time:
        print("Still running...")
        time.sleep(0.5)

    # Stop the motors after the loop
    stop()
    print(time.perf_counter())
    print("Time's up!")

def turnTest():
    duration = 1
    
    # Set speeds once before the loop
    controller.set_speed_r(-0.5)
    controller.set_speed_l(0.5)
    
    end_time = time.perf_counter() + duration
    print(time.perf_counter())
    while time.perf_counter() < end_time:
        print("Still running...")
        time.sleep(0.5)


    # Stop the motors after the loop
    stop()
    print(time.perf_counter())
    print("Time's up!")

straightTest(4)
turnTest()
straightTest(4)
turnTest()
straightTest(4)
turnTest()
straightTest(2.5)
turnTest()
straightTest(2.5)