import time
import robot_controller
import pigpio
import signal
import threading
import math

adjl = .048
pigpi = pigpio.pi()

controller = robot_controller.control(pi=pigpi)

def SignalHandler_SIGINT(SignalNumber,Frame):
     print('Stopping Controller')
     controller.set_speed_r(0)
     controller.set_speed_l(0)
     exit(0)
     
signal.signal(signal.SIGINT,SignalHandler_SIGINT)


def move_straight(controller, speed, dist, tick_speed):
    # Convert distance to mm (assuming dist is in cm)
    dist_mm = dist * 10
    number_of_ticks = dist_mm / controller.tick_length()
    
    # Apply speed adjustment
    controller.set_speed_l(speed + adjl)
    controller.set_speed_r(speed)
    controller.sampling_time = tick_speed

    # Initialize tracking variables
    turns_l = turns_r = 0
    prev_angle_l = controller.get_angle_l()
    prev_angle_r = controller.get_angle_r()
    
    # Calculate target angles
    target_angle_l = controller.get_target_angle(number_of_ticks, prev_angle_l)
    target_angle_r = controller.get_target_angle(number_of_ticks, prev_angle_r)
    
    total_angle_l = prev_angle_l
    total_angle_r = prev_angle_r
    
    while True:
        loop_start = time.time()
        
        # Get current angles
        current_angle_l = controller.get_angle_l()
        current_angle_r = controller.get_angle_r()
        
        # Calculate angle changes since last iteration
        try:
            turns_l, total_angle_l = controller.get_total_angle(
                current_angle_l, 
                controller.unitsFC, 
                prev_angle_l,
                turns_l
            )
            turns_r, total_angle_r = controller.get_total_angle(
                current_angle_r,
                controller.unitsFC,
                prev_angle_r,
                turns_r
            )
            
            # Check if target reached for each wheel
            if total_angle_r >= target_angle_r:
                controller.set_speed_r(0.0)
            if total_angle_l >= target_angle_l:
                controller.set_speed_l(0.0)
                
            # Stop if both wheels reached target
            if total_angle_r >= target_angle_r and total_angle_l >= target_angle_l:
                break
                
        except Exception as e:
            print(f"Error during movement: {str(e)}")
            # Don't swallow the error silently - at least log it
            
        # Update previous angles for next iteration
        prev_angle_l = current_angle_l
        prev_angle_r = current_angle_r
        
        # Calculate remaining loop time and sleep precisely
        elapsed = time.time() - loop_start
        sleep_time = max(0, controller.sampling_time - elapsed)
        if sleep_time > 0:
            time.sleep(sleep_time)
    
    # Ensure full stop
    controller.set_speed_r(0)
    controller.set_speed_l(0)
    return None