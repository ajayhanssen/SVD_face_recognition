import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from svd import *
from camerahandler import CameraHandler

LARGEFONT = ("Verdana", 20)

class SVDApp(tk.Tk):                                                        #-----------Class managing the GUI

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Portable SVD")

        self.camera_handler = CameraHandler()

        container = ttk.Frame(self)                                         #-----------Creating a container to hold all the frames
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        self.frames = {}                                                    #-----------Dictionary to keep track of all the frames

        for F in (MainPage, ScanPage, TrainPage, ViewPage):                 #-----------Iterating over all the frames
            frame = F(parent=container, controller=self, camera_handler=self.camera_handler)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(MainPage)                                           #-----------Showing the main page initially

    def show_frame(self, cont):                                             #-----------Function to show a particular frame
        frame = self.frames[cont]
        frame.tkraise()

        """ for f in self.frames.values():
            f.hide() """

class MainPage(ttk.Frame):                                                  #-----------Main Page of the GUI

    def __init__(self, parent, controller, camera_handler):
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

    def __init__(self, parent, controller, camera_handler):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.camera_handler = camera_handler

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

        match_name = self.match.find_source_image("./source_images/")
        self.match_label_name = ttk.Label(match_frame, text=f"{match_name.split('_')[0]}")
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

        self.update_image()

    
    def update_image(self):
        frame = self.camera_handler.get_frame()                             #-----------Reading the frame from the camera
        if frame is not None:
            self.current_frame = frame                                      #-----------Setting the current frame to the new frame
            resized_frame = cv2.resize(frame, (180, 135))                   #-----------Resizing the frame
            cv2image = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)       #-----------Converting the frame to RGB fromt the weird BGR
            img = Image.fromarray(cv2image)                                 #-----------Converting the frame to an Image object
            imgtk = ImageTk.PhotoImage(image=img)                           #-----------Converting the Image object to an ImageTk object
            self.image_label.imgtk = imgtk                                  #-----------Setting the image label to the new image
            self.image_label.configure(image=imgtk)                         #-----------Configuring the image label
        self.image_label.after(100, self.update_image)                       #-----------Calling the update_image function again after 10ms
    
    def take_photo_and_predict(self):                                                   #-----------Function to save a photo as np-array
        if hasattr(self, 'current_frame'):
            pred_image = self.current_frame
            self.match = svd_agent.predict(pred_image)
            print(self.match)

            match_name = self.match.find_source_image("./source_images/")
            self.match_label_name.configure(text=f"{match_name.split('_')[0]}")
            self.score_label_value.configure(text=f"{round(self.match.score)}")
        else:
            print("No current frame available")
        

