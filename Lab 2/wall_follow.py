from camera import Camera
from robot_systems.robot import HamBot
import numpy as np
import time
import math

# Initialize robot and camera
robot = HamBot()
camera = Camera(fps=10)  # Higher FPS for more responsive readings

# Definition of lidar "Target Areas" - reused from your wall follow code
Lidar_l = [89, 90, 91]
Lidar_r = [269, 270, 271]
Lidar_f = [179, 180, 181]
Lidar_b = [359, 0, 1]

# PID constants for approach control
kp = 0.1
ki = 0.01
kd = 0.05

def get_dominant_color(camera, sample_size=50):
    """
    Get the dominant color that the robot is facing.
    
    Args:
        camera: Camera instance
        sample_size: Size of the center square to sample (default: 50px)
    
    Returns:
        tuple: (R, G, B) color values
        str: Color name from the specified set of colors
    """
    # Get the current image
    image = camera.get_image()
    if image is None:
        return None, "No image captured"
    
    # Get dimensions
    height, width = image.shape[:2]
    
    # Calculate the center region to sample
    x_start = width // 2 - sample_size // 2
    y_start = height // 2 - sample_size // 2
    x_end = x_start + sample_size
    y_end = y_start + sample_size
    
    # Ensure boundaries are within image
    x_start = max(0, x_start)
    y_start = max(0, y_start)
    x_end = min(width, x_end)
    y_end = min(height, y_end)
    
    # Extract the center region
    center_region = image[y_start:y_end, x_start:x_end]
    
    # Calculate the average color in this region
    avg_color = np.mean(center_region, axis=(0, 1)).astype(int)
    
    # The camera likely gives BGR format, so we may need to reverse for RGB
    b, g, r = avg_color  # Adjust this line if your camera returns RGB directly
    
    # Identify which of the specified colors it matches
    color_name = identify_color_range(r, g, b)
    
    return (r, g, b), color_name

def identify_color_range(r, g, b):
    """
    Returns the name of the color based on predefined ranges for each target color.
    """
    # Define comprehensive color ranges that account for both sets of colors
    color_ranges = {
        "Yellow": {
            "r": (130, 255),  # Wide range to capture both light yellow variants
            "g": (110, 240),  # Wide range for G
            "b": (40, 130)    # Yellow has relatively low B, but wider for the brighter version
        },
        "Green": {
            "r": (50, 140),    # Range to capture both green variants
            "g": (150, 255),   # Higher minimum G value to better distinguish from blue
            "b": (15, 60)      # Low B values for green
        },
        "Pink": {
            "r": (160, 255),  # High R values for both pink variants
            "g": (25, 90),    # Low to moderate G values
            "b": (50, 150)    # Range to capture both pink variants
        },
        "Blue": {
            "r": (40, 130),   # Range to capture both blue variants
            "g": (30, 140),   # Lower maximum G value to distinguish from green
            "b": (120, 210)   # Higher minimum B value to distinguish from green
        }
    }
    
    # Check for Green-Blue differentiation specifically
    # Green has high G-to-B ratio
    if g > b * 2 and g > 120:
        # Check if it's in the general green range
        if 50 <= r <= 140 and g >= 120:
            return "Green"
    
    # Blue has higher B than G usually
    if b > g and b > 100:
        # Check if it's in the general blue range
        if 40 <= r <= 130 and 30 <= g <= 140:
            return "Blue"
    
    # First check if the color falls within any of the defined ranges
    for color_name, ranges in color_ranges.items():
        if (ranges["r"][0] <= r <= ranges["r"][1] and
            ranges["g"][0] <= g <= ranges["g"][1] and
            ranges["b"][0] <= b <= ranges["b"][1]):
            return color_name
    
    return "Unknown"

