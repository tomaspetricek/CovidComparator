import tkinter as tk
from tkinter import ttk
from components import Navigation, Graph, Table, SearchBar
from utils import Callback


class View(tk.Frame):
    """
    Represents visual part of app.
    Works with data provided by controller
    """
    TITLE = None

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.navigation = controller.app.view_classes

    def set_navigation(self, value):
        view_classes = value
        texts = []
        callbacks = []

        for view_class in view_classes:
            if self.__class__ != view_class:
                texts.append(view_class.TITLE)
                context = view_class.__name__
                callback = Callback(self.controller.show_view, context=context)
                callbacks.append(callback)

        self._navigation = Navigation(self, texts, callbacks)

    def get_navigation(self):
        return self._navigation

    navigation = property(get_navigation, set_navigation)

    def update(self):
        """
        Updates whole view.
        """
        pass

class MainView(View):
    TITLE = "Main"

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        title = tk.Label(self, text=self.TITLE)
        title.pack(pady=10, padx=10)

        self.grid(row=0, column=0, sticky="nsew")


class VaccinationView(View):
    TITLE = "Vaccination Overview"

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        title = tk.Label(self, text=self.TITLE)
        title.pack(pady=10, padx=10)
        # self.state_bar = ...
        # self.graph = Graph(self, controller.figure)
        # self.search_bar = SearchBar(self, controller.countries, controller.add_country)
        # self.deselect_box =
        self.grid(row=0, column=0, sticky="nsew")

    def update(self):
        # self.state.update(self.controller.state)
        # self.search_bar.update(self.controller.selectable_countries)
        # self.graph.update(self.controller.figure)
        # self.deselect_box(self.selected_countries)
        pass


class DatasetIntegrityView(View):
    TITLE = "Dataset Integrity Overview"

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        title = tk.Label(self, text=self.TITLE)
        title.pack(side="top", fill="x", pady=10)
        # self.state_bar = ...
        # self.table = Table(self, controller.overview)
        self.grid(row=0, column=0, sticky="nsew")

    def _update_table(self, new_rows):
        pass

    def update(self):
        # self.state.update()
        pass






