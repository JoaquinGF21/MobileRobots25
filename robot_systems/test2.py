from robot_systems.robot import HamBot
import numpy as np
import time
import sys
import os

# Try to release camera resources
os.system("sudo killall -9 libcamera_vid libcamera_still 2>/dev/null")

# Initialize robot with camera enabled
robot = HamBot(camera_enabled=True)

# Define color ranges for detection
color_ranges = {
    "Yellow": {
        "r": (130, 255),
        "g": (110, 240),
        "b": (40, 130)
    },
    "Green": {
        "r": (50, 140),
        "g": (150, 255),
        "b": (15, 60)
    },
    "Pink": {
        "r": (160, 255),
        "g": (25, 90),
        "b": (50, 150)
    },
    "Blue": {
        "r": (40, 130),
        "g": (30, 140),
        "b": (120, 210)
    }
}

# Definition of lidar "Target Areas"
Lidar_l = [89, 90, 91]
Lidar_r = [269, 270, 271]
Lidar_f = [179, 180, 181]
Lidar_b = [359, 0, 1]

# PID constants for approach control
kp = 0.1
ki = 0.01
kd = 0.05

def identify_color(r, g, b):
    """Identify color based on RGB values"""
    # Check for Green-Blue differentiation
    if g > b * 2 and g > 120:
        if 50 <= r <= 140 and g >= 120:
            return "Green"
    
    if b > g and b > 100:
        if 40 <= r <= 130 and 30 <= g <= 140:
            return "Blue"
    
    # Check color ranges
    for color_name, ranges in color_ranges.items():
        if (ranges["r"][0] <= r <= ranges["r"][1] and
            ranges["g"][0] <= g <= ranges["g"][1] and
            ranges["b"][0] <= b <= ranges["b"][1]):
            return color_name
    
    return "Unknown"

def detect_color():
    """Detect color using the robot's camera"""
    if robot.camera is None:
        print("Camera not available")
        return "Unknown"
    
    try:
        # Get image from camera
        image = robot.camera.get_image()
        if image is None:
            return "Unknown"
        
        # Get image dimensions
        height, width = image.shape[:2]
        
        # Sample center area
        sample_size = 50
        x_start = width // 2 - sample_size // 2
        y_start = height // 2 - sample_size // 2
        x_end = x_start + sample_size
        y_end = y_start + sample_size
        
        # Ensure boundaries
        x_start = max(0, x_start)
        y_start = max(0, y_start)
        x_end = min(width, x_end)
        y_end = min(height, y_end)
        
        # Extract center region
        center_region = image[y_start:y_end, x_start:x_end]
        
        # Calculate average color
        avg_color = np.mean(center_region, axis=(0, 1)).astype(int)
        r, g, b = avg_color  # The camera might return RGB directly
        
        # Identify color
        color_name = identify_color(r, g, b)
        print(f"Detected color: {color_name}, RGB: ({r}, {g}, {b})")
        
        return color_name
        
    except Exception as e:
        print(f"Error detecting color: {e}")
        return "Unknown"

def turn_complete_circle():
    """Turn robot 360 degrees while looking for target color"""
    print(f"Performing 360° search for {target_color}...")
    
    # Parameters for rotation
    rotation_speed = 20
    rotation_time = 10  # seconds for 360 degrees
    
    start_time = time.time()
    found_color = False
    
    # Start turning
    robot.set_left_motor_speed(-rotation_speed)
    robot.set_right_motor_speed(rotation_speed)
    
    # Keep turning until complete or color found
    while time.time() - start_time < rotation_time and not found_color:
        color_name = detect_color()
        
        if color_name == target_color:
            found_color = True
            print(f"Found {target_color}!")
        
        time.sleep(0.1)
    
    # Stop robot
    robot.stop_motors()
    return found_color

def approach_object(target_distance=500):
    """Approach detected object using PID control"""
    print(f"Approaching {target_color} object...")
    
    # PID variables
    integral = 0.0
    previous_error = 0.0
    prev_time = time.time()
    
    # Approach loop
    while True:
        # Get current time
        current_time = time.time()
        dt = current_time - prev_time
        prev_time = current_time
        
        # Get distance from lidar
        temp_array = robot.get_range_image()
        if isinstance(temp_array, list):
            current_distance = min(temp_array[Lidar_f[0]], temp_array[Lidar_f[1]], temp_array[Lidar_f[2]])
        else:
            print("Cannot get lidar readings")
            robot.stop_motors()
            return False
        
        print(f"Distance to object: {current_distance}mm")
        
        # Calculate error
        error = current_distance - target_distance
        
        # Check if at target distance
        if abs(error) < 50:  # 5cm tolerance
            robot.stop_motors()
            print(f"Target reached at {current_distance}mm!")
            return True
        
        # Calculate PID terms
        p_term = kp * error
        integral += error * dt
        i_term = ki * integral
        derivative = (error - previous_error) / dt if dt > 0 else 0
        d_term = kd * derivative
        
        # Calculate velocity
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
        
        # Check if still seeing target color
        color_name = detect_color()
        if color_name != target_color:
            print(f"Lost sight of {target_color}")
            robot.stop_motors()
            return False
        
        time.sleep(0.05)

def find_and_approach_color(color):
    """Main function to find and approach color"""
    global target_color
    target_color = color
    
    print(f"Looking for {target_color} object...")
    
    # Check if can see color directly
    detected_color = detect_color()
    
    if detected_color == target_color:
        print(f"Found {target_color} directly ahead!")
        if approach_object(500):  # 50cm
            print(f"Successfully approached {target_color}!")
            return True
    
    # Do 360° search if not found initially
    print(f"Cannot see {target_color}. Performing 360° search...")
    if turn_complete_circle():
        print(f"Found {target_color} during rotation!")
        if approach_object(500):
            print(f"Successfully approached {target_color}!")
            return True
    
    # If still not found
    print(f"Could not find {target_color} after complete rotation.")
    print("Work in progress: Add more search patterns here.")
    return False

def main():
    print("Color Finding Robot")
    print("-------------------")
    
    # Make sure camera is available
    if robot.camera is None:
        print("ERROR: Camera not available. Check connections and try again.")
        robot.disconnect_robot()
        sys.exit(1)
    
    # Give camera time to initialize
    print("Warming up camera (2 seconds)...")
    time.sleep(2)
    
    # Prompt for color selection
    valid_colors = ["Blue", "Yellow", "Pink", "Green"]
    
    while True:
        print("\nSelect a color to find:")
        for i, color in enumerate(valid_colors, 1):
            print(f"{i}. {color}")
        
        try:
            choice = int(input("Enter choice (1-4): "))
            if 1 <= choice <= 4:
                selected_color = valid_colors[choice-1]
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    try:
        # Find and approach color
        result = find_and_approach_color(selected_color)
        
        if result:
            print(f"Mission accomplished! Found and approached {selected_color} object.")
        else:
            print(f"Mission not completed. Could not find or approach {selected_color} object.")
    
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    
    finally:
        # Clean up
        print("Shutting down robot...")
        robot.disconnect_robot()

if __name__ == "__main__":
    main()