import tkinter as tk
from tkinter import ttk


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


class Graph(Component):
    """
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = ...
        self.toolbar = ... # removal buttons
        pass


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





