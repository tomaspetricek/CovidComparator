import datetime
import pandas as pd
import matplotlib.pyplot as plt
from data import WHOVaccinationFetcher


def transform(data):
    data = data.fillna(0)
    fig, ax = plt.subplots(nrows=1, ncols=1)

    for key, group in enumerate(data.groupby(["country"])):
        ax.scatter(group["date posted"], group["total vaccinations"], label=key)

    plt.legend(loc='best')
    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    test_data2 = [
        [datetime.datetime(2020, 1, 1), "Czechia", 110],
        [datetime.datetime(2020, 1, 2), "Slovakia", 110],
        [datetime.datetime(2020, 1, 2), "Poland", 110],
        [datetime.datetime(2020, 5, 18), "Slovakia", 130],
        [datetime.datetime(2020, 5, 19), "Slovakia", 130],
        [datetime.datetime(2020, 5, 20), "Slovakia", 140]
    ]

    df2 = pd.DataFrame(test_data2, columns=["date posted", "country", "total vaccinations"])

    data = WHOVaccinationFetcher().fetch(datetime.datetime(2020, 1, 1))

    transform(data)

