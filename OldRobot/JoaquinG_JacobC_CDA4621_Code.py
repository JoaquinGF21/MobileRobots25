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
  
    controller.set_speed_r(0.5)
    controller.set_speed_l(0.5 + adjl)
    
    end_time = time.perf_counter() + duration
    print(time.perf_counter())
    while time.perf_counter() < end_time:
        print("Still running...")
        time.sleep(0.5)

    
    stop()
    print(time.perf_counter())
    print("Time's up!")

def turnTest():
    duration = .5
    
    controller.set_speed_r(-0.5)
    controller.set_speed_l(0.5)
    
    end_time = time.perf_counter() + duration
    print(time.perf_counter())
    while time.perf_counter() < end_time:
        print("Still running...")
        time.sleep(0.5)

    stop()
    print(time.perf_counter())
    print("Time's up!")

straightTest(5.5)
print("VL: 1.15m/s VR: 1.15m/s")
print("Dist: 1.07 m")
print("Time: 1 sec")
#turnTest()
print("VL: 1.15m/s VR: 1.15m/s")
print("Dist:0.72")
print("Time:")

#straightTest(5.5)
print("VL: 1.15m/s VR: 1.15m/s")
print("Dist: 0.91 m")
print("Time:")
#turnTest()
print("VL: 1.15m/s VR: 1.15m/s")
print("Dist:0.72")
print("Time:")
#straightTest(5.5)
print("VL: 1.15m/s VR: 1.15m/s")
print("Dist: 0.457 m")
print("Time:")
#turnTest()
print("VL: 1.15m/s VR: 1.15m/s")
print("Dist:0.95")
print("Time:")
#straightTest(3)

#turnTest()
#straightTest(2)
print("VL: 1.15m/s VR: 1.15m/s")
print("Dist: 1.91")
print("Time:")
#turnTest()
#straightTest(1)

#turnTest()
