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

def move_straight(control,speed,distance,tick_speed):
    start = time.time()
    controller.sampling_time = tick_speed
    controller.set_speed_l(speed + adjl)
    controller.set_speed_r(speed)
    while time.time() != start + 2:
        loop_time = time.time()
        accel = controller.imu.linear_acceleration
        print(accel[0])
#{z, }
        time.sleep(controller.sampling_time -
                   ((time.time() - loop_time) % controller.sampling_time))
        print('{:.20f}'.format((time.time() - loop_time)))

    stop()
    
    
move_straight(controller,0.5,15,.02)