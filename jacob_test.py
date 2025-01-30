import time
import robot_controller
import pigpio
import signal
import threading


pigpi = pigpio.pi()

controller = robot_controller.control(pi=pigpi)

def SignalHandler_SIGINT(SignalNumber,Frame):
     print('Stopping Controller')
     controller.set_speed_r(0)
     controller.set_speed_l(0)
     exit(0)


#diameter of wheels is 66mm
#width of robot is 102mm
#register the signal with Signal handler
signal.signal(signal.SIGINT,SignalHandler_SIGINT)


#input dist in cm
#speed is -1 to 1 min to max
#CHANGE CONTROL BACK TO CONTROLLER (only used for ease)
def move_straight(control,speed,dist,tick_speed):
    number_of_tics = (dist/10)/controller.diameter_wheels
    controller.set_speed_l(speed)
    controller.set_speed_r(speed)
    controller.sampling_time = tick_speed
    turns_l = 0
    turns_r = 0

    #set starting angle
    angle_l = controller.get_angle_l()
    angle_r = controller.get_angle_r()

    #find and set target angle
    target_angle_l = controller.get_angle_l(number_of_tics,angle_l)
    target_angle_r = controller.get_angle_r(number_of_tics,angle_r)

    #Posr_r (position_reached_r) Posr_l respectively
    posr_r = False
    posr_l = False

    print(f"Angle L: {str(angle_l)}\n")
    print(f"Angle R: {str(angle_r)}\n")

    while not posr_r and not posr_l:
         loop_time = time.time()

         angle_l = controller.get_angle_l()
         angle_r = controller.get_angle_r()
