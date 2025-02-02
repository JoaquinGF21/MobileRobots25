import time
import robot_controller
import pigpio
import signal
import threading
import math

pigpi = pigpio.pi()

controller = robot_controller.control(pi=pigpi)

def SignalHandler_SIGINT(SignalNumber,Frame):
     print('Stopping Controller')
     controller.set_speed_r(0)
     controller.set_speed_l(0)
     exit(0)
     
signal.signal(signal.SIGINT,SignalHandler_SIGINT)


def stop(self):
      controller.set_speed_r(0)
      controller.set_speed_l(0)

#diameter of wheels is 66mm
#width of robot is 102mm
#register the signal with Signal handler



#input dist in cm
#speed is -1 to 1 min to max
#CHANGE CONTROL BACK TO CONTROLLER (only used for ease)
def move(controller, Vl, Vr, D, T):

    number_ticks = D/controller.tick_length()

    controller.sampling_time = T
    turns_l = 0
    turns_r = 0

    angle_l = controller.get_angle_l()
    angle_r = controller.get_angle_r()

    '''print("Angle L: " + str(angle_l))
    print("Angle R: " + str(angle_r))'''

    target_angle_r = controller.get_target_angle(
        number_ticks=number_ticks, angle=angle_r)
    target_angle_l = controller.get_target_angle(
        number_ticks=number_ticks, angle=angle_l)

   #print("Target Angle L: " + str(target_angle_l))
    #print("Target Angle R: " + str(target_angle_r))

    position_reached_l = False
    position_reached_r = False
    reached_sp_counter = 0
    # position must be reached for one second to allow
    # overshoots/oscillations before stopping control loop
    wait_after_reach_sp = 1/controller.sampling_time

    # start time of the control loop
    start_time = time.time()

    # control loop:
    while not position_reached_r and not position_reached_l:
        # DEBUGGING OPTION:
        # printing runtime of loop , see end of while true loop
        start_time_each_loop = time.time()

        angle_l = controller.get_angle_l()
        angle_r = controller.get_angle_r()
#             print("Angle L: " + str(angle_l))
#             print("Angle R: " + str(angle_r))

        print(controller.imu.gyro)

        # try needed, because:
        # - first iteration of the while loop prev_angle_* is missing and the
        # method controller.get_total_angle() will throw an exception.
        # - second iteration of the while loop prev_total_angle_* is missing,
        # which will throw another exception
        try:
            turns_l, total_angle_l = controller.get_total_angle(
                angle_l, controller.unitsFC, prev_angle_l, turns_l)
            turns_r, total_angle_r = controller.get_total_angle(
                angle_r, controller.unitsFC, prev_angle_r, turns_r)

            '''print("Total Angle L: " + str(total_angle_l))
            print("Total Angle R: " + str(total_angle_r))'''
            # controller.set_speed_r(1)
            # controller.set_speed_l(0)

        except Exception:
            pass

        prev_angle_l = angle_l
        prev_angle_r = angle_r

        # try needed, because first iteration of the while loop prev_angle_* is
        # missing and the method controller.get_total_angle() will throw an exception,
        # and therefore no total_angle_* gets calculated

        try:
            prev_total_angle_l = total_angle_l
            prev_total_angle_r = total_angle_r
        except Exception:
            pass

        try:
            #                 controller.set_speed_l(0.0)
            #                 controller.set_speed_r(0.0)
            reached_sp_counter += 1

#                 if reached_sp_counter >= wait_after_reach_sp:

            if target_angle_r <= total_angle_r:
                controller.set_speed_r(0.0)
                position_reached_r = True
            else:
                pass
            if target_angle_l <= total_angle_l:
                controller.set_speed_l(0.0)
                position_reached_l = True
            else:
                pass

        except Exception:
            pass

        # Pause control loop for chosen sample time
        # https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds-in-python/25251804#25251804
        time.sleep(controller.sampling_time -
                   ((time.time() - start_time) % controller.sampling_time))

        # DEBUGGING OPTION:
        # printing runtime of loop, see beginning of while true loop
        print('{:.20f}'.format((time.time() - start_time_each_loop)))

    return None
#direct will be right if negative
#speed will be set at a percentage
def move_curve(control,radius,degrees,direct,speed,tick_speed):
     radians = degrees *(math.pi/180)
     controller.sampling_time = tick_speed
     speed = speed/100
     radius = radius/10
     turns_l = 0
     turns_r = 0
#dealing with distance each wheel must travel first
     central_dist = radians * radius
     
     #refers to the individual circles created by the left and right wheel
     #radians * radius(l/r)
     dist_lw = abs(radians * (radius - controller.width_robot()))
     dist_rw = abs(radians * (radius + controller.width_robot()))
     
     #not (number of ticks)
     not_l = dist_rw/controller.tick_length
     not_r = dist_lw/controller.tick_length
     
     #determine angles
     angle_l = controller.get_angle_l()
     angle_r = controller.get_angle_r()
     
     target_angle_l = controller.get_target_angle(not_l,angle_l)
     target_angle_r = controller.get_target_angle(not_r,angle_r)
     
     #position reacher = pos
     pos_l = False
     pos_r = False
     
#find and set speeds
     if radius < 0:
          #spd (speed)
          spd_lw = 1 * speed
          spd_rw = spd_lw((abs(radius) + controller.width_robot)/(abs(radius) - controller.width_robot))
     else:
          spd_rw = 1 * speed
          spd_lw = spd_rw((abs(radius) - controller.width_robot)/(abs(radius) + controller.width_robot))
          
     controller.set_speed_l(spd_lw)
     controller.set_speed_r(spd_rw)     
     while not posr_r and not posr_l:
               loop_time = time.time()

               angle_l = controller.get_angle_l()
               angle_r = controller.get_angle_r()
               try:
                         #try needed for exception
                         turns_l,total_angle_l = controller.get_total_angle(angle_l,controller.unitsFC,prev_angle_l,turns_l)
                         turns_r,total_angle_r = controller.get_total_angle(angle_r,controller.unitsFC,prev_angle_r,turns_r)
               except Exception:
                    pass
               prev_angle_l = angle_l
               prev_angle_r = angle_r


               try:
                    prev_angle_l = total_angle_l
                    prev_angle_r = total_angle_r
               except Exception:
                    pass
               
               try:
                    
                    if target_angle_r <= total_angle_r:
                         controller .set_speed_r(0.0)
                         posr_r = True
                    else:
                         pass
                    if target_angle_l <= total_angle_l:
                         controller.set_speed_l(0.0)
                         posr_l = True
                    else:
                         pass
               except Exception:
                    pass
               #pause controller for sampling_time
               time.sleep(controller.sampling_time -
                    ((time.time() - loop_time) % controller.sampling_time))
     return None
          


move(controller,2,2,1000,0.2)