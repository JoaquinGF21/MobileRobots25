from robot_systems.robot import HamBot
import time

def track_pink_landmark():
    # Initialize the robot
    robot = HamBot(lidar_enabled=False, camera_enabled=True)
    
    # Define pink color in RGB (Red, Green, Blue)
    pink = (255, 105, 180)  # Hot pink
    
    # Set the color to detect with 10% tolerance
    robot.camera.set_landmark_colors(pink, tolerance=0.1)
    
    # Define the center of the camera view
    camera_center_x = robot.camera.width // 2
    
    # Define centering parameters
    centering_threshold = 50  # Pixels from center considered "centered"
    rotation_speed = 15  # Base rotation speed (adjust as needed)
    
    try:
        print("Starting pink landmark tracking. Press Ctrl+C to stop.")
        while True:
            # Find landmarks in the current frame
            landmarks = robot.camera.find_landmarks(area_threshold=500)
            
            if landmarks:
                # Take the first detected pink landmark
                landmark = landmarks[0]
                print(f"Found pink at ({landmark.x}, {landmark.y})")
                
                # Calculate how far the landmark is from the center
                offset = landmark.x - camera_center_x
                
                # Determine if we need to adjust
                if abs(offset) <= centering_threshold:
                    # The landmark is centered - stop motors
                    print("Pink centered")
                    robot.stop_motors()
                else:
                    # Calculate rotation speed based on how far off-center the landmark is
                    # The further off-center, the faster we rotate (capped at max speed)
                    # Use sigmoid-like scaling to make movement smoother
                    speed_factor = min(1.0, abs(offset) / (camera_center_x * 0.8))
                    turn_speed = int(rotation_speed + (speed_factor * 20))
                    
                    if offset > 0:
                        # Landmark is to the right - turn right
                        print(f"Turning right, offset: {offset}, speed: {turn_speed}")
                        robot.set_left_motor_speed(turn_speed)
                        robot.set_right_motor_speed(-turn_speed)
                    else:
                        # Landmark is to the left - turn left
                        print(f"Turning left, offset: {offset}, speed: {turn_speed}")
                        robot.set_left_motor_speed(-turn_speed)
                        robot.set_right_motor_speed(turn_speed)
            else:
                # No landmark detected - stop and wait
                print("No pink detected")
                robot.stop_motors()
            
            # Short delay to prevent CPU overuse
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("Tracking stopped by user")
    finally:
        # Make sure to disconnect the robot properly
        robot.disconnect_robot()
        print("Robot disconnected")

if __name__ == "__main__":
    track_pink_landmark()