from robot_systems.robot import HamBot
import math
import time
import os
import sys
Chris_R = HamBot()
def main():
    # Initialize robot
    
    
    # Important variables
    targetDistanceFromWall = 500  # mm
    previousError = 0.0
    integral = 0.0
    
    # PID gains (for tuning)
    kp = 0.1
    ki = 0.01
    kd = 0.05
    
    # Definition of lidar "Target Areas"
    Lidar_l = [89, 90, 91]
    Lidar_r = [269, 270, 271]
    Lidar_f = [179, 180, 181]
    Lidar_b = [359, 0, 1]
    
    # Control loop timing
    prev_time = time.time()
    
    # Main control loop
    try:
        while True:
            # Get current time and calculate dt
            current_time = time.time()
            dt = current_time - prev_time
            prev_time = current_time
            
            # Get current distance from lidar
            currentDistance = getLidarImage(Lidar_f)
            
            # Call PID controller
            velocity, previousError, integral = pidAlgorithm(
                targetDistanceFromWall, 
                currentDistance, 
                previousError, 
                integral, 
                dt, 
                kp, ki, kd
            )
            
            # Apply velocity command to robot
            # Assuming positive velocity means moving forward
            if abs(velocity) < 0.05:# If velocity is very small, stop the robot
                print("Hurray!!!") 
                robotStop()
                temp_array = Chris_R.get_range_image()
                front_dist_curr = min(temp_array[lidar_angles[0]], temp_array[lidar_angles[1]], temp_array[lidar_angles[2]])
                print(front_dist_curr)
                break
            else:
                # Convert normalized velocity (-1 to 1) to robot speed commands
                # You might need to adjust this based on your robot's API
                Chris_R.set_left_motor_speed(velocity)
                Chris_R.set_right_motor_speed(velocity)
                # velocity, angular_velocity
            
            # Small delay to prevent CPU overuse
            time.sleep(0.05)
            
    except KeyboardInterrupt:
        # Stop robot when Ctrl+C is pressed
        robotStop()
        print("Program terminated by user")
        
        # Secret easter egg - uncomment this line to activate it when terminating with Ctrl+C
        # star_wars_crawl(22)

# Function to get lidar readings
def getLidarImage(lidar_angles):
    temp_array = Chris_R.get_range_image()
    front_dist_curr = min(temp_array[lidar_angles[0]], temp_array[lidar_angles[1]], temp_array[lidar_angles[2]])
    return front_dist_curr

# PID Algorithm function
def pidAlgorithm(targetDistanceFromWall, currentDistance, previousError, integral, dt, kp, ki, kd):
    # Calculates error
    error = targetDistanceFromWall - currentDistance
    
    # Proportional term
    p_term = kp * error
    
    # Integral term, gets error over time
    integral += error * dt
    i_term = ki * integral
    
    # Derivative term, rate of change of said error
    derivative = (error - previousError) / dt
    d_term = kd * derivative
    
    # Calculates PID output
    pid_output = p_term + i_term + d_term
    
    # Converts PID output to velocity command
    velocity_command = pid_output
    
    # Apply limits to velocityy
    max_velocity = 75
    min_velocity = -75
    velocity_command = -(max(min_velocity, min(velocity_command, max_velocity)))
    
    return velocity_command, error, integral

# Function to stop the robot
def robotStop():
    Chris_R.stop_motors()    # Set both linear and angular velocity to 0

# Star Wars crawl easter egg function
def star_wars_crawl(duration=22):
    """
    Display a Star Wars-like text crawl in the console for a specified duration
    
    Args:
        duration (int): Duration in seconds to run the crawl
    """
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Star Wars crawl text
    crawl_text = """
    EPISODE IV
    
    A NEW ROBOT
    
    It is a period of technical innovation.
    Rebel engineers, striking from a hidden
    lab, have built their first autonomous
    robotic system.
    
    During initialization, the engineering
    team managed to steal secret plans for
    the Empire's ultimate weapon, THE HAMBOT,
    a powerful machine with enough intelligence
    to navigate an entire obstacle course.
    
    Pursued by the professor's sinister teaching
    assistants, the team races against time to
    complete the initialization sequence and
    restore freedom to the robotics lab....
    """
    
    lines = crawl_text.split('\n')
    max_line_length = max(len(line) for line in lines)
    
    # Calculate delay between lines to fit the total duration
    # Let's reserve 2 seconds for the title sequence
    line_delay = (duration - 2) / len(lines)
    
    # Display the iconic "A long time ago..." text
    print("\n\n\n")
    print("       A long time ago in a robotics lab far, far away...")
    time.sleep(2)
    
    # Clear screen again
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Start time
    start_time = time.time()
    end_time = start_time + duration
    
    # Calculate how many blank lines we need at the start to push text off bottom of screen
    terminal_height = os.get_terminal_size().lines
    starting_blanks = terminal_height
    
    # The crawl effect
    current_display = [" " * max_line_length] * starting_blanks
    
    for i, line in enumerate(lines):
        # Center each line
        centered_line = line.center(max_line_length)
        
        # Update the display buffer
        current_display.pop(0)
        current_display.append(centered_line)
        
        # Clear and redraw
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n".join(current_display))
        
        # Check if we've reached our time limit
        if time.time() >= end_time:
            break
            
        # Delay before next line
        time.sleep(line_delay)
    
    # If we finish the text before the duration is up, wait the remainder
    remaining_time = end_time - time.time()
    if remaining_time > 0:
        time.sleep(remaining_time)
    
    # Clear the screen when done
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Robot initialization complete. May the Force be with you!")

# Run the main function if this script is executed
if __name__ == "__main__":

    star_wars_crawl(22)  # 22 seconds of crawl
    main()