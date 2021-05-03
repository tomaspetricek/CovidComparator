import pandas as pd
import datetime
import requests
import io
from pathlib import Path
import threading
from pandas.util import hash_pandas_object
from utils import connected_to_internet


def get_csv(url, encoding="utf-8"):
    with requests.Session() as s:
        response = s.get(url)

    content = response.content.decode(encoding)

    return content


class DataFetcher:
    """
    Fetches data from specified data source.
    """
    URL = None

    def fetch(self, from_date):
        """
        :param from_date: datetime
        :return: pd.DataFrame columns specified in Dataset
        """
        pass

    def remove_data_before(self, data, column_name, date_from):
        index_names = data[data[column_name] < date_from].index
        data.drop(index_names, inplace=True)
        return data


class WHOStatsFetcher(DataFetcher):
    URL = "https://covid19.who.int/WHO-COVID-19-global-data.csv"

    def fetch(self, from_date):
        # get data

        csv_url = self.URL
        content = get_csv(csv_url)
        data = pd.read_csv(io.StringIO(content))

        data = data.loc[data['Country'] == "Czechia"]

        # keep only columns used in Dataset.COLUMN_NAMES
        data = data[["Date_reported", "Country", "New_cases", "Cumulative_cases"]]

        # rename columns based on Dataset.COLUMNS
        n_rows = data.shape[0]
        data.insert(4, "date loaded", pd.Series(n_rows * [datetime.datetime.now()]))
        data.columns = StatsDataset.COLUMN_NAMES

        # change columns dtypes based on Dataset.COLUMN_DTYPES
        data['date posted'] = pd.to_datetime(data['date posted'], format='%Y-%m-%d')

        data = self.remove_data_before(data, 'date posted', from_date)

        return data


class MZCRStatsFetcher(DataFetcher):
    URL = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/zakladni-prehled.csv"

    def fetch(self, from_date):
        # get data
        csv_url = self.URL
        content = get_csv(csv_url)
        data = pd.read_csv(io.StringIO(content))

        # keep only columns used in Dataset.COLUMN_NAMES
        data = data[["datum", "potvrzene_pripady_vcerejsi_den", "potvrzene_pripady_celkem"]]

        # rename columns based on Dataset.COLUMNS
        n_rows = data.shape[0]
        data.insert(1, "country", pd.Series(n_rows * ["Czechia"]))
        data.insert(4, "date loaded", pd.Series(n_rows * [datetime.datetime.now()]))
        data.columns = StatsDataset.COLUMN_NAMES

        # change columns dtypes based on Dataset.COLUMN_DTYPES
        data['date posted'] = pd.to_datetime(data['date posted'], format='%Y-%m-%d')

        # remove data before from_date
        data = self.remove_data_before(data, 'date posted', from_date)

        return data


class WHOVaccinationFetcher(DataFetcher):
    URL = "https://covid19.who.int/who-data/vaccination-data.csv"

    def fetch(self, from_date):
        # get data
        csv_url = self.URL
        content = get_csv(csv_url)
        data = pd.read_csv(io.StringIO(content))

        # keep only columns used in Dataset.COLUMN_NAMES
        data = data[["DATE_UPDATED", "COUNTRY", "TOTAL_VACCINATIONS", "TOTAL_VACCINATIONS_PER100"]]

        # rename columns based on Dataset.COLUMNS
        n_rows = data.shape[0]
        data.insert(4, "date loaded", pd.Series(n_rows * [datetime.datetime.now()]))
        data.columns = VaccinationDataset.COLUMN_NAMES

        # change columns dtypes based on Dataset.COLUMN_DTYPES
        data['date posted'] = pd.to_datetime(data['date posted'], format='%Y-%m-%d')

        data = self.remove_data_before(data, 'date posted', from_date)

        return data


class Dataset:
    """
    Stores data and makes available.
    """
    COLUMN_NAMES = None
    COLUMN_DTYPES = None

    def __init__(self, fetcher, csv_filename, date_from, name):
        """

        :param fetcher: DataFetcher
        :param data: pd.DataFrame
        """
        self.fetcher = fetcher
        self.data = pd.DataFrame(columns=self.COLUMN_NAMES)
        self.last_fetched = None
        self.last_updated = None
        self.csv_filename = csv_filename
        self.date_from = date_from
        self.name = name
        self.hash = None
        self.today_updated = False

    def _retain_first_loaded(self, old_data):
        cols = list(self.data.columns)
        date_loaded_col_idx = cols.index("date loaded")

        # change back to old index if did not change
        for index, row in self.data.iterrows():
            date_posted, country = index

            # check if index in old data
            if index in old_data.index:
                old_row = list(old_data.loc[date_posted, country])
                new_row = list(row)

                # check if values have changed
                if old_row[:-1] == new_row[:-1]:
                    self.data.loc[index, "date loaded"] = old_data.loc[date_posted, country][date_loaded_col_idx]

    def _combine_data(self, data):
        data = data.set_index(["date posted", "country"])
        self.data = self.data.set_index(["date posted", "country"])
        old_data = self.data.copy()

        self.data = data.combine_first(self.data)

        if not old_data.empty:
            self._retain_first_loaded(old_data)

        self.data.reset_index(inplace=True)

    def update(self):
        if connected_to_internet():
            data = self.fetcher.fetch(self.date_from)
            # update whole data, because data can be changed after initial release

            data.dropna(axis=0, how='any', inplace=True)

            self._combine_data(data)

            self.save()
            self.last_fetched = datetime.datetime.now()
            self.check_up_to_date()

    def load(self):
        if Path(self.csv_filename).is_file():
            # file exists
            self.data = pd.read_csv(self.csv_filename)

            if not self.data.empty:
                self.data['date posted'] = pd.to_datetime(self.data['date posted'], format='%Y-%m-%d')
                self.date_from = min(self.data["date posted"])
                self.data['date loaded'] = pd.to_datetime(self.data['date loaded'], format='%Y-%m-%d %H:%M:%S.%f')

        self.update()

    def save(self):
        kwargs = {
            "path_or_buf": self.csv_filename,
            "index": False,
        }
        thread = threading.Thread(target=self.data.to_csv, kwargs=kwargs)
        thread.start()

    def check_up_to_date(self):
        new_hash = hash_pandas_object(self.data).sum()

        if new_hash != self.hash:
            self.today_updated = True
            self.hash = new_hash

            if not self.data.empty:
                self.last_updated = self.data["date loaded"].max()
            else:
                self.last_updated = None
        else:
            self.today_updated = False


class StatsDataset(Dataset):
    COLUMN_NAMES = ["date posted", "country", "daily increase of infected", "total number of infected", "date loaded"]
    COLUMN_DTYPES = [datetime.datetime, str, int, int, datetime.datetime]


class VaccinationDataset(Dataset):
    COLUMN_NAMES = ["date posted", "country", "total vaccinations", "total vaccinations per 100", "date loaded"]
    COLUMN_DTYPES = [datetime.datetime, str, int, int, datetime.datetime]
