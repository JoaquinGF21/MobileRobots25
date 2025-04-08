from robot_systems.robot import HamBot
import numpy as np
import time
import sys
import os

# Try to release camera resources
os.system("sudo killall -9 libcamera_vid libcamera_still 2>/dev/null")

# Initialize robot with camera enabled
robot = HamBot(camera_enabled=True)

# Define color ranges for detection - MUCH wider ranges to improve detection
color_ranges = {
    "Yellow": {
        "r": (100, 255),  # Wider range
        "g": (100, 255),  # Wider range
        "b": (0, 150)     # Wider range, yellow has low blue
    },
    "Green": {
        "r": (0, 150),    # Wider range
        "g": (100, 255),  # Wider range, must have strong green
        "b": (0, 150)     # Wider range
    },
    "Pink": {
        "r": (150, 255),     # Strong red component, includes 185
        "g": (0, 100),       # Very low green (adjusted for RGB 185,0,255)
        "b": (180, 255)      # Very high blue (adjusted for RGB 185,0,255)
    },
    "Blue": {
        "r": (0, 150),    # Low red
        "g": (0, 150),    # Low to moderate green
        "b": (100, 255)   # Must have strong blue
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
    """Identify color based on RGB values using relative channel strengths"""
    # Check relative strengths of color channels - this is often more reliable than absolute values
    
    # Check specifically for the new pink color (185, 0, 255)
    # Allow some tolerance around these values
    pink_r_diff = abs(r - 185)
    pink_b_diff = abs(b - 255)
    if pink_r_diff < 50 and g < 50 and b > 200:
        return "Pink"
    
    # Simple color ratio checks for other colors
    if r > g and r > b and g > b*0.8:  # High red, medium-high green, low blue
        return "Yellow"
    
    if g > r*1.2 and g > b*1.2:  # Green significantly stronger than others
        return "Green"
    
    if r > g*1.5 and b > g*1.5 and b > 180:  # High red, low green, high blue (another pink check)
        return "Pink"
    
    if b > r and b > g:  # Blue is strongest channel
        return "Blue"
    
    # Fallback to range checks
    for color_name, ranges in color_ranges.items():
        if (ranges["r"][0] <= r <= ranges["r"][1] and
            ranges["g"][0] <= g <= ranges["g"][1] and
            ranges["b"][0] <= b <= ranges["b"][1]):
            return color_name
    
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
        
        # Debug information for pink detection
        pink_debug = []
        
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
            
            # Extra debug for pink detection
            if r > 150 and g < 100 and b > 180:
                pink_debug.append(f"Region {i}: Potential pink with RGB({r},{g},{b})")
        
        # Determine winner by votes (exclude Unknown)
        if "Unknown" in color_votes:
            del color_votes["Unknown"]
            
        if not color_votes:
            return "Unknown"
            
        # Find color with most votes
        winner = max(color_votes.items(), key=lambda x: x[1])
        print(f"Color detection result: {winner[0]} with {winner[1]} votes")
        
        # Print extra debug info for pink detection
        if pink_debug:
            print("Pink detection details:")
            for debug_line in pink_debug:
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
    
    print("\nSpecial detection enabled for Pink RGB(185, 0, 255)")
    
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