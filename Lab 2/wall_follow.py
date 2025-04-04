from robot_systems.robot import HamBot
import math
import time
import os
import sys

Chris_R = HamBot()
#initialize directions and base speed
Lidar_l = [89,90,91]
Lidar_r = [269,270,271]
Lidar_f = [179,180,181]
Lidar_b = [359,0,1]
base_speed = 50
target = 300

kp = 0.05
ki = 0.001
kd = 0.2


set_dist = 300
#function to turn 90 degree when aproaching a wall
def corner(dir):
    if (dir == 'left'):
        Chris_R.run_left_motor_for_rotations(0.5,30,False)
        Chris_R.run_right_motor_for_rotations(0.5,-30,True)
    if (dir == 'right'):
        print()
    
    Chris_R.stop_motors()

        
#function returning the neccesary PID adjustment values 
def PID(target, current,prev_error,integral,dt):
    err = target - current
    
    #Proportional
    p_term = kp * err
    
    #integral
    integral += err * dt
    i_term = ki * integral
    #derivative
    derivative = (err -prev_error)/dt
    d_term = kd * derivative
    
    adj = p_term + i_term + d_term
    
    return adj, err, integral
    
    
    

def wall_follow(dir):
    #initialize current distance along with a temp array to hold the lidar readings
    front_dist_curr = 0
    side_dist_curr = 0
    adj = 0
    temp_array = []
    #initialize prevTime and variables used in the PID function
    prevTime = time.perf_counter()
    integral = 0
    prev_error = 0.0
    while(True):
        currentTime = time.perf_counter()
        #we decided to only adjust the angle by changing the left wheel for less variability
        Chris_R.set_left_motor_speed(max(-75,min(75,base_speed + adj)))
        Chris_R.set_right_motor_speed(base_speed)
        
        temp_array = Chris_R.get_range_image()
        front_dist_curr = max(0,min(temp_array[Lidar_f[0]],temp_array[Lidar_f[1]],temp_array[Lidar_f[2]]))
        
        
        if (dir == 'left'):
            side_dist_curr = max(0,min(temp_array[Lidar_l[0]],temp_array[Lidar_l[1]],temp_array[Lidar_l[2]]))
            
        if (dir == 'right'):
            side_dist_curr = max(0,min(temp_array[Lidar_r[0]],temp_array[Lidar_r[1]],temp_array[Lidar_r[2]]))
        #checks if robot has reached a corner. target +100 to give more room for the robot
        if front_dist_curr <= target + 100:
            Chris_R.stop_motors()
            corner(dir)
            
        #initialize dt and call the PID function
        dt = currentTime - prevTime
        adj, prev_error, integral = PID(target,side_dist_curr,prev_error,integral,dt)  
        prevTime = currentTime


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
       
def main():   
    star_wars_crawl(22)
    wall_follow("left")
main()
            
        
    
