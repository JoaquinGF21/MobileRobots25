import time
import robot_controller
import pigpio
import signal
import threading
import math

adjl = .0465
pigpi = pigpio.pi()
Default_accel = (0,0,0)
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
def calculate_distance(acceleration,dt):
    global velocity, distance
    if -.05 <= acceleration <= .05:
        acceleration = 0
    else:
        pass
    velocity += acceleration *dt
    
    distance += velocity *dt
    
    return distance * 100

def move_straight(control,speed,distance,tick_speed):
    current = time.perf_counter()
    last = time.perf_counter()
    controller.sampling_time = tick_speed
    controller.set_speed_l(speed + adjl)
    controller.set_speed_r(speed)
    pos = False
    while not pos:
        current = time.perf_counter()
        # values = controller.imu.magnetic
        # print("Heading: " + str(180 + math.atan2(values[1], values[0]) * 180 / math.pi))
        accel = controller.imu.linear_acceleration or Default_accel
        #try needed because last isn't initialized yet
        #use accel[1]
        print(f"{accel[1]} : {calculate_distance(accel[1],current - last)}")
        if distance <= calculate_distance(accel[1],current - last):
            pos = True
            break
        else:
            pass
        

        time.sleep(controller.sampling_time -
                   ((time.perf_counter() - current) % controller.sampling_time))
        last = current
        
    stop()

    
# relativily 1m seems to vary about 10cm
move_straight(controller,0.5,450,.03)