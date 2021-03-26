import requests
import csv


def get_csv(url, encoding="utf-8"):
    delimiter = ","

    with requests.Session() as s:
        response = s.get(url)

    content = response.content.decode(encoding)

    reader = csv.reader(content.splitlines(), delimiter=delimiter)
    lines = list(reader)

    return lines

def send_request_api(url):
    pass

def main():
    csv_url = "https://covid19.who.int/WHO-COVID-19-global-data.csv"
    lines = get_csv(csv_url)

    for line in lines:
        print(line)

    print("number of lines: ", len(lines))


if __name__ == '__main__':
    main()
