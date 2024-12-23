import tkinter as tk
import ttkbootstrap as ttk
from labelsimages import LabelesAndImages
from PIL import Image, ImageTk, ImageFile

ROOT_SCREEN_X = 1280
ROOT_SCREEN_Y = 800

APP_NAME = "Predators"

class App(ttk.Window):
    # Основне вікно
    def __init__(self):
        super().__init__(resizable=(False, False))
        self.geometry(f"{ROOT_SCREEN_X}x{ROOT_SCREEN_Y}")
        self.title(APP_NAME)

        self.style.theme_use('morph')
        
        self.bind("<Motion>", lambda event, : self.motionEvent(event))
        
        self.create_zoo()
        self.mainloop()
        
    # Mouse pos tracker
    def motionEvent(self, event :tk.Event):
        print(f"X: {event.x}, Y: {event.y}")

    # Button creating along with labels
    def create_zoo(self):
        BUTTON_POS_X = ROOT_SCREEN_X/2
        BUTTON_POS_Y = ROOT_SCREEN_Y/2
        
        min_resolution = min(BUTTON_POS_X, ROOT_SCREEN_X - BUTTON_POS_X, BUTTON_POS_Y, ROOT_SCREEN_Y - BUTTON_POS_Y)

        RADIUS_FROM_BUTTON = min_resolution / 1.3
        IMAGE_SIZE = (min_resolution / 3.5) / min_resolution
    	
        self.image_canvases = []

        self.create_button(BUTTON_POS_X, BUTTON_POS_Y, "Predators")

        animals = {
            "Bear": Image.open("bear.png"),
            "Fox": Image.open("fox.png"),
            "Lynx": Image.open("lynx.png"),
            "Tiger": Image.open("tiger.png"),
            "Wolf": Image.open("wolf.png"),
            "Shark": Image.open("shark.png")
        }

        self.imagetk = 0

        animal_names = [str(animal) for animal in animals.keys()]

        self.animal_labels :tk.Widget = LabelesAndImages.create_set_of_labeles(window=self, names=animal_names, font='Bahnschrift', size=12)

        for label in self.animal_labels:
            label.bind("<Enter>", lambda event, : self.show_image_by_label(event=event, images=animals, scale=IMAGE_SIZE))

        LabelesAndImages.place_around(widgets=self.animal_labels, radius=RADIUS_FROM_BUTTON, x=BUTTON_POS_X, y=BUTTON_POS_Y)

    # Animation loop
    def show_image(self, imageCanvas :tk.Canvas, image :Image, imageid :int, startValue, scale :int, animation_time :int):
        if startValue > animation_time: return
        try:
            imageCanvas.delete(imageid)
            imageid = None
            imageCanvas.imagetk = None  # delete previous image from the canvas

            width, height = image.size
            new_size = int(startValue/animation_time * width * scale), int(startValue/animation_time * height * scale)
            imagetk = ImageTk.PhotoImage(image.resize(new_size))
            imageid = imageCanvas.create_image((0, 0), anchor=tk.NW, image=imagetk)

            imageCanvas.scale('all', new_size[0]/2, new_size[1]/2, startValue/animation_time, startValue/animation_time)
            imageCanvas.imagetk = imagetk  # keep an extra reference to prevent garbage-collection

            startValue+=1
            self.after(10, lambda: self.show_image(imageCanvas=imageCanvas, image=image, imageid=imageid, startValue=startValue, scale=scale, animation_time=animation_time))
        except: None
            
    # Show image on tk.Event coords
    def show_image_by_label(self, event :tk.Event, images, scale):
        image :ImageFile = images[event.widget.cget("text")]
        width, height = image.size

        # Create image_canvas and put image on it
        image_canvas = tk.Canvas(self.master)
        image_canvas.imagetk = ImageTk.PhotoImage(image.resize((int(width/4), int(height/4)))) # Create refference to prevent garbage collection
        image_canvas.place(x=event.widget.winfo_x(),y=event.widget.winfo_y(), width=width * scale, height=height * scale, anchor=tk.CENTER)

        image_id = image_canvas.create_image(0, 0, anchor=tk.NW, image=image_canvas.imagetk)

        self.show_image(imageCanvas=image_canvas, image=image, imageid=image_id, startValue=1, scale=scale, animation_time=30)

        self.image_canvases.append(image_canvas)

    def on_button_click(self):
        for canvas in self.image_canvases:
            canvas.destroy()

    def create_button(self, x, y, text :str):
        button = tk.Button(self, text=text, bg='deepskyblue', command=self.on_button_click)
        button.place(x=x, y=y, anchor=tk.CENTER)

App()