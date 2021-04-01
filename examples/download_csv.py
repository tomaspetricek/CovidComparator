import requests
import io
import pandas as pd
import datetime


def get_csv(url, encoding="utf-8"):
    with requests.Session() as s:
        response = s.get(url)

    content = response.content.decode(encoding)
    return content

def send_request_api(url):
    pass

def main():
    csv_url = "https://covid19.who.int/WHO-COVID-19-global-data.csv"
    content = get_csv(csv_url)

    data = pd.read_csv(io.StringIO(content))

    print(data)
    print(data.columns)
    print(data.dtypes)
    print(type(data["Date_reported"][0]))
    print(data.iloc[[0]])


if __name__ == '__main__':
    main()
