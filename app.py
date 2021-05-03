import threading
import tkinter as tk
from tkinter import ttk
from controllers import MainController, VaccinationController, DatasetIntegrityController
from utils import Logger, connected_to_internet
import socket
import datetime
import time
from data import *
from config import *
import requests
import queue

START_TIME = datetime.datetime.now()    # datetime.datetime(2021, 4, 1)
START_TIME = START_TIME.replace(hour=0, minute=0, second=0, microsecond=0)


class Updater:
    """
    Takes care of updating app.
    """
    UPDATE_FREQUENCY = 15 * 60 # waiting time
    DATASET_LOCK = threading.Lock()

    def __init__(self, app, datasets, controllers):
        self.app = app
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
        if connected_to_internet():
            self._update_datasets()
        self.app.callback_queue.put(self._update_controllers)

    def _keep_running(self):
        # put into callback_queue so it can be called from the main thread
        self.app.callback_queue.put(self.update)
        time_ = self.UPDATE_FREQUENCY

        today = datetime.datetime.today()
        today = today.replace(hour=0, minute=0, second=0, microsecond=0)

        if self._check_datasets_up_to_date() and START_TIME != today:
            time_ = self.seconds_until_midnight()

        self.timer = threading.Timer(time_, self._keep_running)
        self.timer.start()

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

    def stop(self):
        if self.DATASET_LOCK.locked():
            self.DATASET_LOCK.release()

        self.timer.cancel()


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
        self.start_time = START_TIME
        self.title(self.NAME)
        self.frame = None
        self.view_classes = self.CONTROLLER_CLASSES
        self.controllers = self.CONTROLLER_CLASSES
        self.viewer = Viewer(self.controllers, MainController.VIEW_CLASS)
        self.minsize(width=self.MIN_WIDTH, height=self.MIN_HEIGHT)
        self.updater = Updater(self, [self.international_dataset, self.vaccination_dataset, self.local_dataset],
                               self.controllers)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.callback_queue = queue.Queue()

    def on_close(self):
        self.updater.stop()
        self.destroy()

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

    def _keep_checking_for_callbacks(self):
        try:
            callback = self.callback_queue.get(False)  # doesn't block
        except queue.Empty:  # raised when queue is empty
            pass
        else:
            if callback:
                callback()

        self.after(10000, self._keep_checking_for_callbacks)  # Every 10 sec

    def run(self):
        self.updater.run()
        self.viewer.show_view()
        self._keep_checking_for_callbacks()
        self.after(1, self._keep_checking_for_callbacks)
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


def main():
    # logger.send_info("Aplikace spuštěna na " + str(socket.gethostname()))

    fetcher = WHOVaccinationFetcher()
    mzcr_fetcher = MZCRStatsFetcher()
    who_fecther = WHOStatsFetcher()

    vaccination_dataset = VaccinationDataset(fetcher, VACCINATION_DATASET, START_TIME, "WHO vaccinations")
    local_dataset = StatsDataset(mzcr_fetcher, LOCAL_STATS_DATASET, START_TIME, "MZČR stats")
    international_dataset = StatsDataset(who_fecther, INTERNATIONAL_STATS_DATASET, START_TIME, "WHO stats")
    logger_url = 'http://covid.martinpolacek.eu/writeLog.php'
    app = App(international_dataset, local_dataset, vaccination_dataset, logger_url)
    app.run()


if __name__ == '__main__':
    main()
