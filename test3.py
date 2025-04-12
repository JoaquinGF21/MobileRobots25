from robot_systems.robot import HamBot
import time

def track_pink_landmark():
    # Initialize the robot
    robot = HamBot(lidar_enabled=False, camera_enabled=True)
    
    # Define pink color in RGB
    pink = (158, 0, 255)  # Hot pink
    
    # Set the color to detect with 10% tolerance
    robot.camera.set_landmark_colors(pink, tolerance=0.1)
    
    # Define the center of the camera view
    camera_center_x = 320  # Assuming 640x480 resolution, center is at 320
    
    # PID control variables
    targetPosition = camera_center_x
    previousError = 0.0
    integral = 0.0
    
    # PID gains (tune these values as needed)
    kp = 0.1  # Proportional gain
    ki = 0.01  # Integral gain
    kd = 0.05  # Derivative gain
    
    # Control timing
    prev_time = time.time()
    
    # Define centering threshold
    centering_threshold = 20  # Pixels from center considered "centered"
    
    try:
        print("Starting pink landmark tracking. Press Ctrl+C to stop.")
        while True:
            # Get current time and calculate dt
            current_time = time.time()
            dt = current_time - prev_time
            prev_time = current_time
            
            # Find landmarks in the current frame
            try:
                landmarks = robot.camera.find_landmarks()
            except Exception as e:
                print(f"Error detecting landmarks: {e}")
                landmarks = []
            
            if landmarks:
                # Take the first detected pink landmark
                landmark = landmarks[0]
                print(f"Found pink at ({landmark.x}, {landmark.y})")
                
                # Calculate how far the landmark is from the center
                currentPosition = landmark.x
                
                # Call PID controller for turning
                turn_speed, previousError, integral = pidAlgorithm(
                    targetPosition, 
                    currentPosition, 
                    previousError, 
                    integral, 
                    dt, 
                    kp, ki, kd
                )
                
                # Determine if we need to adjust
                if abs(targetPosition - currentPosition) <= centering_threshold:
                    # The landmark is centered - stop motors
                    print("Pink centered")
                    robot.stop_motors()
                else:
                    # Scale the PID output to motor speed range (-75 to 75)
                    max_turn_speed = 30  # Cap the maximum turn speed
                    
                    # Apply the turn speed (positive = turn right, negative = turn left)
                    left_speed = -turn_speed
                    right_speed = turn_speed
                    
                    print(f"Adjusting: turn_speed={turn_speed:.2f}, left={left_speed:.2f}, right={right_speed:.2f}")
                    robot.set_left_motor_speed(left_speed)
                    robot.set_right_motor_speed(right_speed)
            else:
                # No landmark detected - stop and wait
                print("No pink detected")
                robot.stop_motors()
                # Reset the integral term when no target is visible
                integral = 0.0
            
    except KeyboardInterrupt:
        print("Tracking stopped by user")
    finally:
        # Make sure to disconnect the robot properly
        robot.disconnect_robot()
        print("Robot disconnected")

# PID Algorithm function (adapted from your code)
def pidAlgorithm(targetPosition, currentPosition, previousError, integral, dt, kp, ki, kd):
    # Calculate error (positive error = target is to the right)
    error = targetPosition - currentPosition
    
    # Proportional term
    p_term = kp * error
    
    # Integral term with anti-windup (limit accumulation)
    integral += error * dt
    # Anti-windup: limit the integral term
    integral = max(-500, min(integral, 500))
    i_term = ki * integral
    
    # Derivative term
    if dt > 0:  # Avoid division by zero
        derivative = (error - previousError) / dt
    else:
        derivative = 0
    d_term = kd * derivative
    
    # Calculate PID output
    pid_output = p_term + i_term + d_term
    
    # Apply limits to turn speed
    max_turn = 40
    min_turn = -40
    turn_command = max(min_turn, min(pid_output, max_turn))
    
    return turn_command, error, integral

if __name__ == "__main__":
    track_pink_landmark()