import threading
import tkinter as tk
from tkinter import ttk
from views import MainView, VaccinationOverview, DatasetIntegrityOverview


class Updater:
    """
    Takes care of updating app.
    """
    UPDATE_FREQUENCY = 15 * 60  # waiting time

    def __init__(self, datasets, app):
        self.app = app
        self.datasets = datasets

    def _update_controllers(self):
        for controller in self.app.controllers:
            controller.update()

    def update(self, dataset):
        updated = dataset.update()
        if updated:
            self._update_controllers()
            self.app.viewer.update()

        # create new thread
        threading.Timer(self.UPDATE_FREQUENCY, self.update, dataset)

    def run(self):
        for dataset in self.datasets:
            if dataset.update_time:
                self.update(dataset)


class App(tk.Tk):
    """
    Inspiration: https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/
    """
    NAME = "Covid Comparator"

    VIEW_CLASSES = [
        MainView,
        VaccinationOverview,
        DatasetIntegrityOverview
    ]

    def __init__(self, international_dataset, local_dataset):
        super().__init__()
        #self.international_dataset = international_dataset
        #self.local_dataset = local_dataset
        #self.countries = ...
        #self.updater = ...  # Updater()
        self.title(self.NAME)
        self.frame = None
        self.views = None
        #self.geometry("250x150+300+300")

    def set_frame(self, value):
        self._frame = tk.Frame()
        self._frame.pack(side="top", fill="both", expand=True)
        self._frame.grid_rowconfigure(0, weight=1)
        self._frame.grid_columnconfigure(0, weight=1)

    def get_frame(self):
        return self._frame

    frame = property(get_frame, set_frame)

    def set_views(self, value):
        self._views = {}

        for view_class in self.VIEW_CLASSES:
            context = view_class.__name__
            view = view_class(self.frame, self)
            self._views[context] = view

            if view_class == MainView:
                self.active_view = view

    def get_views(self):
        return self._views

    views = property(get_views, set_views)

    def show_view(self, context=None):
        if context is None:
            view = self.active_view
        else:
            print(context)
            view = self.views[context]
            self.active_view = view

        view.tkraise()

    def load(self):
        """
        Load in data.
        """
        self.international_dataset.load()
        self.local_dataset.load(self.frame)

    def run(self):
        #self.load()
        #self.updater.run()
        self.mainloop()
        self._viewer.show_view()


if __name__ == '__main__':
    app = App(None, None)
    app.run()

