import time
import robot_controller
import pigpio
import signal
import threading
import math

adjl = .0463
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
def calculate_distance(acceleration,dt):
    global velocity, distance
    
    velocity += acceleration *dt
    
    distance += velocity *dt
    return distance

def move_straight(control,speed,distance,tick_speed):
    current = time.time()
    controller.sampling_time = tick_speed
    controller.set_speed_l(speed + adjl)
    controller.set_speed_r(speed)
    pos = False
    while not pos:
        current = time.time()
        # values = controller.imu.magnetic
        # print("Heading: " + str(180 + math.atan2(values[1], values[0]) * 180 / math.pi))
        accel = controller.imu.linear_acceleration
        #try needed because last isn't initialized yet
        try:
            if distance >= calculate_distance(accel[1],current - last):
                pos = True
                break
            else:
                pass
        except Exception:
            pass
        time.sleep(controller.sampling_time -
                   ((time.time() - current) % controller.sampling_time))
        last = current
        #use accel[1]
        

    
    
move_straight(controller,0.5,15,.02)