import time
import robot_controller
import pigpio
import signal
import threading
import functions

move_straight = functions.move_straight
manual_curve = functions.manual_curve
pigpi = pigpio.pi()

controller = robot_controller.control(pi=pigpi)

def SignalHandler_SIGINT(SignalNumber,Frame):
     print('Stopping Controller')
     controller.set_speed_r(0)
     controller.set_speed_l(0)
     exit(0)

#register the signal with Signal handler
signal.signal(signal.SIGINT,SignalHandler_SIGINT)

manual_curve(controller,90,34.5,0.5,0.25,0.2)
