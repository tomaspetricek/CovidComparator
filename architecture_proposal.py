import threading

# data.py
class DataFetcher:
    """
    Fetches data from specified data source.
    """
    def fetch(self, from_date):
        pass

class Dataset:
    """
    Stores data and makes available.
    """
    COLUMNS = ["date posted", "country", "daily increase of infected", "total number of infected"]

    def __init__(self, fetcher):
        """

        :param fetcher: DataFetcher
        :param data: pd.DataFrame
        """
        self.fetcher = fetcher
        self.data = None

    def update(self):
        self.fetcher.fetch()
        ...

    def load(self):
        pass

    def save(self):
        pass

# app.py
class Updater:
    """
    Takes care of updating app.
    """
    UPDATE_FREQUENCY = 15 * 60  # waiting time

    def __init__(self, datasets):
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
        self.updater = Updater()
        self.active_frame = ...

    def load(self):
        pass

    def run(self):
        self.load()
        self.updater.run()

# frames.py
class Frame:
    def load(self):
        pass

    def refresh(self):
        pass

class Main(Frame):
    pass

class VaccinationOverview(Frame):
    pass

class DatasetIntegrityOverview(Frame):
    pass

class IntegrityComparator:
    pass

class VaccinationComparator:
    pass

# components.py
class Component:
    def __init__(self, parent_widget):
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