import tkinter as tk
from tkinter import ttk
from components import Navigation, Graph, Table, SearchBar, StateBar, ListBox
from utils import Callback
from mixins import FlexibleMixin


class View(tk.Frame, FlexibleMixin):
    """
    Represents visual part of app.
    Works with data provided by controller
    """
    TITLE = None
    N_COLUMNS = None
    N_ROWS = None
    NAVIGATION_BUTTON_COLOR = "#91cde3"

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.navigation = controller.app.view_classes

        self.title = tk.Label(self, text=self.TITLE, font=("Arial", 25))

    def layout(self):
        pass

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

        self._navigation = Navigation(self, texts, callbacks, btn_color=self.NAVIGATION_BUTTON_COLOR)

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
    N_COLUMNS = 2
    N_ROWS = 2

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        help_text = "WHO vaccination stats are updated one or two times per week for some countries only. \n" \
                    "WHO stats are updated each day during evening. \n" \
                    "MZČR stats are updated each day during morning."
        self.help = tk.Label(self, text=help_text, justify="center")
        self.layout()

    def layout(self):
        self.navigation.grid(row=0, column=0, columnspan=self.N_COLUMNS, sticky="we")
        self.title.grid(row=1, column=0, columnspan=self.N_COLUMNS, sticky="we")
        self.help.grid(row=2, column=0, columnspan=self.N_COLUMNS, sticky="we")
        self.make_flexible(n_rows=self.N_ROWS, n_cols=self.N_COLUMNS)
        self.grid(row=0, column=0, sticky="nsew")


class VaccinationView(View):
    TITLE = "Vaccination Overview"
    N_COLUMNS = 3
    N_ROWS = 4

    REMOVE_HELP_TEXT = "Click on country to be removed."
    ADD_HELP_TEXT = "Search for country in search box.\n" \
                    "Click on country to be added.\n" \
                    "Only {n_country} countries can be added."

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.state_bar = StateBar(self, controller.status)
        self.graph = Graph(self, controller.figure)

        help_text = self.ADD_HELP_TEXT.format(n_country=self.controller.MAX_COUNTRIES_SELECTED)
        self.search_bar = SearchBar(self, controller.selectable_countries, controller.add_country,
                                    help_text=help_text)
        self.deselect_box = ListBox(self, controller.selected_countries, controller.remove_country,
                                    help_text=self.REMOVE_HELP_TEXT)
        self.update_button = tk.Button(self, text="Check for update", command=Callback(self.controller.update_app))
        self.layout()

    def layout(self):
        self.navigation.grid(row=0, column=0, columnspan=self.N_COLUMNS, sticky="we")
        self.title.grid(row=1, column=0)
        self.state_bar.grid(row=1, column=1)
        self.update_button.grid(row=1, column=2)
        self.search_bar.grid(row=2, column=0, padx=30)
        self.deselect_box.grid(row=3, column=0, padx=30)
        self.graph.grid(row=2, column=1, columnspan=2, rowspan=2)
        self.make_flexible(n_rows=self.N_ROWS, n_cols=self.N_COLUMNS)
        self.grid(row=0, column=0, sticky="nsew")

    def update(self):
        self.state_bar.update(self.controller.status)
        self.search_bar.update(self.controller.selectable_countries)
        self.graph.update()
        self.deselect_box.update(self.controller.selected_countries)


class DatasetIntegrityView(View):
    TITLE = "Dataset Integrity Overview"
    N_COLUMNS = 3
    N_ROWS = 2

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.state_bar = StateBar(self, controller.status)
        self.table = Table(self, controller.overview)
        self.update_button = tk.Button(self, text="Check for update", command=Callback(self.controller.update_app))
        self.layout()

    def layout(self):
        self.navigation.grid(row=0, column=0, columnspan=self.N_COLUMNS, sticky="we")
        self.title.grid(row=1, column=0)
        self.state_bar.grid(row=1, column=1)
        self.update_button.grid(row=1, column=2)
        self.table.grid(row=2, column=0, columnspan=self.N_COLUMNS, pady=(25, ))
        self.make_flexible(n_rows=self.N_ROWS, n_cols=self.N_COLUMNS)
        self.grid(row=0, column=0, sticky="nsew")

    def update(self):
        self.state_bar.update(self.controller.status)
        self.table.update(self.controller.overview)






