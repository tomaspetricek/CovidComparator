import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mixins import FlexibleMixin


class Component(tk.Frame, FlexibleMixin):
    def __init__(self, parent, help_text=None):
        super().__init__(parent)
        if help_text:
            self.help = tk.Label(self, text=help_text)
        else:
            self.help = None

    def layout(self):
        pass

    def update(self, *args, **kwargs):
        pass

    def clear(self):
        """
        Removes all widgets from the frame.
        """
        for widget in self.winfo_children():
            widget.destroy()

class ListBox(Component):
    def __init__(self, parent, items, on_select, help_text=None):
        super().__init__(parent, help_text)
        self.list_box = items
        self.on_select = on_select
        self.layout()
        self.make_flexible(n_rows=1, n_cols=1)

    def layout(self):
        list_box_row = 0

        if self.help:
            self.help.grid(row=0, column=0)
            list_box_row = 1

        self._list_box.grid(row=list_box_row, column=0)

    def set_list_box(self, value):
        items = value
        self._list_box = tk.Listbox(self)
        self._update_items(items)
        self._list_box.bind("<<ListboxSelect>>", self._on_select_event_handler)

    def get_list_box(self):
        return self._list_box

    list_box = property(get_list_box, set_list_box)

    def _on_select_event_handler(self, event):
        # Note here that Tkinter passes an event object to onselect()
        widget = event.widget
        cursor_selection = widget.curselection()

        if cursor_selection != ():
            index = cursor_selection[0]
            value = widget.get(index)
            self.on_select(value)

    def _update_items(self, items):
        # clear previous data
        self._list_box.delete(0, 'end')

        # put new data
        for item in items:
            self._list_box.insert('end', item)
            
    def update(self, items):
        self._update_items(items)


class SearchBar(Component):
    """
    Inspired: # https://www.geeksforgeeks.org/autocmplete-combobox-in-python-tkinter/
    """
    def __init__(self, parent, items, on_select, help_text=None):
        super().__init__(parent, help_text)
        self.items = items
        self.search_box = None
        self.advisor = ListBox(self, items, on_select)
        self.on_select = on_select
        self.layout()
        self.make_flexible(n_rows=2, n_cols=1)

    def layout(self):
        free_row = 0

        if self.help:
            self.help.grid(row=0, column=0)
            free_row = 1

        self._search_box.grid(row=free_row, column=0)
        self.advisor.grid(row=free_row + 1, column=0)

    def set_search_box(self, value):
        self._search_box = tk.Entry(self)
        self._search_box.bind('<KeyRelease>', self._check_search)

    def get_search_box(self):
        return self._search_box

    search_box = property(get_search_box, set_search_box)

    def _check_search(self, event):
        target = event.widget.get()

        if target == '':
            items_to_display = self.items
        else:
            items_to_display = []
            for item in self.items:
                if target.lower() in item.lower():
                    items_to_display.append(item)

        self.advisor.update(items_to_display)

    def _on_select(self, event):
        # Note here that Tkinter passes an event object to onselect()
        widget = event.widget
        index = int(widget.curselection()[0])
        value = widget.get(index)
        self.on_select(value)
        
    def update(self, items):
        self.items = items
        self.advisor.update(items)


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
        self._canvas_widget.grid(row=0, column=0)

    def set_canvas(self, value):
        figure = value
        canvas = FigureCanvasTkAgg(figure, self)
        self._canvas_widget = canvas.get_tk_widget()
        self._canvas = canvas

    def get_canvas(self):
        return self._canvas

    canvas = property(get_canvas, set_canvas)

    def update(self):
        self._canvas.draw()


class Table(Component):
    """
    Inspiration: https://www.geeksforgeeks.org/create-table-using-tkinter/
    """
    def __init__(self, parent, data):
        super().__init__(parent)
        self.data = data
        self._free_row = 0
        self.header = self.data
        self.body = self.data
        # self.make_flexible()

    def _add(self, values, n_rows, n_cols):
        cells = list()
        cell_row = None

        for row in range(n_rows):
            for col in range(n_cols):
                cell_row = list()

                if n_rows == 1 and type(values) == list:
                    text = values[col]
                else:
                    text = values[row][col]

                label = tk.Label(self, text=text, borderwidth=1, relief="solid")
                label.grid(row=self._free_row + row, column=col, sticky="nesw")
                cell_row.append(label)

            cells.append(cell_row)

        self._free_row += n_rows
        return cells

    def set_header(self, value):
        data = value
        values = data.columns.values.tolist()
        n_rows = 1
        n_cols = len(values)
        self._header = self._add(values, n_rows, n_cols)

    def get_header(self):
        return self._header

    header = property(get_header, set_header)

    def set_body(self, value):
        data = value
        values = data.to_numpy()
        n_rows, n_cols = values.shape
        self._body = self._add(values, n_rows, n_cols)

    def get_body(self):
        return self._body

    body = property(get_body, set_body)

    def _clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def update(self, data):
        self._clear()
        self.data = data
        self.header = self.data
        self.body = self.data

class Navigation(Component):
    """
    Inspiration: https://www.youtube.com/watch?v=ZS2_v_zsPTg
    """
    def __init__(self, parent, labels, callbacks, btn_color=None):
        super().__init__(parent)
        n_cols = len(labels)

        background_color_key = 'color.TButton'

        if btn_color:
            ttk.Style().configure(background_color_key, background='black')

        for col, (label, callback) in enumerate(zip(labels, callbacks)):
            button = ttk.Button(self, text=label, command=callback)

            if btn_color:
                button.config(style=background_color_key)

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

    def _update_states(self, states):
        for name, label in self._states.items():
            label.config(text=states[name])

    def update(self, states):
        self._update_states(states)
        




