import pandas as pd
import datetime
import requests
import io
import csv
from pathlib import Path

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

    # def _process(self, data):
    # def _get_data(self):

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


class WHOStatsFetcher(DataFetcher):
    URL = "https://covid19.who.int/WHO-COVID-19-global-data.csv"

    def _fetch_stats(self):
        # get data
        csv_url = self.URL
        content = get_csv(csv_url)
        data = pd.read_csv(io.StringIO(content))

        # keep only columns used in Dataset.COLUMN_NAMES
        data = data[["Date_reported", "Country", "New_cases", "Cumulative_cases"]]

        # rename columns based on Dataset.COLUMNS
        n_rows = data.shape[0]
        # data.insert(4, "vaccinations", pd.Series(n_rows * [None]))
        data.insert(4, "date loaded",  pd.Series(n_rows * [datetime.datetime.now()]))
        data.columns = StatsDataset.COLUMN_NAMES

        # change columns dtypes based on Dataset.COLUMN_DTYPES
        data['date posted'] = pd.to_datetime(data['date posted'], format='%Y-%m-%d')

        return data

    def fetch(self, from_date):
        stats = self._fetch_stats()
        return stats


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
        data.insert(1, "country",  pd.Series(n_rows * ["Czechia"]))
        data.insert(4, "date loaded",  pd.Series(n_rows * [datetime.datetime.now()]))
        data.columns = StatsDataset.COLUMN_NAMES
        # change columns dtypes based on Dataset.COLUMN_DTYPES
        data['date posted'] = pd.to_datetime(data['date posted'], format='%Y-%m-%d')
        
        #print(data.iloc[0])
        #print(data.columns)
        #print(data.dtypes)


        # remove data before from_date

        return data

class WHOVaccinationFetcher(DataFetcher):
    URL = "https://covid19.who.int/who-data/vaccination-data.csv"

    def fetch(self, from_date):
        # get data
        csv_url = self.URL
        content = get_csv(csv_url)
        data = pd.read_csv(io.StringIO(content))

        # keep only columns used in Dataset.COLUMN_NAMES
        data = data[["DATE_UPDATED", "COUNTRY", "TOTAL_VACCINATIONS"]]

        # rename columns based on Dataset.COLUMNS
        n_rows = data.shape[0]
        data.insert(3, "date loaded",  pd.Series(n_rows * [datetime.datetime.now()]))
        data.columns = VaccinationDataset.COLUMN_NAMES

        # change columns dtypes based on Dataset.COLUMN_DTYPES
        data['date posted'] = pd.to_datetime(data['date posted'], format='%Y-%m-%d')

        return data

class MZCRVaccinationFetcher(DataFetcher):
    URL = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/zakladni-prehled.csv"

    def fetch(self, from_date):
        # get data
        csv_url = self.URL
        content = get_csv(csv_url)
        data = pd.read_csv(io.StringIO(content))

        # keep only columns used in Dataset.COLUMN_NAMES
        data = data[["datum", "vykazana_ockovani_celkem"]]

        # rename columns based on Dataset.COLUMNS
        n_rows = data.shape[0]
        data.insert(1, "country",  pd.Series(n_rows * ["Czechia"]))
        data.insert(3, "date loaded",  pd.Series(n_rows * [datetime.datetime.now()]))
        data.columns = VaccinationDataset.COLUMN_NAMES
        # change columns dtypes based on Dataset.COLUMN_DTYPES
        data['date posted'] = pd.to_datetime(data['date posted'], format='%Y-%m-%d')


        return data

class Dataset:
    """
    Stores data and makes available.
    """
    COLUMN_NAMES = None
    COLUMN_DTYPES = None

    def __init__(self, fetcher, csv_filename):
        """

        :param fetcher: DataFetcher
        :param data: pd.DataFrame
        """
        self.fetcher = fetcher
        self.data = ...
        self.last_updated = ...
        self.csv_filename = csv_filename

    def update(self):
        # add all data that are different and change old ones
        # - some data can be changed after initial value was placed
        pass

    def load(self):
        # check if there are csv files in home directory if so load them
        # fetch new data
        # save whole dataset rewriting old one
        # self.save
        pass

    def save(self):
        # rewrite old csv file
        pass

class StatsDataset(Dataset):
    COLUMN_NAMES = ["date posted", "country", "daily increase of infected", "total number of infected", "date loaded"]
    COLUMN_DTYPES = [datetime.datetime, str, int, int, datetime.datetime]

    def __init__(self, fetcher):
        super().__init__(fetcher)
        pass

    def update(self):
        self.fetcher.fetch(...)
        # update whole data, because data can be changed after initial release
        ...

    def load(self):
        if Path(self.csv_filename).is_file():
            # file exists
            self.data = pd.read_csv(self.csv_filename)
        
        self.fetcher.fetch(...)


        self.save()

    def save(self):
        self.data.to_csv(self.csv_filename, index=False)


class VaccinationDataset(Dataset):
    COLUMN_NAMES = ["date posted", "country", "total vaccinations", "date loaded"]
    COLUMN_DTYPES = [datetime.datetime, str, int, datetime.datetime]

    def __init__(self, fetcher):
        super().__init__(fetcher)
        pass

    def update(self):
        self.fetcher.fetch(...)
        # update whole data, because data can be changed after initial release
        ...

    def load(self):
        self.fetcher.fetch(...)


        self.save()

    def save(self):
        self.data.to_csv(self.csv_filename, index=False)


if __name__ == "__main__":
    #MZCRStatsFetcher().fetch(None)
    #MZCRVaccinationFetcher().fetch(None)

    WHOStatsFetcher().fetch(None)
    WHOVaccinationFetcher().fetch(None)
