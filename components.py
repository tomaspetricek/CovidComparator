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
    def __init__(self, parent, data):
        super().__init__(parent)
        self._free_row = 0
        self.header = data
        self.body = data

    def _add(self, cells, n_rows, n_cols):
        for row in range(n_rows):
            for col in range(n_cols):
                if n_rows == 1:
                    label = tk.Label(self.parent, text=cells[col])
                else:
                    label = tk.Label(self.parent, text=cells[row][col])
                # label.grid(row=self._free_row + row, column=col)
                label.pack()

        self._free_row += n_rows

    def set_header(self, value):
        data = value
        self._header = data.columns.values.tolist()
        n_rows = 1
        n_cols = len(self._header)
        self._add(self._header, n_rows, n_cols)

    def get_header(self):
        return self._header

    header = property(get_header, set_header)

    def set_body(self, value):
        data = value
        self._body = data.to_numpy()
        n_rows, n_cols = self._body.shape
        self._add(self._body, n_rows, n_cols)

    def get_body(self):
        return self._body

    body = property(get_body, set_body)


class Navigation(Component):
    """
    Inspiration: https://www.youtube.com/watch?v=ZS2_v_zsPTg
    """
    def __init__(self, parent, labels, callbacks):
        super().__init__(parent)
        for label, callback in zip(labels, callbacks):
            button = tk.Button(parent, text=label, command=callback)
            button.pack()





