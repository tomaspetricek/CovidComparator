import pandas as pd
import datetime
import requests
import io


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
        # update whole data, because data can be changed after initial release
        ...

    def load(self):
        self.fetcher.fetch(...)

    def save(self):
        pass