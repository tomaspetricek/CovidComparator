import pandas as pd
import datetime
import requests
import io
from pathlib import Path
import threading
from pandas.util import hash_pandas_object
import numpy as np


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

        # keep only columns used in Dataset.COLUMN_NAMES
        data = data[["Date_reported", "Country", "New_cases", "Cumulative_cases"]]

        # rename columns based on Dataset.COLUMNS
        n_rows = data.shape[0]
        # data.insert(4, "vaccinations", pd.Series(n_rows * [None]))
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

        # print(data.iloc[0])
        # print(data.columns)
        # print(data.dtypes)

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


"""
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

        data = self.remove_data_before(data, 'date posted', from_date)

        return data
"""


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
        self.last_updated = None
        self.csv_filename = csv_filename
        self.date_from = date_from
        self.name = name
        self.hash = None
        self.today_updated = False

    def _combine_data(self, data):
        data = data.set_index(["date posted", "country"])
        self.data = self.data.set_index(["date posted", "country"])
        data_old = self.data.copy().reset_index()

        self.data = data.combine_first(self.data).reset_index()

        #df.loc[df['A']  != 2, 'B'] = new_val
        """
        for index, row in df.iterrows():
            date_posted = row[0]
            country = row[1]
            self.data.loc[date_posted, country][-1] = data_old.loc[date_posted, country][-1]
            print(self.data.loc[date_posted, country][-1])
            print(data_old.loc[date_posted, country][-1])
        """
        
        self.data = data_old.combine_first(self.data)

    def update(self):
        data = self.fetcher.fetch(self.date_from)
        # update whole data, because data can be changed after initial release

        self._combine_data(data)

        self.save()
        self.last_updated = datetime.datetime.now()
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
        else:
            self.today_updated = False


class StatsDataset(Dataset):
    COLUMN_NAMES = ["date posted", "country", "daily increase of infected", "total number of infected", "date loaded"]
    COLUMN_DTYPES = [datetime.datetime, str, int, int, datetime.datetime]


class VaccinationDataset(Dataset):
    COLUMN_NAMES = ["date posted", "country", "total vaccinations", "total vaccinations per 100", "date loaded"]
    COLUMN_DTYPES = [datetime.datetime, str, int, int, datetime.datetime]


if __name__ == "__main__":
    #MZCRStatsFetcher().fetch(None)
    #MZCRVaccinationFetcher().fetch(None)

    #WHOStatsFetcher().fetch(None)
    #WHOVaccinationFetcher().fetch(None)

    test_data = [[datetime.datetime(2020, 5, 17), "Czechia", 110, 1000, datetime.datetime(2020, 5, 17)], [datetime.datetime(2020, 5, 17), "Slovakia", 110, 1000, datetime.datetime(2020, 5, 17)],
       [datetime.datetime(2020, 3, 3), "Poland", 110, 1000, datetime.datetime(2020, 5, 17)], [datetime.datetime(2020, 5, 18), "Slovakia", 110, 2000, datetime.datetime(2020, 5, 17)]]
    df = pd.DataFrame(test_data, columns = VaccinationDataset.COLUMN_NAMES)

    test_data2 = [[datetime.datetime(2020, 5, 17), "Czechia", 110, 1000, datetime.datetime(2020, 6, 17)], [datetime.datetime(2020, 5, 17), "Slovakia", 110, 1000, datetime.datetime(2020, 6, 17)],
       [datetime.datetime(2020, 3, 3), "Poland", 110, 1000, datetime.datetime(2020, 6, 17)], [datetime.datetime(2020, 5, 18), "Slovakia", 130, 2000, datetime.datetime(2020, 6, 17)],
       [datetime.datetime(2020, 5, 19), "Slovakia", 130, 3000, datetime.datetime(2020, 6, 17)], [datetime.datetime(2020, 5, 20), "Slovakia", 140, 4000, datetime.datetime(2020, 6, 17)]]
    df2 = pd.DataFrame(test_data2, columns = VaccinationDataset.COLUMN_NAMES)

    #d = WHOVaccinationFetcher().fetch(datetime.datetime(2021,4,1))
    #xprint(d)

    vaccinationDataset = VaccinationDataset(None, None, datetime.datetime(2020,4,1), None)
    vaccinationDataset.data = df
    vaccinationDataset._combine_data(df2)
    print(df)
    print(df2)
    print(vaccinationDataset.data)

    

    """
    test_data = [[datetime.datetime(2020, 5, 17), "Czechia", 110], [datetime.datetime(2020, 5, 17), "Slovakia", 110],
       [datetime.datetime(2020, 3, 3), "Poland", 110], [datetime.datetime(2020, 5, 18), "Slovakia", 110]]
    df = pd.DataFrame(test_data, columns = StatsDataset.COLUMN_NAMES[:-2])

    test_data2 = [[datetime.datetime(2020, 5, 17), "Czechia", 110], [datetime.datetime(2020, 5, 17), "Slovakia", 110],
       [datetime.datetime(2020, 3, 3), "Poland", 110], [datetime.datetime(2020, 5, 18), "Slovakia", 130],
       [datetime.datetime(2020, 5, 19), "Slovakia", 130], [datetime.datetime(2020, 5, 20), "Slovakia", 140]]
    df2 = pd.DataFrame(test_data2, columns = StatsDataset.COLUMN_NAMES[:-2])

    #d = WHOVaccinationFetcher().fetch(datetime.datetime(2021,4,1))
    #xprint(d)

    statsDataset = StatsDataset(None, None, datetime.datetime(2020,4,1), None)
    statsDataset.data = df
    statsDataset._combine_data(df2)
    #print(statsDataset.data)
    """
