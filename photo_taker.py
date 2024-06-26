import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime
import os

class SVDApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Portable SVD")

        # Create a container to hold all the frames
        container = ttk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew")

        # Initialize a dictionary to keep track of frames
        self.frames = {}

        # Create frames and add them to the container
        for F in (MainPage, StorePage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the main page initially
        self.show_frame("MainPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class MainPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ttk.Label(self, text="Welcome to the Camera App")
        label.pack(pady=10)

        button = ttk.Button(self, text="Go to Camera",
                            command=lambda: controller.show_frame("StorePage"))
        button.pack()

class StorePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.label = ttk.Label(self)
        self.label.pack()

        self.snap_button = ttk.Button(self, text="Snap Photo", command=self.snap_photo)
        self.snap_button.pack(pady=10)

        # Open the camera
        self.cap = cv2.VideoCapture(0)

        # Check if the camera opened successfully
        if not self.cap.isOpened():
            print("Error: Could not open camera.")
            self.controller.quit()
            return

        # Start the video feed update loop
        self.update_frame()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert the frame to RGB (apparently opencv uses BGR)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert the frame to an ImageTk object
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            # Update the label with the new image
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)
        # Call update_frame again after 10 ms
        self.controller.after(10, self.update_frame)

    def snap_photo(self):
        ret, frame = self.cap.read()
        if ret:
            # Generate a unique filename based on the current date and time
            filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
            absolute_filename = os.path.abspath(f"source_images/{filename}")
            # Save the captured frame to a file
            if cv2.imwrite(absolute_filename, frame):
                print("Image saved as", absolute_filename)
            else:
                print("Error: Could not save image.")

    def __del__(self):
        # Release the camera when the window is closed
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()

if __name__ == "__main__":
    svdapp = SVDApp()
    svdapp.mainloop()
