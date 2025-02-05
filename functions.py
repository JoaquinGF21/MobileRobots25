#space for important functions
import time
import robot_controller
import pigpio
import signal
import threading
import math
adjl = 0.49
pigpi = pigpio.pi()

controller = robot_controller.control(pi=pigpi)

# Ctr - C stop function
def SignalHandler_SIGINT(SignalNumber,Frame):
     print('Stopping Controller')
     controller.set_speed_r(0)
     controller.set_speed_l(0)
     exit(0)
     
signal.signal(signal.SIGINT,SignalHandler_SIGINT)

def stop():
      controller.set_speed_r(0)
      controller.set_speed_l(0)


def move_straight(controller,speed,dist,tick_speed):

     number_of_tics = (dist*10)/controller.tick_length()
     controller.set_speed_l(speed+adjl)
     controller.set_speed_r(speed)
     controller.sampling_time = tick_speed
     turns_l = 0
     turns_r = 0

     #set starting angle
     angle_l = controller.get_angle_l()
     angle_r = controller.get_angle_r()

     #find and set target angle
     target_angle_l = controller.get_target_angle(number_of_tics,angle_l)
     target_angle_r = controller.get_target_angle(number_of_tics,angle_r)
     
     print(f"TargetangleL: {target_angle_l}")
     print(f"targetangleR: {target_angle_r}")
     #Posr_r (position_reached_r) Posr_l respectively
     posr_r = False
     posr_l = False

     print(f"Angle L: {str(angle_l)}\n")
     print(f"Angle R: {str(angle_r)}\n")

     while not posr_r or not posr_l:
          loop_time = time.time()

          angle_l = controller.get_angle_l()
          angle_r = controller.get_angle_r()
          
          print(controller.imu.gyro)
          try:
                    #try needed for exception
                    turns_l,total_angle_l = controller.get_total_angle(angle_l,controller.unitsFC,prev_angle_l,turns_l)
                    turns_r,total_angle_r = controller.get_total_angle(angle_r,controller.unitsFC,prev_angle_r,turns_r)
                    print(f"total Angle L: {total_angle_l}")
                    print(f"total Angle R: {total_angle_r}")
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
                    stop()
                    posr_r = True
                    break
               else:
                    pass
               if target_angle_l <= total_angle_l:
                    stop()
                    posr_l = True
                    break
               else:
                    pass
          except Exception:
                pass
          #pause controller for sampling_time
          time.sleep(controller.sampling_time -
                   ((time.time() - loop_time) % controller.sampling_time))
          print('{:.20f}'.format((time.time() - loop_time)))
     time.sleep(1)
     return None
print()
def manual_curve(controller,degrees,radius,Vr,Vl,tick_speed):
     radians = degrees *(math.pi/180)
     controller.sampling_time = tick_speed
     radius = radius/10
     turns_l = 0
     turns_r = 0
     controller.set_speed_l(Vl)
     controller.set_speed_r(Vr)
#dealing with distance each wheel must travel first
     central_dist = radians * radius
     
     #refers to the individual circles created by the left and right wheel
     #radians * radius(l/r)
     dist_lw = abs(radians * (radius - controller.width_robot))
     dist_rw = abs(radians * (radius + controller.width_robot))
     
     #not (number of ticks)
     not_l = dist_rw/controller.tick_length()
     not_r = dist_lw/controller.tick_length()
     
     #determine angles
     angle_l = controller.get_angle_l()
     angle_r = controller.get_angle_r()
     
     target_angle_l = controller.get_target_angle(not_l,angle_l)
     target_angle_r = controller.get_target_angle(not_r,angle_r)
     
     #position reacher = pos
     pos_l = False
     pos_r = False
     while not posr_r or not posr_l:
          loop_time = time.time()

          angle_l = controller.get_angle_l()
          angle_r = controller.get_angle_r()
          
          print(controller.imu.gyro)
          try:
                    #try needed for exception
                    turns_l,total_angle_l = controller.get_total_angle(angle_l,controller.unitsFC,prev_angle_l,turns_l)
                    turns_r,total_angle_r = controller.get_total_angle(angle_r,controller.unitsFC,prev_angle_r,turns_r)
                    print(f"total Angle L: {total_angle_l}")
                    print(f"total Angle R: {total_angle_r}")
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
                    stop()
                    posr_r = True
                    break
               else:
                    pass
               if target_angle_l <= total_angle_l:
                    stop()
                    posr_l = True
                    break
               else:
                    pass
          except Exception:
                pass
          #pause controller for sampling_time
          time.sleep(controller.sampling_time -
                   ((time.time() - loop_time) % controller.sampling_time))
          print('{:.20f}'.format((time.time() - loop_time)))
     time.sleep(1)
     return None