class TrainPage(ttk.Frame):                                                 #-----------Train Page of the GUI
    
    def __init__(self, parent, controller, camera_handler):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.camera_handler = camera_handler

        self.train_images = []

        label = ttk.Label(self, text="Train Page", font=LARGEFONT)
        label.pack(fill=tk.BOTH, expand=tk.TRUE, pady=10, padx=10)

        #-----------------------LEFT-FRAME Camera----------------------#
        image_frame = ttk.Frame(self)
        image_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.image_label = ttk.Label(image_frame)
        self.image_label.pack()
        # Button for taking a photo, saves it into an array of max 4 images
        save_button = ttk.Button(image_frame, text="Take Photo", command=self.take_photo)
        save_button.pack(fill=tk.BOTH, expand=tk.TRUE, side=tk.TOP, padx=10, pady=10)

        #----------------------RIGHT-FRAME Training--------------------#
        train_frame = ttk.Frame(self)
        train_frame.pack(fill=tk.BOTH, expand=tk.TRUE, side=tk.RIGHT, padx=10, pady=10)

        self.entry_label = ttk.Label(train_frame, text="Name:")
        self.entry_label.pack(fill=tk.BOTH, expand=tk.TRUE, side=tk.TOP, padx=10, pady=0)

        # Entry for the name of the newly trained object
        self.entry_name = ttk.Entry(train_frame)
        self.entry_name.pack(fill=tk.BOTH, expand=tk.TRUE, side=tk.TOP, padx=10, pady=0)

        # Button for saving the new entry
        save_button = ttk.Button(train_frame, text="Save Entry", command=self.save_new_entry)
        save_button.pack(fill=tk.BOTH, expand=tk.TRUE, side=tk.TOP, padx=10, pady=0)

        # Button for resetting the entry
        reset_button = ttk.Button(train_frame, text="Reset Entry", command=self.reset_entry)
        reset_button.pack(fill=tk.BOTH, expand=tk.TRUE, side=tk.TOP, padx=10, pady=0)

        back_button = ttk.Button(train_frame, text="Back", command=lambda: controller.show_frame(MainPage))
        back_button.pack(fill=tk.BOTH, expand=tk.TRUE, side=tk.BOTTOM, padx=10, pady=10)

        self.images_frame = ttk.Frame(train_frame)
        self.images_frame.pack(fill=tk.BOTH, expand=tk.TRUE, side=tk.TOP, padx=5, pady=5)

        self.update_image()

    def update_image(self):
        frame = self.camera_handler.get_frame()                             #-----------Reading the frame from the camera
        if frame is not None:
            self.current_frame = frame                                      #-----------Setting the current frame to the new frame
            resized_frame = cv2.resize(frame, (180, 135))                   #-----------Resizing the frame
            cv2image = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)       #-----------Converting the frame to RGB fromt the weird BGR
            img = Image.fromarray(cv2image)                                 #-----------Converting the frame to an Image object
            imgtk = ImageTk.PhotoImage(image=img)                           #-----------Converting the Image object to an ImageTk object
            self.image_label.imgtk = imgtk                                  #-----------Setting the image label to the new image
            self.image_label.configure(image=imgtk)                         #-----------Configuring the image label
        self.image_label.after(100, self.update_image)                      #-----------Calling the update_image function again after 10ms

    def update_images_frame(self, events=None):
        # Clear the current images
        for widget in self.images_frame.winfo_children():
            widget.destroy()

        # Convert NumPy arrays to PIL Images, resize, and convert to PhotoImage
        images = [Image.fromarray(img) for img in self.train_images]
        images = [img.resize((25, 25)) for img in images]  # Resize images
        photos = [ImageTk.PhotoImage(img) for img in images]

        for photo in photos:
            label = ttk.Label(self.images_frame, image=photo)
            label.image = photo  # Keep a reference to avoid garbage collection
            label.pack(side=tk.LEFT, padx=2, pady=0)

    def take_photo(self):                                                   #-----------Function to save a photo as np-array
        if hasattr(self, 'current_frame') and len(self.train_images) < 4:
            self.train_images.append(self.current_frame)
            print(len(self.train_images))
        else:
            print("No current frame available")
        self.update_images_frame(self)

    def save_new_entry(self):
        entry_name = self.entry_name.get()                                  #-----------Getting the name of the new entry from the widget

        existing_entries = []                                               #-----------Checking if the name already exists
        for filename in os.listdir("./source_images/"):
            if filename.split("_")[0] not in existing_entries:
                existing_entries.append(filename.split("_")[0])

        if entry_name in existing_entries:
            self.entry_label.configure(text="Name already exists")
            return
        else:
            cnt = 0
            for img in self.train_images:
                cv2.imwrite(f"./source_images/{entry_name}_{cnt}.jpg", img) #-----------Saving the image to the source_images folder
                cnt += 1
            self.entry_label.configure(text="Entry saved")

            svd_agent.train('./source_images/')                             #-----------Retraining the model with the new images

        self.train_images = []
        self.update_images_frame(self)

    def reset_entry(self):
        self.train_images = []
        self.entry_name.delete(0, tk.END)
        self.entry_label.configure(text="Name:")
        self.update_images_frame(self)


class ViewPage(ttk.Frame):                                                  #-----------View Page of the GUI
    
    def __init__(self, parent, controller, camera_handler):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Trained Objects", font=LARGEFONT)
        label.pack(fill=tk.BOTH, expand=tk.TRUE, pady=10, padx=10)

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=tk.TRUE, padx=10, pady=10)

        self.canvas = tk.Canvas(self.main_frame, height=70)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)


        self.back_button = ttk.Button(self, text="Back", command=lambda: controller.show_frame(MainPage))
        self.back_button.pack(fill=tk.BOTH, padx=10, pady=10)

        self.refresh_interval = 5000 # ms, (5sec)
        self.check_for_updates()

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def add_image(self, img_path, name, row, col):
        # Load and resize the image
        img = Image.open(img_path)
        img = img.resize((75, 75))
        img = ImageTk.PhotoImage(img)

        # Create image label
        img_label = ttk.Label(self.scrollable_frame, image=img)
        img_label.image = img  # Reference to avoid garbage collection, needed apparently
        img_label.grid(row=row, column=col, padx=10, pady=5)

        # Create text label
        text_label = ttk.Label(self.scrollable_frame, text=name)
        text_label.grid(row=row + 1, column=col, padx=10, pady=5)

    def check_for_updates(self):
        self.find_object_images()
        self.after(self.refresh_interval, self.check_for_updates)

    def find_object_images(self):
        existing_entries = {}
        row = 0
        col = 0
        for filename in os.listdir("./source_images/"):
            name = filename.split("_")[0]
            if name not in existing_entries:
                existing_entries[name] = cv2.imread(f"./source_images/{filename}")
                self.add_image(f"./source_images/{filename}", name, row, col)
                col += 1
                if col > 3:
                    col = 0
                    row += 2


if __name__ == "__main__":                                                  #-----------Main function to run the GUI

    svd_agent = SVD_Object()
    svd_agent.train('./source_images/')


    app = SVDApp()
    app.mainloop()
    app.camera_handler.release()