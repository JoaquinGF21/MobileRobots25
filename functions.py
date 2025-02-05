#space for important functions
import time
import robot_controller
import pigpio
import signal
import threading
import math

pigpi = pigpio.pi()

controller = robot_controller.control(pi=pigpi)

# Ctr - C stop function
def SignalHandler_SIGINT(SignalNumber,Frame):
     print('Stopping Controller')
     controller.set_speed_r(0)
     controller.set_speed_l(0)
     exit(0)
     
signal.signal(signal.SIGINT,SignalHandler_SIGINT)