import tkinter as tk
import math

class LabeleOperations:
    @staticmethod
    def create_set_of_labeles(window :tk.Label, names, font, size) -> list:
        labels = []

        for animal in enumerate(names):
            label = tk.Label(window, text=animal[1], font=(font, size))
            labels.append(label)

        return labels
    
    @staticmethod
    # Placing widgets around
    def place_around(widgets :list, radius :float, x :float, y :float):
        for i, widget in enumerate(widgets):
            threta = 360 / len(widgets)

            widget.place(x= radius * (math.cos(math.radians(i*threta))) + x, 
                        y= radius * (math.sin(math.radians(i*threta))) + y, 
                        anchor= tk.CENTER)