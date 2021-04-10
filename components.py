import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mixins import FlexibleMixin


class Component(tk.Frame, FlexibleMixin):
    def __init__(self, parent):
        super().__init__(parent)

    def layout(self):
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
        self.layout()
        self.make_flexible(n_rows=2, n_cols=1)

    def layout(self):
        self._search_box.grid(row=0, column=0)
        self._advisor.grid(row=1, column=0)

    def set_search_box(self, value):
        self._search_box = tk.Entry(self)
        self._search_box.bind('<KeyRelease>', self._check_search)

    def get_search_box(self):
        return self._search_box

    search_box = property(get_search_box, set_search_box)

    def set_advisor(self, value):
        items = value
        self._advisor = tk.Listbox(self)
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


class Graph(Component):
    """
    Inspiration: https://datatofish.com/matplotlib-charts-tkinter-gui/
    """
    def __init__(self, parent, figure):
        super().__init__(parent)
        self.figure = figure
        self.canvas = self.figure
        self.layout()
        self.make_flexible(n_rows=1, n_cols=1)

    def layout(self):
        self._canvas.grid(row=0, column=0)

    def set_canvas(self, value):
        figure = value
        canvas = FigureCanvasTkAgg(figure, self)
        self._canvas = canvas.get_tk_widget()

    def get_canvas(self):
        return self._canvas

    def _update_graph(self, figure):
        self.canvas.destroy()
        plt.close('all')
        self.canvas = figure

    def update(self, figure):
        self._update_graph(figure)
        self.layout()

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
                    label = tk.Label(self, text=cells[col])
                else:
                    label = tk.Label(self, text=cells[row][col])
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
        n_cols = len(labels)
        for col, (label, callback) in enumerate(zip(labels, callbacks)):
            button = tk.Button(self, text=label, command=callback)# width=50)
            button.grid(row=0, column=col,  sticky="we", padx=5, pady=5)

        self.make_flexible(n_cols=n_cols, n_rows=1)

class StateBar(Component):
    STATE_NAME_COL = 0
    STATE_VALUE_COL = 1
    N_COLUMNS = 2

    def __init__(self, parent, states):
        super().__init__(parent)
        self.states = states
        n_rows = len(states)
        self.make_flexible(n_rows=n_rows, n_cols=self.N_COLUMNS)

    def set_states(self, value):
        states = value
        self._states = {}

        for row, (name, value) in enumerate(states.items()):
            name_label = tk.Label(self, text=name)
            name_label.grid(row=row, column=self.STATE_NAME_COL)

            value_label = tk.Label(self, text=value)
            value_label.grid(row=row, column=self.STATE_VALUE_COL)

            self._states[name] = value_label

    def get_states(self):
        return self._states

    states = property(get_states, set_states)




