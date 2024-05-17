import numpy as np
import cv2
from skimage import color

# Initialize the camera
camera = cv2.VideoCapture(0)  # 0 is usually the default camera

# Check if the camera is opened successfully
if not camera.isOpened():
    print("Error: Unable to access the camera.")
    exit()

# Capture a single frame
ret, frame = camera.read()

# Check if the frame was captured successfully
if not ret:
    print("Error: Unable to capture frame.")
    exit()

# Save the frame as an image
cv2.imwrite("captured_image.jpg", frame)
#gray_image = color.rgb2gray(rgb_image)


print(frame.shape)
print(type(frame))

# Release the camera
camera.release()