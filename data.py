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

    def remove_data_before(self, data, column_name, date_from):
        index_names = data[ data[column_name] < date_from ].index
        data.drop(index_names, inplace = True)
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
        data.insert(4, "date loaded",  pd.Series(n_rows * [datetime.datetime.now()]))
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
        data.insert(1, "country",  pd.Series(n_rows * ["Czechia"]))
        data.insert(4, "date loaded",  pd.Series(n_rows * [datetime.datetime.now()]))
        data.columns = StatsDataset.COLUMN_NAMES
        # change columns dtypes based on Dataset.COLUMN_DTYPES
        data['date posted'] = pd.to_datetime(data['date posted'], format='%Y-%m-%d')
        
        #print(data.iloc[0])
        #print(data.columns)
        #print(data.dtypes)


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
        data = data[["DATE_UPDATED", "COUNTRY", "TOTAL_VACCINATIONS"]]

        # rename columns based on Dataset.COLUMNS
        n_rows = data.shape[0]
        data.insert(3, "date loaded",  pd.Series(n_rows * [datetime.datetime.now()]))
        data.columns = VaccinationDataset.COLUMN_NAMES

        # change columns dtypes based on Dataset.COLUMN_DTYPES
        data['date posted'] = pd.to_datetime(data['date posted'], format='%Y-%m-%d')

        data = self.remove_data_before(data, 'date posted', from_date)

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

        data = self.remove_data_before(data, 'date posted', from_date)

        return data

class Dataset:
    """
    Stores data and makes available.
    """
    COLUMN_NAMES = None
    COLUMN_DTYPES = None

    def __init__(self, fetcher, csv_filename, date_from):
        """

        :param fetcher: DataFetcher
        :param data: pd.DataFrame
        """
        self.fetcher = fetcher
        self.data = None
        self.last_updated = None
        self.csv_filename = csv_filename
        self.date_from = date_from

    def _combine_data(self, data):
        data = data.set_index(["date posted", "country"])
        self.data = self.data.set_index(["date posted", "country"])

        self.data = data.combine_first(self.data).reset_index()

    def update(self):
        data = self.fetcher.fetch(self.date_from)
        # update whole data, because data can be changed after initial release

        self._combine_data(data)

        self.save()
        self.last_updated = datetime.datetime.now()

    def load(self):
        if Path(self.csv_filename).is_file():
            # file exists
            self.data = pd.read_csv(self.csv_filename)
            self.date_from = min(self.data["date posted"])
        
        self.update()


    def save(self):
        self.data.to_csv(self.csv_filename, index=False)

class StatsDataset(Dataset):
    COLUMN_NAMES = ["date posted", "country", "daily increase of infected", "total number of infected", "date loaded"]
    COLUMN_DTYPES = [datetime.datetime, str, int, int, datetime.datetime]


class VaccinationDataset(Dataset):
    COLUMN_NAMES = ["date posted", "country", "total vaccinations", "date loaded"]
    COLUMN_DTYPES = [datetime.datetime, str, int, datetime.datetime]


if __name__ == "__main__":
    #MZCRStatsFetcher().fetch(None)
    #MZCRVaccinationFetcher().fetch(None)

    #WHOStatsFetcher().fetch(None)
    #WHOVaccinationFetcher().fetch(None)

    test_data = [[datetime.datetime(2020, 5, 17), "Czechia", 110], [datetime.datetime(2020, 5, 17), "Slovakia", 110],
       [datetime.datetime(2020, 3, 3), "Poland", 110], [datetime.datetime(2020, 5, 18), "Slovakia", 110]]
    df = pd.DataFrame(test_data, columns = VaccinationDataset.COLUMN_NAMES[:-1])

    test_data2 = [[datetime.datetime(2020, 5, 17), "Czechia", 110], [datetime.datetime(2020, 5, 17), "Slovakia", 110],
       [datetime.datetime(2020, 3, 3), "Poland", 110], [datetime.datetime(2020, 5, 18), "Slovakia", 130],
       [datetime.datetime(2020, 5, 19), "Slovakia", 130], [datetime.datetime(2020, 5, 20), "Slovakia", 140]]
    df2 = pd.DataFrame(test_data2, columns = VaccinationDataset.COLUMN_NAMES[:-1])

    #d = WHOVaccinationFetcher().fetch(datetime.datetime(2021,4,1))
    #xprint(d)

    vaccinationDataset = VaccinationDataset(None, None, datetime.datetime(2020,4,1))
    vaccinationDataset.data = df
    vaccinationDataset._combine_data(df2)
    print(vaccinationDataset.data)

    


    test_data = [[datetime.datetime(2020, 5, 17), "Czechia", 110], [datetime.datetime(2020, 5, 17), "Slovakia", 110],
       [datetime.datetime(2020, 3, 3), "Poland", 110], [datetime.datetime(2020, 5, 18), "Slovakia", 110]]
    df = pd.DataFrame(test_data, columns = StatsDataset.COLUMN_NAMES[:-2])

    test_data2 = [[datetime.datetime(2020, 5, 17), "Czechia", 110], [datetime.datetime(2020, 5, 17), "Slovakia", 110],
       [datetime.datetime(2020, 3, 3), "Poland", 110], [datetime.datetime(2020, 5, 18), "Slovakia", 130],
       [datetime.datetime(2020, 5, 19), "Slovakia", 130], [datetime.datetime(2020, 5, 20), "Slovakia", 140]]
    df2 = pd.DataFrame(test_data2, columns = StatsDataset.COLUMN_NAMES[:-2])

    #d = WHOVaccinationFetcher().fetch(datetime.datetime(2021,4,1))
    #xprint(d)

    statsDataset = StatsDataset(None, None, datetime.datetime(2020,4,1))
    statsDataset.data = df
    statsDataset._combine_data(df2)
    print(statsDataset.data)
