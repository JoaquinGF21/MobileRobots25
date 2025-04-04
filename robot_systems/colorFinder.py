from camera import Camera
import numpy as np
import time

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
    
    # Identify which of the specified colors it most closely matches
    color_name = identify_specific_color(r, g, b)
    
    return (r, g, b), color_name

def identify_specific_color(r, g, b):
    """
    Returns the name of the closest matching color from our specified set.
    
    Colors:
    Light Yellow - #98843b (RGB: 152, 132, 59)
    Green - #60961c (RGB: 96, 150, 28)
    Pink - #b72947 (RGB: 183, 41, 71)
    Blue - #3c2d30 (RGB: 60, 45, 48)
    """
    # Define our target colors (RGB format)
    target_colors = {
        "Light Yellow": (152, 132, 59),
        "Green": (96, 150, 28),
        "Pink": (183, 41, 71),
        "Blue": (60, 45, 48)
    }
    
    # Calculate color distance to each target using Euclidean distance
    min_distance = float('inf')
    closest_color = "Unknown"
    
    for color_name, (target_r, target_g, target_b) in target_colors.items():
        # Calculate Euclidean distance
        distance = np.sqrt((r - target_r)**2 + (g - target_g)**2 + (b - target_b)**2)
        
        # Update closest color if this distance is smaller
        if distance < min_distance:
            min_distance = distance
            closest_color = color_name
    
    # If the closest color is still too far away, return "Unknown"
    # You can adjust this threshold as needed
    if min_distance > 100:
        return "Unknown"
    
    return closest_color

def main():
    # Initialize the camera
    print("Initializing camera...")
    camera = Camera(fps=10)  # Higher FPS for more responsive readings
    
    try:
        # Give the camera time to warm up
        time.sleep(2)
        
        print("Ready! Press Ctrl+C to exit.")
        print("Detecting colors: Light Yellow, Green, Pink, Blue")
        
        # Continuously detect and display the color
        while True:
            rgb_color, color_name = get_dominant_color(camera)
            if rgb_color is not None:
                print(f"Detected color: {color_name} - RGB: {rgb_color}")
            time.sleep(0.5)  # Update twice per second
            
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        # Clean up
        camera.stop_camera()

if __name__ == "__main__":
    main()