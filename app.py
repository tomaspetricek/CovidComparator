import threading


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


class App:
    def __init__(self, international_dataset, local_dataset):
        self.international_dataset = international_dataset
        self.local_dataset = local_dataset
        self.countries = ...
        self.updater = ...  # Updater()
        self.frame = ...
        self.controllers = ...
        self.viewer = ...

    def load(self):
        """
        Load in data.
        """
        self.international_dataset.load()
        self.local_dataset.load()

    def run(self):
        self.load()
        self.updater.run()


class Viewer:
    """
    Switches between views.
    """

    def __init__(self, views, app):
        self.views = views
        self.app = app
        self.active_view = ...

    def show_view(self, view):
        pass

    def update(self):
        pass