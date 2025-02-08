import time
import robot_controller
import pigpio
import signal
import threading
import math

adjl = .0465
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

def turn(controller, speed, target_angle, tick_speed, kp=0.001):
    """
    Turn the robot by a specified angle
    
    Args:
        controller: robot controller instance
        speed: base turning speed (positive for right turn, negative for left turn)
        target_angle: desired angle to turn in degrees (positive for right turn, negative for left turn)
        tick_speed: sampling time interval
        kp: proportional control constant
    """
    current = time.perf_counter()
    controller.sampling_time = tick_speed
    
    # Get initial heading
    values = controller.imu.magnetic
    initial_heading = 180 + math.atan2(values[1], values[0]) * 180 / math.pi
    
    # Calculate target heading
    target_heading = initial_heading + target_angle
    # Normalize to 0-360 range
    target_heading = target_heading % 360
    
    # Set initial wheel speeds for turning
    if target_angle > 0:  # Right turn
        controller.set_speed_r(-speed)
        controller.set_speed_l(speed)
    else:  # Left turn
        controller.set_speed_r(speed)
        controller.set_speed_l(-speed)
    
    while True:
        # Get current heading
        values = controller.imu.magnetic
        current_heading = 180 + math.atan2(values[1], values[0]) * 180 / math.pi
        
        # Calculate error (shortest angle between current and target heading)
        error = ((target_heading - current_heading + 180) % 360) - 180
        
        # If we're close enough to target angle, stop
        if abs(error) < 2:  # 2 degrees tolerance
            break
            
        # Calculate speed adjustment based on error
        adjustment = kp * abs(error)
        # Limit maximum adjustment
        adjustment = min(adjustment, speed)
        
        # Apply proportional control
        if target_angle > 0:  # Right turn
            controller.set_speed_r(-speed * adjustment)
            controller.set_speed_l(speed * adjustment)
        else:  # Left turn
            controller.set_speed_r(speed * adjustment)
            controller.set_speed_l(-speed * adjustment)
            
        print(f"Current: {current_heading:.1f}, Target: {target_heading:.1f}, Error: {error:.1f}")
        
        time.sleep(controller.sampling_time -
                  ((time.perf_counter() - current) % controller.sampling_time))
        current = time.perf_counter()
    
    stop()

# Test the turn function

    # Example: Turn 90 degrees right
turn(controller, 0.3, 90, 0.03)
time.sleep(1)  # Wait a second between turns
    
    # Example: Turn 90 degrees left
turn(controller, 0.3, -90, 0.03)