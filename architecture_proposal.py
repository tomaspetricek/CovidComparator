import threading
import datetime


# data.py
class DataFetcher:
    """
    Fetches data from specified data source.
    """

    def fetch(self, from_date):
        """
        :param from_date: datetime
        :return: pd.DataFrame columns specified in Dataset
        """
        # get data
        # keep only columns used in Dataset.COLUMN_NAMES
        # rename columns based on Dataset.COLUMNS
        # change columns dtypes based on Dataset.COLUMN_DTYPES
        # remove data before from_date
        pass


class WHOFetcher(DataFetcher):
    def fetch(self, from_date):
        pass


class MZCRFetcher(DataFetcher):
    def fetch(self, from_date):
        pass


class Dataset:
    """
    Stores data and makes available.
    """
    COLUMN_NAMES = ["date posted", "country", "daily increase of infected", "total number of infected"]
    COLUMN_DTYPES = [datetime.datetime, str, int, int]

    def __init__(self, fetcher):
        """

        :param fetcher: DataFetcher
        :param data: pd.DataFrame
        """
        self.fetcher = fetcher
        self.data = ...
        self.last_updated = ...

    def update(self):
        self.fetcher.fetch(...)
        ...

    def load(self):
        self.fetcher.fetch(...)

    def save(self):
        pass


# app.py
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
    Switches views.
    """

    def __init__(self, views, app):
        self.views = views
        self.app = app
        self.active_view = ...

    def show_view(self):
        pass

    def update(self):
        pass


# controllers.py
class Controller:
    """
    Handles logic for view.
    """

    def __init__(self, app):
        self.app = app
        self.view = None
        self.navigation_callbacks = ...

    def set_navigation_callbacks(self, value):
        self._navigation_callbacks = []

        # create call backs for all views except this one
        for view in self.app.views:
            if view != self:
                callback = lambda: self.app.show_view(view)
                self._navigation_callbacks.append(callback)

    def get_navigation_callbacks(self):
        return self._navigation_callbacks

    navigation_callbacks = property(get_navigation_callbacks, set_navigation_callbacks)

    def update(self):
        """
        Updates data for view.
        """
        pass


class DatasetIntegrityController(Controller):
    def __init__(self, app):
        super().__init__(app)
        self.overview = ...
        self.status = ...
        self.view = DatasetIntegrityOverview(app, self)

    def update(self):
        self.status = ...
        # update overview based on new data
        self.view.update()
        pass


class VaccinationController(Controller):
    def __init__(self, app):
        super().__init__(app)
        self.overview = ...
        self.selected_countries = ...
        self.status = ...
        self.view = VaccinationOverview(app, self)

    def add_country(self, country):
        # add country to selected countries
        # update graph
        pass

    def remove_country(self, country):
        # remove country from selected countries
        # update graph
        pass

    def update(self):
        self.status = ...
        # update overview based on new data
        self.view.update()
        pass

# MVC - Tkinter
# https://sukhbinder.wordpress.com/2014/12/25/an-example-of-model-view-controller-design-pattern-with-tkinter-python/
# views.py
class View:
    """
    Represents visual part of app.
    Works with data provided by controller
    """

    def __init__(self, parent, controller):
        self.controller = controller
        pass

    def update(self):
        pass


class Main(View):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.navigation = ...


class VaccinationOverview(View):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.navigation = ...
        self.graph = ...
        self.search_bar = ...

    def update(self):
        pass


class DatasetIntegrityOverview(View):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.navigation = ...
        self.state = ...
        self.table = ...

    def update(self):
        pass


class IntegrityComparator:
    pass


class VaccinationComparator:
    pass


# components.py
class Component:
    def __init__(self, parent):
        pass


class AutocompleteSearchBar(Component):
    pass


class Graph(Component):
    """
    Inspiration: j
    """
    pass


class Table(Component):
    """
    Inspiration: https://www.geeksforgeeks.org/create-table-using-tkinter/
    """
    pass


class Navigation(Component):
    pass
    # Menu - https://www.youtube.com/watch?v=ZS2_v_zsPTg


# logging.py
class Logger:
    def __init__(self, url):
        pass

    def send_info(self, message):
        pass

    def send_error(self, message):
        pass

    def send_warning(self, message):
        pass

    def _send(self, type_, message):
        pass
