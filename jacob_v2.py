import time
import robot_controller
import pigpio
import signal
import threading
import math

adjl = .0466
velocity = 0
distance = 0
ROC_last_t = None
ROC_last_a = None
pigpi = pigpio.pi()
Default_accel = (0,0,0)
controller = robot_controller.control(pi=pigpi)

def SignalHandler_SIGINT(SignalNumber,Frame):
     print('Stopping Controller')
     controller.set_speed_r(0)
     controller.set_speed_l(0)
     exit(0)
     
signal.signal(signal.SIGINT,SignalHandler_SIGINT)

def reset():
    global velocity, distance
    velocity = 0
    distance = 0
    ROC_last_t = None
    ROC_last_a = None

def stop():
    controller.set_speed_r(0)
    controller.set_speed_l(0)
    return None
def find_ROC_Angle(current_a):
    global ROC_last_a, ROC_last_t
    current_time = time.time()
    #normalize the angle
    current_a = current_a % 360

    if ROC_last_t is None or ROC_last_a is None:
        ROC_last_t = current_time
        ROC_last_a = current_a
        
        return 0.0
    
    angle_change = current_a - ROC_last_a
    #print(f"current {current_a} - ROC {ROC_last_a} = {angle_change}")
    if angle_change > 180:
        angle_change -= 360
    elif angle_change < -180:
        angle_change += 360
    #print(angle_change)
    #print()
        
    time_change = current_time - ROC_last_t
    #print(f" current {current_time} - ROC {ROC_last_t} = {time_change}")
    #ROC rate of change
    ROC = angle_change / time_change

    ROC_last_t = current_time
    ROC_last_a = current_a
    print(ROC)
    return ROC
#{x,y,z} for linear_acceleration
#dt is the time interval between use of the function
# I took the skeleton of this function from Clause ai

def calculate_distance(acceleration,dt):
    global velocity, distance
    if -.4 <= acceleration <= .4:
        acceleration = 0
    else:
        pass
    velocity += acceleration *dt
    
    distance += velocity *dt
    
    return distance * 100

def move_straight(control,speed,distance,tick_speed,kp = .001):
    current = time.perf_counter()
    last = time.perf_counter()
    controller.sampling_time = tick_speed
    accel = controller.imu.linear_acceleration
    speed_l = speed + adjl
    controller.set_speed_r(speed)
    controller.set_speed_l(speed_l)
    correction = 0
    #gets starting heading 
    values = controller.imu.magnetic
    print(values)
    setpoint = 180 + math.atan2(values[1], values[0]) * 180 / math.pi
    print(f"Start heading: {setpoint}")
    pos = False
    while not pos:
        current = time.perf_counter()
        # Get current heading
        values = controller.imu.magnetic
        current_angle = 180 + math.atan2(values[1], values[0]) * 180 / math.pi
        rate = find_ROC_Angle(current_angle)
        if rate <= -.05:
            correction += .002
        elif rate >= 0.5:
            correction -= .001
        #print(f"{rate} : {correction}")
        accel = controller.imu.linear_acceleration
        if accel[1] == None:
            accel = Default_accel
        #try needed because last isn't initialized yet
        #use accel[1]
        #print(f"{accel[1]} : {calculate_distance(accel[1],current - last)}")
        if distance <= calculate_distance(accel[1],current - last):
            pos = True
            break
        else:
            pass
        

        time.sleep(controller.sampling_time -
                   ((time.perf_counter() - current) % controller.sampling_time))
        last = current
        
    stop()
    time.sleep(1)
    
# relativily 1m seems to vary about 10cm
reset()
move_straight(controller,0.5,300,.03)
# print("\n\n\n")
# reset_distance()
# move_straight(controller,0.5,140,.03)
# print("\n\n\n")
# reset_distance()
# move_straight(controller,0.5,140,.03)
# print("\n\n\n")
# reset_distance()