import threading
import tkinter as tk
from tkinter import ttk
from controllers import MainController, VaccinationController, DatasetIntegrityController
from utils import Logger
import socket
import datetime
import time
from data import *
from config import *


class Updater:
    """
    Takes care of updating app.
    """
    UPDATE_FREQUENCY = 30 # 15 * 60  # waiting time
    DATASET_LOCK = threading.Lock()

    def __init__(self, datasets, controllers):
        self.controllers = controllers
        self.datasets = datasets

    def _update_datasets(self):
        with self.DATASET_LOCK:
            for dataset in self.datasets:
                dataset.update()

    def _update_controllers(self):
        for controller in self.controllers:
            controller.update()
    
    def update(self):
        self._update_datasets()
        self._update_controllers()

    def _keep_running(self):
        self.update()
        if self._check_datasets_up_to_date():
            threading.Timer(self.seconds_until_midnight(), self._keep_running)
        else:
            threading.Timer(self.UPDATE_FREQUENCY, self._keep_running)

    def _check_datasets_up_to_date(self):
        for dataset in self.datasets:
            if not dataset.today_updated:
                return False
        return True

    def seconds_until_midnight(self):
        now = datetime.datetime.now()
        return ((24 - now.hour - 1) * 60 * 60) + ((60 - now.minute - 1) * 60) + (60 - now.second)

    def run(self):
        """
        Runs periodic updates based on UPDATE_FREQUENCY.
        """
        self._keep_running()


class App(tk.Tk):
    """
    Inspiration: https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/
    """
    NAME = "Covid Comparator"

    MIN_WIDTH = 1000
    MIN_HEIGHT = 550

    CONTROLLER_CLASSES = [
        MainController,
        VaccinationController,
        DatasetIntegrityController,
    ]

    def __init__(self, international_dataset, local_dataset, vaccination_dataset, logger_url):
        super().__init__()
        self.international_dataset = international_dataset
        self.vaccination_dataset = vaccination_dataset
        self.local_dataset = local_dataset
        self.vaccination_dataset = vaccination_dataset
        self.logger = Logger(logger_url)
        self.load()
        self.start_time = datetime.datetime.now()
        self.title(self.NAME)
        self.frame = None
        self.view_classes = self.CONTROLLER_CLASSES
        self.controllers = self.CONTROLLER_CLASSES
        self.viewer = Viewer(self.controllers, MainController.VIEW_CLASS)
        self.minsize(width=self.MIN_WIDTH, height=self.MIN_HEIGHT)
        self.updater = Updater([self.international_dataset, self.vaccination_dataset, self.local_dataset],
                               self.controllers)

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
        self.vaccination_dataset.load()
        self.international_dataset.load()
        self.local_dataset.load()

    def run(self):
        self.updater.run()
        self.viewer.show_view()
        self.mainloop()

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
    # logger.send_info("Aplikace spuštěna na " + str(socket.gethostname()))

    fetcher = WHOVaccinationFetcher()
    mzcr_fetcher = MZCRStatsFetcher()
    who_fecther = WHOStatsFetcher()

    start_time = datetime.datetime.now() - datetime.timedelta(days=1)   # datetime.datetime(2020, 1, 1),

    vaccination_dataset = VaccinationDataset(fetcher, VACCINATION_DATASET,  start_time, "vaccinations")
    local_dataset = StatsDataset(mzcr_fetcher, LOCAL_STATS_DATASET, start_time, "czech stats")
    international_dataset = StatsDataset(who_fecther, INTERNATIONAL_STATS_DATASET, start_time, "international stats")
    logger_url = 'http://covid.martinpolacek.eu/writeLog.php'
    app = App(international_dataset, local_dataset, vaccination_dataset, logger_url)
    app.run()

