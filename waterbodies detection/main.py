import requests
import cv2
import numpy as np
import os

def download_satellite_image(api_key, center, zoom, size, map_type, output_path):
    """
    Download a satellite image from Google Maps Static API.
    """
    base_url = "https://maps.googleapis.com/maps/api/staticmap"
    params = {
        "center": center,
        "zoom": zoom,
        "size": size,
        "maptype": map_type,
        "key": api_key,
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"Map image saved to {output_path}")
    else:
        print(f"Failed to download map image: {response.status_code} - {response.text}")
        raise ValueError("Failed to download map image. Check your API key and parameters.")

def count_water_bodies(image_path, lower_color, upper_color, min_area=500, output_image_path="output_with_water_bodies.jpg"):
    """
    Count the number of water bodies in an image based on color detection.
    """
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Image not found at path: {image_path}")
    
    # Convert to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Threshold the image to extract water bodies
    mask = cv2.inRange(hsv_image, np.array(lower_color), np.array(upper_color))
    
    # Find contours of the masked regions
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter contours by area to ignore noise
    water_bodies = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]
    
    # Draw contours on the original image (optional for visualization)
    output_image = image.copy()
    cv2.drawContours(output_image, water_bodies, -1, (0, 255, 0), 2)
    
    # Save the output image for visualization
    cv2.imwrite(output_image_path, output_image)
    print(f"Output image with water bodies saved to {output_image_path}")
    
    # Return the count of water bodies
    return len(water_bodies)

# Configuration
API_KEY = "AIzaSyCsbREqMxMHclfarDaTe9bwYjKNxB1UKDg"  # Securely load the API key
CENTER = "23.0225,72.5714"                  
ZOOM = 7                                   
SIZE = "640x640"                           
MAP_TYPE = "satellite"                     
MAP_IMAGE_PATH = "gujarat_satellite.jpg"

# Download satellite image of Gujarat
download_satellite_image(API_KEY, CENTER, ZOOM, SIZE, MAP_TYPE, MAP_IMAGE_PATH)

# Define color range for water bodies in HSV
lower_blue = [90, 50, 50]  
upper_blue = [140, 255, 255]

# Count water bodies in the downloaded satellite image
num_water_bodies = count_water_bodies(MAP_IMAGE_PATH, lower_blue, upper_blue)

print(f"Number of water bodies detected in Gujarat: {num_water_bodies}")
