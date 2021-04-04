import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Component:
    def __init__(self, parent):
        self.parent = parent
        pass

class SearchBar(Component):
    """
    Inspired: # https://www.geeksforgeeks.org/autocmplete-combobox-in-python-tkinter/
    """
    def __init__(self, parent, items, on_select):
        super().__init__(parent)
        self.items = items
        self.search_box = None
        self.advisor = self.items
        self.on_select = on_select

    def set_search_box(self, value):
        self._search_box = tk.Entry(self.parent)
        self._search_box.pack()
        self._search_box.bind('<KeyRelease>', self._check_search)

    def get_search_box(self):
        return self._search_box

    search_box = property(get_search_box, set_search_box)

    def set_advisor(self, value):
        items = value
        self._advisor = tk.Listbox(self.parent)
        self._advisor.pack()
        self._update_advisor(items)
        self.advisor.bind("<<ListboxSelect>>", self._on_select)

    def get_advisor(self):
        return self._advisor

    advisor = property(get_advisor, set_advisor)

    def _check_search(self, event):
        target = event.widget.get()

        if target == '':
            items_to_display = self.items
        else:
            items_to_display = []
            for item in self.items:
                if target.lower() in item.lower():
                    items_to_display.append(item)

        self._update_advisor(items_to_display)

    def _update_advisor(self, items_to_display):
        # clear previous data
        self.advisor.delete(0, 'end')

        # put new data
        for item in items_to_display:
            self.advisor.insert('end', item)

    def _on_select(self, event):
        # Note here that Tkinter passes an event object to onselect()
        widget = event.widget
        index = int(widget.curselection()[0])
        value = widget.get(index)
        self.on_select(value)

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
        self.frame = tk.Frame(self.parent)
        self._free_row = 0
        self.header = data
        self.body = data
        self.frame.pack()

    def _add(self, cells, n_rows, n_cols):
        for row in range(n_rows):
            for col in range(n_cols):
                if n_rows == 1:
                    label = tk.Label(self.frame, text=cells[col])
                else:
                    label = tk.Label(self.frame, text=cells[row][col])
                label.grid(row=self._free_row + row, column=col)

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





