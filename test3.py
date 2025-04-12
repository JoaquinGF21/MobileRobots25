from robot_systems.robot import HamBot
import numpy as np
import time
<<<<<<< HEAD
import sys
import os

# Try to release camera resources
os.system("sudo killall -9 libcamera_vid libcamera_still 2>/dev/null")

# Initialize robot with camera enabled
robot = HamBot(camera_enabled=True)

# Define color values and tolerances
# Each value is an exact RGB value with a tolerance of +/-10
color_values = {
    "Green": {
        "r": 116, 
        "g": 231, 
        "b": 88,
        "tolerance": 10
    },
    "Pink": {
        "r": 165,
        "g": 0,
        "b": 249,
        "tolerance": 10
    },
    "Blue": {
        "r": 119,
        "g": 72,
        "b": 90,
        "tolerance": 10
    },
    "Yellow": {
        "r": 165,
        "g": 208,
        "b": 212,
        "tolerance": 10
    }
}

# Generate ranges from the values and tolerances
color_ranges = {}
for color_name, values in color_values.items():
    tolerance = values["tolerance"]
    color_ranges[color_name] = {
        "r": (max(0, values["r"] - tolerance), min(255, values["r"] + tolerance)),
        "g": (max(0, values["g"] - tolerance), min(255, values["g"] + tolerance)),
        "b": (max(0, values["b"] - tolerance), min(255, values["b"] + tolerance))
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
    """Identify color based on precise RGB values with tolerance"""
    # Calculate distance to each target color
    color_distances = {}
    
    for color_name, values in color_values.items():
        # Calculate Euclidean distance in RGB space
        distance = np.sqrt(
            (r - values["r"])**2 + 
            (g - values["g"])**2 + 
            (b - values["b"])**2
        )
        color_distances[color_name] = distance
        
    # Check if any color is within acceptable range
    # We'll use a slightly more generous threshold for detection (sqrt(3) * tolerance)
    # This is because Euclidean distance in 3D space can be larger than individual tolerances
    best_color = min(color_distances.items(), key=lambda x: x[1])
    max_allowed_distance = best_color[1] * 1.732  # sqrt(3)
    
    # Direct range check as fallback
    for color_name, ranges in color_ranges.items():
        if (ranges["r"][0] <= r <= ranges["r"][1] and
            ranges["g"][0] <= g <= ranges["g"][1] and
            ranges["b"][0] <= b <= ranges["b"][1]):
            return color_name
    
    # If we're still here, check if best match is within a reasonable distance
    if best_color[1] < 25:  # Allow a bit more flexibility for detection
        return best_color[0]
    
    return "Unknown"

def detect_color():
    """Detect color using the robot's camera with multiple sampling zones"""
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
        
        # Sample multiple regions instead of just center
        # This improves detection when color object isn't perfectly centered
        sample_regions = [
            # Center (larger)
            (width//2 - 40, height//2 - 40, 80, 80),
            # Left of center
            (width//2 - 70, height//2, 40, 40),
            # Right of center
            (width//2 + 30, height//2, 40, 40),
            # Above center
            (width//2, height//2 - 70, 40, 40),
            # Below center
            (width//2, height//2 + 30, 40, 40)
        ]
        
        # Track color detections from each region
        color_votes = {}
        
        # Debug information for color detection
        color_debug = {}
        for color in color_values.keys():
            color_debug[color] = []
        
        for i, (x, y, w, h) in enumerate(sample_regions):
            # Ensure boundaries
            x_start = max(0, x)
            y_start = max(0, y)
            x_end = min(width, x + w)
            y_end = min(height, y + h)
            
            # Skip if region is too small
            if x_end - x_start < 10 or y_end - y_start < 10:
                continue
                
            # Extract region
            region = image[y_start:y_end, x_start:x_end]
            
            # Calculate average color
            avg_color = np.mean(region, axis=(0, 1)).astype(int)
            r, g, b = avg_color
            
            # Identify color
            color_name = identify_color(r, g, b)
            
            # Add to vote tally
            if color_name not in color_votes:
                color_votes[color_name] = 0
            color_votes[color_name] += 1
            
            # Print debug info
            print(f"Region {i}: RGB({r},{g},{b}) -> {color_name}")
            
            # Calculate distances to each target color for debugging
            for color, values in color_values.items():
                distance = np.sqrt(
                    (r - values["r"])**2 + 
                    (g - values["g"])**2 + 
                    (b - values["b"])**2
                )
                if distance < 30:  # Only log close matches
                    color_debug[color].append(f"Region {i}: Distance to {color}={distance:.1f} with RGB({r},{g},{b})")
        
        # Determine winner by votes (exclude Unknown)
        if "Unknown" in color_votes:
            del color_votes["Unknown"]
            
        if not color_votes:
            return "Unknown"
            
        # Find color with most votes
        winner = max(color_votes.items(), key=lambda x: x[1])
        print(f"Color detection result: {winner[0]} with {winner[1]} votes")
        
        # Print extra debug info for color detection
        for color, debug_lines in color_debug.items():
            if debug_lines:
                print(f"{color} detection details:")
                for debug_line in debug_lines:
                    print(f"  {debug_line}")
        
        return winner[0]
        
    except Exception as e:
        print(f"Error detecting color: {e}")
        return "Unknown"

def slower_turn_with_pauses():
    """Turn robot 360 degrees slowly with pauses to improve detection"""
    print(f"Performing slow 360° search for {target_color}...")
    
    # Parameters for rotation
    rotation_speed = 10  # Slower rotation
    segment_time = 0.7   # Time to rotate a bit
    pause_time = 0.5     # Time to pause and check for color
    
    # We'll do 20 segments to complete 360 degrees
    segments = 20
    found_color = False
    
    for segment in range(segments):
        if found_color:
            break
            
        # Rotate a bit
        robot.set_left_motor_speed(-rotation_speed)
        robot.set_right_motor_speed(rotation_speed)
        time.sleep(segment_time)
        
        # Stop and check for color
        robot.stop_motors()
        time.sleep(pause_time)  # Pause to let camera stabilize
        
        # Check multiple times for more reliable detection
        detections = []
        for _ in range(3):
            color_name = detect_color()
            detections.append(color_name)
            time.sleep(0.1)
        
        # If target color appears in majority of detections
        if detections.count(target_color) >= 2:
            found_color = True
            print(f"Found {target_color}!")
    
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
    
    # Count consecutive frames where color is lost
    lost_color_count = 0
    max_lost_frames = 5  # More tolerant of momentary losses
    
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
        max_velocity = 50  # Lower max speed for more stability
        min_velocity = -50
        velocity = max(min_velocity, min(velocity, max_velocity))
        
        # Drive robot
        robot.set_left_motor_speed(velocity)
        robot.set_right_motor_speed(velocity)
        
        # Update previous error
        previous_error = error
        
        # Check if still seeing target color
        color_name = detect_color()
        if color_name != target_color:
            lost_color_count += 1
            print(f"Lost sight of {target_color} ({lost_color_count}/{max_lost_frames})")
            
            # Only stop if we've lost the color for multiple consecutive frames
            if lost_color_count >= max_lost_frames:
                robot.stop_motors()
                return False
        else:
            # Reset counter when we see the color again
            lost_color_count = 0
        
        time.sleep(0.05)

def find_and_approach_color(color):
    """Main function to find and approach color"""
    global target_color
    target_color = color
    
    print(f"Looking for {target_color} object...")
    
    # Take multiple readings for initial detection
    color_detections = []
    for _ in range(5):
        color_detections.append(detect_color())
        time.sleep(0.1)
    
    # Check if target color appears in majority of detections
    if color_detections.count(target_color) >= 3:
        print(f"Found {target_color} directly ahead!")
        if approach_object(500):  # 50cm
            print(f"Successfully approached {target_color}!")
            return True
    
    # Do 360° search if not found initially
    print(f"Cannot see {target_color}. Performing 360° search...")
    if slower_turn_with_pauses():
        print(f"Found {target_color} during rotation!")
        # Double-check detection after stopping
        time.sleep(0.5)  # Wait for camera to stabilize
        
        color_check = []
        for _ in range(3):
            color_check.append(detect_color())
            time.sleep(0.1)
            
        if color_check.count(target_color) >= 2:
            if approach_object(500):
                print(f"Successfully approached {target_color}!")
                return True
        else:
            print(f"False detection - color disappeared after stopping")
    
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
    print("Warming up camera (3 seconds)...")
    time.sleep(3)
    
    # Display color calibration info
    print("\nCalibrating color detection. Please show each color to the camera:")
    print("Sampling color ranges...")
    for _ in range(5):
        detect_color()
        time.sleep(0.5)
    
    print("\nColor detection configured with the following RGB values and tolerances:")
    for color, values in color_values.items():
        print(f"{color}: RGB({values['r']}, {values['g']}, {values['b']}) ±{values['tolerance']}")
    
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