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
        self.datasets = datasets

    def update(self, dataset):
        dataset.update()

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
        self.updater = ... # Updater()
        self.frame = ...
        self.views = ...
        self.active_view = ...

    def load(self):
        """
        Load in data.
        """
        self.international_dataset.load()
        self.local_dataset.load()

    def show_view(self, view):
        pass

    def refresh(self):
        self.active_view.refresh()

    def run(self):
        self.load()
        self.updater.run()

# views.py
class View:
    def __init__(self, app):
        pass

    def load(self):
        pass

    def refresh(self):
        pass

class Main(View):
    def __init__(self, app):
        super().__init__(app)
        self.navigation = ...

class VaccinationOverview(View):
    def __init__(self, app, dataset):
        super().__init__(app)
        self.dataset = dataset  # international dataset in our case
        self.navigation = ...
        self.graph = ...
        self.search_bar = ...
    pass

class DatasetIntegrityOverview(View):
    def __init__(self, app):
        super().__init__(app)
        self.navigation = ...
        self.state = ...
        self.table = ...
    pass

class IntegrityComparator:
    pass

class VaccinationComparator:
    pass

# components.py
class Component:
    def __init__(self, parent):
        pass

class AutocompleteSearchBar:
    pass

class Graph:
    """
    Inspiration: https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/
    """
    pass

class Table:
    """
    Inspiration: https://www.geeksforgeeks.org/create-table-using-tkinter/
    """
    pass

# Menu - https://www.youtube.com/watch?v=ZS2_v_zsPTg

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