def approach_object(target_distance=500):
    """
    Use PID control to approach the detected colored object
    """
    # PID control variables
    integral = 0.0
    previous_error = 0.0
    prev_time = time.time()
    
    # Main approach loop
    while True:
        # Get current time for PID
        current_time = time.time()
        dt = current_time - prev_time
        prev_time = current_time
        
        # Get current distance from lidar (front-facing)
        temp_array = robot.get_range_image()
        current_distance = min(temp_array[Lidar_f[0]], temp_array[Lidar_f[1]], temp_array[Lidar_f[2]])
        
        # Calculate error
        error = current_distance - target_distance
        
        # If we're already at the target distance (within tolerance), stop
        if abs(error) < 50:  # 5cm tolerance
            robot.stop_motors()
            print(f"Target reached! Current distance: {current_distance}mm")
            return True
        
        # Proportional term
        p_term = kp * error
        
        # Integral term
        integral += error * dt
        i_term = ki * integral
        
        # Derivative term
        derivative = (error - previous_error) / dt if dt > 0 else 0
        d_term = kd * derivative
        
        # Calculate velocity command
        velocity = p_term + i_term + d_term
        
        # Limit velocity
        max_velocity = 75
        min_velocity = -75
        velocity = max(min_velocity, min(velocity, max_velocity))
        
        # Drive robot
        robot.set_left_motor_speed(velocity)
        robot.set_right_motor_speed(velocity)
        
        # Update previous error
        previous_error = error
        
        # Check if we still see the target color
        _, color_name = get_dominant_color(camera)
        if color_name == "Unknown" or color_name != target_color:
            robot.stop_motors()
            print("Lost sight of target color!")
            return False
        
        # Small delay to prevent CPU overuse
        time.sleep(0.05)

def turn_complete_circle():
    """
    Turn the robot in a complete 360-degree circle while looking for the target color
    """
    # Parameters for rotation
    rotation_speed = 20  # Slow enough to detect colors
    
    # Calculate time needed for a full rotation based on the robot's turning characteristics
    # This will need calibration for your specific robot
    rotation_time = 10  # seconds for a full 360-degree turn (adjust as needed)
    
    start_time = time.time()
    found_color = False
    
    # Start turning
    robot.set_left_motor_speed(-rotation_speed)
    robot.set_right_motor_speed(rotation_speed)
    
    # Keep turning until we complete the circle or find the color
    while time.time() - start_time < rotation_time and not found_color:
        # Check for target color
        _, color_name = get_dominant_color(camera)
        
        if color_name == target_color:
            found_color = True
            print(f"Found target color: {target_color}!")
        
        time.sleep(0.1)  # Small delay
    
    # Stop the robot
    robot.stop_motors()
    return found_color

def find_and_approach_color(color):
    """
    Main function to find and approach a specific colored object
    """
    global target_color
    target_color = color
    
    print(f"Looking for {target_color} object...")
    
    # First, check if we can immediately see the target color
    _, detected_color = get_dominant_color(camera)
    
    if detected_color == target_color:
        print(f"Found {target_color} directly in front! Approaching...")
        if approach_object(500):  # 50cm = 500mm
            print(f"Successfully approached {target_color} object!")
            return True
    
    # If not found initially, do a 360° search
    print(f"Cannot see {target_color}. Performing 360° search...")
    if turn_complete_circle():
        # If found during rotation, approach it
        print(f"Found {target_color} during rotation. Approaching...")
        if approach_object(500):  # 50cm = 500mm
            print(f"Successfully approached {target_color} object!")
            return True
        else:
            print(f"Lost sight of {target_color} while approaching.")
            return False
    
    # If still not found after 360° rotation
    print(f"Could not find {target_color} after complete rotation.")
    print("Work in progress: Add more search patterns here.")
    return False

def main():
    # Give the camera time to initialize
    print("Initializing camera...")
    time.sleep(2)
    
    # Prompt user to select a color
    valid_colors = ["Blue", "Yellow", "Pink", "Green"]
    
    while True:
        print("\nSelect a color to find:")
        for i, color in enumerate(valid_colors, 1):
            print(f"{i}. {color}")
        
        try:
            choice = int(input("Enter choice (1-4): "))
            if 1 <= choice <= 4:
                target_color = valid_colors[choice-1]
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    try:
        # Find and approach the selected color
        result = find_and_approach_color(target_color)
        
        if result:
            print(f"Mission accomplished! Found and approached {target_color} object.")
        else:
            print(f"Mission not completed. Could not find or approach {target_color} object.")
            
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        
    finally:
        # Clean up
        camera.stop_camera()
        robot.stop_motors()

# Start the program
main()