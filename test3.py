from robot_systems.robot import HamBot
from robot_systems.camera import Camera
import time

# Initialize the camera
camera = Camera()

# Standard pink color in RGB (Red, Green, Blue)
pink = (255, 105, 180)  # Hot pink

# Set the color to detect with 10% tolerance
camera.set_landmark_colors(pink, tolerance=0.1)

try:
    print("Starting pink detection. Press Ctrl+C to stop.")
    while True:
        # Find landmarks in the current frame
        landmarks = camera.find_landmarks(area_threshold=500)
        
        # Print when pink is detected
        if landmarks:
            print(f"Found {len(landmarks)} pink object(s)!")
        
        # Short delay to prevent CPU overuse
        time.sleep(0.2)
        
except KeyboardInterrupt:
    print("Detection stopped by user")
finally:
    # Make sure to stop the camera when done
    camera.stop_camera()
    print("Camera stopped")