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
    
    # Identify which of the specified colors it matches
    color_name = identify_color_range(r, g, b)
    
    return (r, g, b), color_name

def identify_color_range(r, g, b):
    """
    Returns the name of the color based on predefined ranges for each target color.
    
    Original Colors (variable lighting):
    Light Yellow - #98843b (RGB: 152, 132, 59)
    Green - #60961c (RGB: 96, 150, 28)
    Pink - #b72947 (RGB: 183, 41, 71)
    Blue - #3c2d30 (RGB: 60, 45, 48)
    
    Ideal Lighting Colors:
    Blue - #6e77a2 (RGB: 110, 119, 162)
    Yellow - #fbea74 (RGB: 251, 234, 116)
    Green - #7be720 (RGB: 123, 231, 32)
    Pink - #ff3e8e (RGB: 255, 62, 142)
    """
    # Define comprehensive color ranges that account for both sets of colors
    color_ranges = {
        "Yellow": {
            "r": (130, 255),  # Wide range to capture both light yellow variants
            "g": (110, 240),  # Wide range for G
            "b": (40, 130)    # Yellow has relatively low B, but wider for the brighter version
        },
        "Green": {
            "r": (70, 140),   # Range to capture both green variants
            "g": (130, 240),  # High G values (green is dominant)
            "b": (15, 60)     # Low B values for both variants
        },
        "Pink": {
            "r": (160, 255),  # High R values for both pink variants
            "g": (25, 90),    # Low to moderate G values
            "b": (50, 150)    # Range to capture both pink variants
        },
        "Blue": {
            "r": (40, 130),   # Range to capture both blue variants
            "g": (30, 140),   # Range to capture both blue variants
            "b": (35, 180)    # Higher for bright blue, lower for dark blue
        }
    }
    
    # If the color doesn't match any range, use closest match from the ideal lighting colors
    ideal_colors = {
        "Blue": (110, 119, 162),
        "Yellow": (251, 234, 116),
        "Green": (123, 231, 32),
        "Pink": (255, 62, 142)
    }
    
    # First check if the color falls within any of the defined ranges
    for color_name, ranges in color_ranges.items():
        if (ranges["r"][0] <= r <= ranges["r"][1] and
            ranges["g"][0] <= g <= ranges["g"][1] and
            ranges["b"][0] <= b <= ranges["b"][1]):
            return color_name
    
    # If no direct range match, find the closest ideal color
    min_distance = float('inf')
    closest_color = "Unknown"
    
    for color_name, (target_r, target_g, target_b) in ideal_colors.items():
        # Calculate Euclidean distance
        distance = np.sqrt((r - target_r)**2 + (g - target_g)**2 + (b - target_b)**2)
        
        # Update closest color if this distance is smaller
        if distance < min_distance:
            min_distance = distance
            closest_color = color_name
    
    # Only return the closest color if it's within a reasonable distance
    if min_distance > 150:  # This threshold can be adjusted
        return "Unknown"
    
    return closest_color

# Initialize the camera
print("Initializing camera...")
camera = Camera(fps=10)  # Higher FPS for more responsive readings

try:
    # Give the camera time to warm up
    time.sleep(2)
    
    print("Ready! Press Ctrl+C to exit.")
    print("Detecting colors: Yellow, Green, Pink, Blue")
    
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