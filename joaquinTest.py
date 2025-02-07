import time
import robot_controller
import pigpio
import signal
import threading
import math

adjl = .0465
pigpi = pigpio.pi()

controller = robot_controller.control(pi=pigpi)

def SignalHandler_SIGINT(SignalNumber,Frame):
     print('Stopping Controller')
     controller.set_speed_r(0)
     controller.set_speed_l(0)
     exit(0)
     
signal.signal(signal.SIGINT,SignalHandler_SIGINT)


def stop():
    controller.set_speed_r(0)
    controller.set_speed_l(0)
    return None
#{x,y,z} for linear_acceleration
#dt is the time interval between use of the function
# I took the skeleton of this function from Clause ai
velocity = 0
distance = 0
Default_accel = (0,0,0)
def calculate_distance(acceleration,dt):
    global velocity, distance
    
    velocity += acceleration *dt
    
    distance += velocity *dt
    return distance * 100

def move_straight(control, speed, distance, tick_speed, kp=0.1):
    current = time.perf_counter()
    last = time.perf_counter()
    controller.sampling_time = tick_speed
    
    # Get initial heading as setpoint
    values = controller.imu.magnetic
    setpoint = 180 + math.atan2(values[1], values[0]) * 180 / math.pi
    
    pos = False
    while not pos:
        current = time.perf_counter()
        
        # Get current heading
        values = controller.imu.magnetic
        current_heading = 180 + math.atan2(values[1], values[0]) * 180 / math.pi
        
        # Calculate heading error and correction
        error = setpoint - current_heading
        correction = kp * error
        
        # Apply corrections to wheel speeds
        controller.set_speed_l(speed + correction)
        controller.set_speed_r(speed - correction)
        
        # Distance calculation
        accel = controller.imu.linear_acceleration or Default_accel
        if distance <= calculate_distance(accel[1], current - last):
            pos = True
            break
            
        time.sleep(controller.sampling_time -
                   ((time.perf_counter() - current) % controller.sampling_time))
        last = current
        
    stop()

    
# relativily 1m seems to vary about 1 square
#move_straight(controller,0.5,160,.03)
move_straight(controller,0.5,450,0.03)