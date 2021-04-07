import threading
import tkinter as tk
from tkinter import ttk
from controllers import MainController, VaccinationController, DatasetIntegrityController
from utils import Logger
import socket
import datetime

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

    CONTROLLER_CLASSES = [
        MainController,
        VaccinationController,
        DatasetIntegrityController,
    ]

    def __init__(self, international_dataset, local_dataset):
        super().__init__()
        #self.international_dataset = international_dataset
        #self.local_dataset = local_dataset
        #self.countries = ...
        #self.updater = ...  # Updater()
        self.start_time = datetime.datetime.now()
        self.title(self.NAME)
        self.frame = None
        self.view_classes = self.CONTROLLER_CLASSES
        self.controllers = self.CONTROLLER_CLASSES
        self.viewer = Viewer(self.controllers, MainController.VIEW_CLASS)
        self.geometry("750x500")

    def set_frame(self, value):
        self._frame = tk.Frame()
        self._frame.pack(side="top", fill="both", expand=True)
        self._frame.grid_rowconfigure(0, weight=1)
        self._frame.grid_columnconfigure(0, weight=1)

    def get_frame(self):
        return self._frame

    frame = property(get_frame, set_frame)

    def set_view_classes(self, value):
        controller_classes = value
        self._view_classes = []

        for controller_class in controller_classes:
            view_class = controller_class.VIEW_CLASS
            self._view_classes.append(view_class)

    def get_view_classes(self):
        return self._view_classes

    view_classes = property(get_view_classes, set_view_classes)

    def set_controllers(self, value):
        controller_classes = value
        self._controllers = []
        
        for controller_class in controller_classes:
            controller = controller_class(self)
            self._controllers.append(controller)

    def get_controllers(self):
        return self._controllers

    controllers = property(get_controllers, set_controllers)

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
        self.viewer.show_view()

class Viewer:
    """
    Switches between views.
    """

    def __init__(self, controllers, active_view_class):
        self.views = controllers
        self.active_view = self.views[active_view_class.__name__]

    def set_views(self, value):
        controllers = value
        self._views = {}

        for controller in controllers:
            view_class = controller.VIEW_CLASS
            context = view_class.__name__
            view = controller.view
            self._views[context] = view

    def get_views(self):
        return self._views

    views = property(get_views, set_views)

    def show_view(self, context=None):
        if context is None:
            view = self.active_view
        else:
            view = self._views[context]
            self.active_view = view

        view.tkraise()

    def update(self):
        pass


if __name__ == '__main__':
    logger = Logger('http://covid.martinpolacek.eu/writeLog.php')
    logger.send_info("Aplikace spuštěna na " + str(socket.gethostname()))
    app = App(None, None)
    app.run()

