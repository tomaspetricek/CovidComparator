import pandas as pd
import datetime
import requests
import io

def get_csv(url, encoding="utf-8"):
    with requests.Session() as s:
        response = s.get(url)

    content = response.content.decode(encoding)
    return content

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
    def _fetch_vaccines(self):
        pass

    def _fetch_stats(self):
        # get data
        csv_url = "https://covid19.who.int/WHO-COVID-19-global-data.csv"
        content = get_csv(csv_url)
        data = pd.read_csv(io.StringIO(content))

        # keep only columns used in Dataset.COLUMN_NAMES
        data = data[["Date_reported", "Country", "New_cases", "Cumulative_cases"]]

        # rename columns based on Dataset.COLUMNS
        n_rows = data.shape[0]
        data.insert(4, "vaccinations", pd.Series(n_rows * [None]))
        data.insert(5, "date loaded",  pd.Series(n_rows * [datetime.datetime.now()]))
        data.columns = Dataset.COLUMN_NAMES

        # change columns dtypes based on Dataset.COLUMN_DTYPES
        data['date posted'] = pd.to_datetime(data['date posted'], format='%Y-%m-%d')

        return data

    def fetch(self, from_date):
        stats = self._fetch_stats()
        vaccines = self._fetch_vaccines()
        return data


class MZCRFetcher(DataFetcher):
    def fetch(self, from_date):
        # get data
        csv_url = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/zakladni-prehled.csv"
        content = get_csv(csv_url)
        data = pd.read_csv(io.StringIO(content))

        # keep only columns used in Dataset.COLUMN_NAMES
        data = data[["datum", "potvrzene_pripady_vcerejsi_den", "potvrzene_pripady_celkem", "vykazana_ockovani_celkem"]]

        # rename columns based on Dataset.COLUMNS
        n_rows = data.shape[0]
        data.insert(1, "country",  pd.Series(n_rows * ["Czechia"]))
        data.insert(5, "date loaded",  pd.Series(n_rows * [datetime.datetime.now()]))
        data.columns = Dataset.COLUMN_NAMES
        # change columns dtypes based on Dataset.COLUMN_DTYPES
        data['date posted'] = pd.to_datetime(data['date posted'], format='%Y-%m-%d')
        
        #print(data.iloc[0])
        #print(data.columns)
        #print(data.dtypes)


        # remove data before from_date

        return data

class Dataset:
    """
    Stores data and makes available.
    """
    COLUMN_NAMES = ["date posted", "country", "daily increase of infected", "total number of infected", "total vaccinations", "date loaded"]
    COLUMN_DTYPES = [datetime.datetime, str, int, int, int, datetime.datetime]

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
        # update whole data, because data can be changed after initial release
        ...

    def load(self):
        self.fetcher.fetch(...)

    def save(self):
        pass


if __name__ == "__main__":
    #MZCRFetcher().fetch(None)
    WHOFetcher().fetch(None)
