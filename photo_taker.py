import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime
import os

# Define the function to update the video feed
def update_frame():
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret:
        # Convert the frame to RGB (OpenCV uses BGR by default)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Convert the frame to an ImageTk object
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        # Update the label with the new image
        label.imgtk = imgtk
        label.configure(image=imgtk)
    # Call update_frame again after 10 ms
    root.after(10, update_frame)

# Define the function to snap a photo
def snap_photo():
    ret, frame = cap.read()
    if ret:
        # Generate a unique filename based on the current date and time
        filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
        absolute_filename = os.path.abspath(f"source_images/{filename}")
        # Save the captured frame to a file
        if cv2.imwrite(absolute_filename, frame):
            print("Image saved as", absolute_filename)
        else:
            print("Error: Could not save image.")

# Create a Tkinter window
root = tk.Tk()
root.title("Camera Capture")

# Create a label to display the video feed
label = ttk.Label(root)
label.grid(row=0, column=0, columnspan=2)

# Create a button to snap a photo
snap_button = ttk.Button(root, text="Snap Photo", command=snap_photo)
snap_button.grid(row=1, column=0, columnspan=2, pady=10)

# Open the camera
camera_index = 0
cap = cv2.VideoCapture(camera_index)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Start the video feed update loop
update_frame()

# Start the Tkinter main loop
root.mainloop()

# Release the camera when the window is closed
cap.release()