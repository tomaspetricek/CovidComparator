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

class Updater:
    """
    Takes care of updating app.
    """
    def __init__(self, datasets):
        self.datasets = datasets

    def update(self):
        for dataset in self.datasets:
            dataset.update()

    def run(self):
        pass

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