import cv2
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk

class CameraHandler():
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
    
    def get_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (240, 180))
            return ImageTk.PhotoImage(image=Image.fromarray(frame))
        return None
    
    def release():
        self.cap.release()