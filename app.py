import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from svd import *
from camerahandler import CameraHandler

LARGEFONT = ("Verdana", 26)

class SVDApp(tk.Tk):                                                        #-----------Class managing the GUI

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        container = ttk.Frame(self)                                         #-----------Creating a container to hold all the frames
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        self.frames = {}                                                    #-----------Dictionary to keep track of all the frames

        for F in (MainPage, ScanPage, TrainPage, ViewPage):                 #-----------Iterating over all the frames
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(MainPage)                                           #-----------Showing the main page initially

    def show_frame(self, cont):                                             #-----------Function to show a particular frame
        frame = self.frames[cont]
        frame.tkraise()


class MainPage(ttk.Frame):                                                  #-----------Main Page of the GUI

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Welcome to Portable SVD", font=LARGEFONT)
        label.pack(fill=tk.BOTH, expand=tk.TRUE, pady=10, padx=10)

        #-------------------BUTTON-FRAME SCAN/TRAIN-------------------#
        button_frame_s_t = ttk.Frame(self)
        button_frame_s_t.pack(fill=tk.BOTH, expand=tk.TRUE)

        button_cf_scan = ttk.Button(button_frame_s_t, text="Scan", command=lambda: controller.show_frame(ScanPage))
        button_cf_scan.pack(fill=tk.BOTH, expand=tk.TRUE, side=tk.LEFT, padx=10, pady=10)

        button_cf_train = ttk.Button(button_frame_s_t, text="Train", command=lambda: controller.show_frame(TrainPage))
        button_cf_train.pack(fill=tk.BOTH, expand=tk.TRUE, side=tk.LEFT, padx=10, pady=10)
        #------------------------------------------------------------#

        #----------------------BUTTON-FRAME VIEW---------------------#
        button_frame_view = ttk.Frame(self)
        button_frame_view.pack(fill=tk.BOTH, expand=tk.TRUE)
        
        button_cf_view = ttk.Button(button_frame_view, text="View Trained", command=lambda: controller.show_frame(ViewPage))
        button_cf_view.pack(fill=tk.BOTH, expand=tk.TRUE, side=tk.LEFT, padx=10, pady=10)
        #------------------------------------------------------------#

        text_creators = ttk.Label(self, text="Created by: Thöni Andreas, Pluder Jonas")
        text_creators.pack(fill=tk.BOTH, expand=tk.TRUE, pady=10, padx=10)
    


class ScanPage(ttk.Frame):                                                  #-----------Scan Page of the GUI

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.match = Match(0,0)
        self.current_frame = None

        label = ttk.Label(self, text="Scan Page", font=LARGEFONT)
        label.pack(fill=tk.BOTH, expand=tk.TRUE, pady=10, padx=10)

        #-----------------------LEFT-FRAME Camera----------------------#
        image_frame = ttk.Frame(self)
        image_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.image_label = ttk.Label(image_frame)
        self.image_label.pack() #padx=10, pady=10

        #----------------------RIGHT-FRAME Overview--------------------#
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.BOTH, expand=tk.TRUE, side=tk.RIGHT, padx=10, pady=10)

        save_button = ttk.Button(button_frame, text="Scan Image", command=self.take_photo_and_predict)
        save_button.pack(fill=tk.BOTH, expand=tk.TRUE, side=tk.TOP, padx=10, pady=10)

        ttk.Separator(button_frame, orient=tk.HORIZONTAL).pack(fill='x', padx=10, pady=5)
        
        # Match Labels
        match_frame = ttk.Frame(button_frame)
        match_frame.pack(fill=tk.X, padx=10, pady=10)

        self.match_label = ttk.Label(match_frame, text="Match:")
        self.match_label.pack(side=tk.LEFT)

        match_name = find_source_image(self.match)
        self.match_label_name = ttk.Label(match_frame, text=f"{match_name}")
        self.match_label_name.pack(side=tk.LEFT, padx=(5, 0))

        # Score Labels
        score_frame = ttk.Frame(button_frame)
        score_frame.pack(fill=tk.X, padx=10, pady=10)

        self.score_label = ttk.Label(score_frame, text="Distance:")
        self.score_label.pack(side=tk.LEFT)

        self.score_label_value = ttk.Label(score_frame, text=f"{self.match.score}")
        self.score_label_value.pack(side=tk.LEFT, padx=(5, 0))

        ttk.Separator(button_frame, orient=tk.HORIZONTAL).pack(fill='x', padx=10, pady=5)

        back_button = ttk.Button(button_frame, text="Back", command=lambda: controller.show_frame(MainPage))
        back_button.pack(fill=tk.BOTH, expand=tk.TRUE, side=tk.BOTTOM, padx=10, pady=10)

        self.cap = cv2.VideoCapture(0)
        self.update_image()

    
    def update_image(self):
        ret, frame = self.cap.read()                                        #-----------Reading the frame from the camera
        if ret:
            self.current_frame = frame                                      #-----------Setting the current frame to the new frame
            resized_frame = cv2.resize(frame, (240, 180))                   #-----------Resizing the frame
            cv2image = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)       #-----------Converting the frame to RGB fromt the weird BGR
            img = Image.fromarray(cv2image)                                 #-----------Converting the frame to an Image object
            imgtk = ImageTk.PhotoImage(image=img)                           #-----------Converting the Image object to an ImageTk object
            self.image_label.imgtk = imgtk                                  #-----------Setting the image label to the new image
            self.image_label.configure(image=imgtk)                         #-----------Configuring the image label
        self.image_label.after(30, self.update_image)                       #-----------Calling the update_image function again after 10ms
    
    def take_photo_and_predict(self):                                                   #-----------Function to save a photo as np-array
        if hasattr(self, 'current_frame'):
            pred_image = self.current_frame
            self.match = svd_agent.predict(pred_image)
            print(self.match)

            match_name = find_source_image(self.match)
            self.match_label_name.configure(text=f"{match_name}")
            self.score_label_value.configure(text=f"{round(self.match.score)}")
        else:
            print("No current frame available")
        

    def __del__(self):                                                      #-----------Destructor to release the camera
        if self.cap.isOpened():
            self.cap.release()


class TrainPage(ttk.Frame):                                                 #-----------Train Page of the GUI
    
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
    
            label = ttk.Label(self, text="Train Page", font=LARGEFONT)
            label.pack(fill=tk.BOTH, expand=tk.TRUE, pady=10, padx=10)

            #-----------------------LEFT-FRAME Camera----------------------#





class ViewPage(ttk.Frame):                                                  #-----------View Page of the GUI
    
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
    
            label = ttk.Label(self, text="View Page", font=LARGEFONT)
            label.grid(row=0, column=4, padx=10, pady=10)



if __name__ == "__main__":                                                  #-----------Main function to run the GUI

    svd_agent = SVD_Object()
    svd_agent.train('./source_images/')


    app = SVDApp()
    app.mainloop()