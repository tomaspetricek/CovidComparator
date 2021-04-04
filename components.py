import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Component:
    def __init__(self, parent):
        self.parent = parent
        pass

class AutocompleteSearchBar(Component):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = ...
        self.toolbar = ... # removal buttons
        pass

class StatusBar(Component):
    def __init__(self, parent):
        super().__init__(parent)
        pass

class Graph(Component):
    """
    Inspiration: https://datatofish.com/matplotlib-charts-tkinter-gui/
    """
    def __init__(self, parent, figure):
        super().__init__(parent)
        self.canvas = figure

    def set_canvas(self, value):
        figure = value
        self._canvas = FigureCanvasTkAgg(figure, self.parent)
        self._canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

    def get_canvas(self):
        return self._canvas

    canvas = property(get_canvas, set_canvas)


class Table(Component):
    """
    Inspiration: https://www.geeksforgeeks.org/create-table-using-tkinter/
    """
    pass


class Navigation(Component):
    """
    Inspiration: https://www.youtube.com/watch?v=ZS2_v_zsPTg
    """
    def __init__(self, parent, labels, callbacks):
        super().__init__(parent)
        for label, callback in zip(labels, callbacks):
            button = tk.Button(parent, text=label, command=callback)
            button.pack()





