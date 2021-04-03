import tkinter as tk
from tkinter import ttk
from components import Navigation


class Callback:
    def __init__(self, fun, *args, **kwargs):
        self.fun = fun
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        self.fun(*self.args, **self.kwargs)

class View(tk.Frame):
    """
    Represents visual part of app.
    Works with data provided by controller
    """
    TITLE = None

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.navigation = controller.VIEW_CLASSES

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


class VaccinationOverview(View):
    TITLE = "Vaccination Overview"

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        # self.data = app.international_dataset
        # self.selected_countries = ...
        # self.status = ...

        title = tk.Label(self, text=self.TITLE)
        title.pack(pady=10, padx=10)
        #self.state = ...
        #self.graph = ...
        #self.search_bar = ...
        self.grid(row=0, column=0, sticky="nsew")

    def update_graph(self):
        pass

    def update(self):
        pass

    def add_country(self, country):
        # add country to selected countries
        # update graph
        self.update_graph()
        pass

    def remove_country(self, country):
        # remove country from selected countries
        # update graph
        self.update_graph()
        pass


class DatasetIntegrityOverview(View):
    TITLE = "Dataset Integrity Overview"

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        title = tk.Label(self, text=self.TITLE)
        title.pack(side="top", fill="x", pady=10)
        # self.state = ...
        # self.table = ...

        # self.data = self.app.international_dataset, self.app.local_dataset
        # self.status = ...
        self.grid(row=0, column=0, sticky="nsew")

    def update_table(self):
        pass

    def update(self):
        pass

    def get_data(self):
        return self._data

    def set_data(self, value):
        international_dataset, local_dataset = value
        filtered_international_dataset = international_dataset.loc[international_dataset["country"] == "Czechia"]
        filtered_international_dataset = filtered_international_dataset.dropna(how='any', axis=0)

        merged_dataset = pd.merge_asof(international_dataset, local_dataset, on='date posted')
        diff_daily_infected = merged_dataset["daily increase of infected_x"] - merged_dataset["daily increase of infected_y"]
        diff_total_infected = merged_dataset["total number of infected_x"] - merged_dataset["total number of infected_y"]
        diff_date_posted = merged_dataset["date loaded_x"] - merged_dataset["date loaded_y"]

        self._data = pd.DataFrame({'date posted': merged_dataset["date posted"], "diffrence daily increase of infected" : diff_daily_infected,
                            "diffrence total number of infected": diff_total_infected, "difference date posted": diff_date_posted})

    data = property(get_data, set_data)


# if __name__ == "__main__":
#     controller_ = DatasetIntegrityController(None)
#     cr_data = MZCRFetcher().fetch(None)
#     controller_.set_data((cr_data, cr_data))