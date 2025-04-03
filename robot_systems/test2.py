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
        str: Color name approximation
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
    r, g, b = avg_color
    
    # Simple color name approximation
    color_name = identify_color(r, g, b)
    
    return (r, g, b), color_name

def identify_color(r, g, b):
    """
    Returns an approximate color name based on RGB values.
    This is a simple implementation and can be expanded.
    """
    # Check if it's mostly a shade of gray
    if abs(r - g) < 20 and abs(r - b) < 20 and abs(g - b) < 20:
        if r < 50:
            return "Black"
        elif r > 200:
            return "White"
        else:
            return "Gray"
    
    # Find the dominant color channel
    max_channel = max(r, g, b)
    
    if r == max_channel and r > g + 50 and r > b + 50:
        return "Red"
    elif g == max_channel and g > r + 50 and g > b + 50:
        return "Green"
    elif b == max_channel and b > r + 50 and b > g + 50:
        return "Blue"
    elif r > 200 and g > 200 and b < 100:
        return "Yellow"
    elif r > 200 and g < 100 and b > 200:
        return "Purple"
    elif r < 100 and g > 150 and b > 150:
        return "Cyan"
    elif r > 200 and g > 100 and b < 100:
        return "Orange"
    else:
        return "Unknown"

def main():
    # Initialize the camera
    print("Initializing camera...")
    camera = Camera(fps=10)  # Higher FPS for more responsive readings
    
    try:
        # Give the camera time to warm up
        time.sleep(2)
        
        print("Ready! Press Ctrl+C to exit.")
        
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