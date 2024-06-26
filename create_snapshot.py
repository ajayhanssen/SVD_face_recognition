import cv2
from datetime import datetime
import os

camera_index = 0

cap = cv2.VideoCapture(camera_index)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

ret,frame = cap.read()

if not ret:
    print("Error: Could not read frame.")
    exit()
else:
    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
    absolute_path = os.path.abspath(f"source_images/{filename}")

    cv2.imwrite(absolute_path, frame)
    print("Image saved as", filename)


cap.release()
cv2.destroyAllWindows()