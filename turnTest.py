def turn(control, speed, target_angle, tick_speed, kp=0.001):
    """
    Turn the robot by a specified angle
    
    Args:
        control: robot controller instance
        speed: base turning speed (positive for right turn, negative for left turn)
        target_angle: desired angle to turn in degrees (positive for right turn, negative for left turn)
        tick_speed: sampling time interval
        kp: proportional control constant
    """
    current = time.perf_counter()
    last = time.perf_counter()
    controller.sampling_time = tick_speed
    
    # Get initial heading
    values = controller.imu.magnetic
    print(values)
    initial_heading = 180 + math.atan2(values[1], values[0]) * 180 / math.pi
    print(f"Start heading: {initial_heading}")
    
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
    
    pos = False
    while not pos:
        current = time.perf_counter()
        
        # Get current heading
        values = controller.imu.magnetic
        current_heading = 180 + math.atan2(values[1], values[0]) * 180 / math.pi
        
        # Calculate error (shortest angle between current and target heading)
        error = ((target_heading - current_heading + 180) % 360) - 180
        
        print(f"Current: {current_heading:.1f}, Target: {target_heading:.1f}, Error: {error:.1f}")
        
        # If we're close enough to target angle, stop
        if abs(error) < 2:  # 2 degrees tolerance
            pos = True
            break
            
        # Calculate speed adjustment based on error
        adjustment = kp * abs(error)
        # Limit maximum adjustment
        adjustment = min(adjustment, 1.0)  # Ensure adjustment doesn't exceed 1
        
        # Apply proportional control
        if target_angle > 0:  # Right turn
            controller.set_speed_r(-speed * adjustment)
            controller.set_speed_l(speed * adjustment)
        else:  # Left turn
            controller.set_speed_r(speed * adjustment)
            controller.set_speed_l(-speed * adjustment)
        
        time.sleep(controller.sampling_time -
                  ((time.perf_counter() - current) % controller.sampling_time))
        last = current
    
    stop()
    time.sleep(1)

# Test the turn function
reset_distance()
turn(controller, 0.5, 90, 0.03)  # Try turning 90 degrees right with 0.5 speed