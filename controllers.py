from views import *
from data import *
import matplotlib.pyplot as plt
import pandas as pd


class Controller:
    """
    Handles logic for view.
    """
    VIEW_CLASS = None

    def __init__(self, app):
        self.app = app
        self.view = None

    def update(self):
        """
        Updates data for view.
        """
        pass

    def show_view(self, context):
        self.app.viewer.show_view(context)

    def update_app(self):
        self.app.updater.update()

    def format_date(self, date, hours):
        if date is None:
            return "Cannot connect to internet."
        if hours:
            return date.strftime("%d-%m-%Y %H:%M")
        return date.strftime("%d-%m-%y")

    def format_delta_time(self, delta):
        hours, remainder = divmod(abs(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        return "{:02d}:{:02d}:{:02d}".format(int(hours), int(minutes), int(round(seconds)))


class MainController(Controller):
    VIEW_CLASS = MainView

    def __init__(self, app):
        super().__init__(app)
        self.view = self.VIEW_CLASS(app.frame, self)


class DatasetIntegrityController(Controller):
    VIEW_CLASS = DatasetIntegrityView

    def __init__(self, app):
        super().__init__(app)
        self.status = self.app.international_dataset, self.app.local_dataset
        self.overview = self.app.international_dataset, self.app.local_dataset
        self.view = self.VIEW_CLASS(app.frame, self)

    def get_overview(self):
        return self._overview

    def set_overview(self, value):
        international_dataset, local_dataset = value

        filtered_international_dataset = international_dataset.data.loc[
            international_dataset.data["country"] == "Czechia"]
        filtered_international_dataset = filtered_international_dataset.dropna(how='any', axis=0)

        merged_dataset = pd.merge(filtered_international_dataset, local_dataset.data, on='date posted')
        merged_dataset = merged_dataset.dropna(how='any', axis=0)

        diff_daily_infected = merged_dataset["daily increase of infected_x"] - merged_dataset[
            "daily increase of infected_y"]
        diff_total_infected = merged_dataset["total number of infected_x"] - merged_dataset[
            "total number of infected_y"]

        diff_date_posted = pd.to_datetime(merged_dataset["date loaded_x"]) - pd.to_datetime(merged_dataset["date loaded_y"])
        diff_date_posted_formated = list()

        for dat in diff_date_posted:
            diff_date_posted_formated.append(self.format_delta_time(dat))

        data = {
            "date posted": merged_dataset["date posted"],
            "difference daily increase of infected": diff_daily_infected,
            "difference total number of infected": diff_total_infected,
            "difference time loaded": diff_date_posted_formated
        }

        self._overview = pd.DataFrame(data)
        self._overview.dropna(inplace=True)

    overview = property(get_overview, set_overview)

    def set_status(self, value):
        datasets = value

        self._status = {}

        dataset_key = " last updated:"

        for dataset in datasets:
            last_updated = dataset.last_updated

            if last_updated:
                last_updated = self.format_date(dataset.last_updated, True)
            else:
                last_updated = "No data available"

            self._status[dataset.name + dataset_key] = last_updated

        self._status["Last update attempt:"] = self.format_date(dataset.last_fetched, True)

    def get_status(self):
        return self._status

    status = property(get_status, set_status)

    def update(self):
        self.status = self.app.international_dataset, self.app.local_dataset

        # update overview based on new data
        self.overview = self.app.international_dataset, self.app.local_dataset

        self.view.update()


class VaccinationController(Controller):
    VIEW_CLASS = VaccinationView
    MAX_COUNTRIES_SELECTED = 4

    def __init__(self, app):
        super().__init__(app)
        self.overview = self.app.vaccination_dataset.data
        self.selectable_countries = list(self.app.vaccination_dataset.data["country"].unique())
        self.selected_countries = []
        self.status = self.app.vaccination_dataset
        self._figure = None
        self.figure = self._overview
        self.view = self.VIEW_CLASS(app.frame, self)

    def get_overview(self):
        return self._overview

    def set_overview(self, value):
        vaccination_dataset = value
        self._overview = vaccination_dataset[["date posted", "country", "total vaccinations per 100"]]
        self._overview = self._overview.fillna(0)

    overview = property(get_overview, set_overview)

    def set_figure(self, value):
        if not self._figure:
            self._figure, self._ax = plt.subplots(nrows=1, ncols=1)

        self._ax.clear()

        # pick only countries from selected_countries and Czechia always
        try:
            for country, group in self._overview.groupby(["country"]):
                if country in self.selected_countries or country == "Czechia":
                    self._ax.scatter(group["date posted"], group["total vaccinations per 100"], label=country)
        except (KeyError, AttributeError) as err:
            self.app.logger.send_error("Nelze na????st spr??vn?? data pro graf: " + str(err))

        plt.legend(loc='best')
        self._ax.set_xlabel("Date posted")
        self._ax.set_ylabel("Total vaccinations per 100")
        self._ax.tick_params(axis='x', rotation=45)
        # ax.set_title("")
        self._figure.tight_layout()

    def get_figure(self):
        return self._figure

    figure = property(get_figure, set_figure)

    def add_country(self, country):
        # add country to selected countries
        if country in self.selectable_countries and len(self.selected_countries) < self.MAX_COUNTRIES_SELECTED:
            self.selected_countries.append(country)
            self.selectable_countries.remove(country)

        self.figure = self._overview

        # update graph
        self.view.update()

    def remove_country(self, country):
        # remove country from selected countries
        if country in self.selected_countries:
            self.selected_countries.remove(country)
            self.selectable_countries.append(country)

        self.figure = self._overview

        # update graph
        self.view.update()

    def get_status(self):
        return self._status

    def set_status(self, value):
        dataset = value
        self._status = {}
        dataset_key = " last updated:"

        last_updated = dataset.last_updated

        if last_updated:
            last_updated = self.format_date(dataset.last_updated, True)
        else:
            last_updated = "No data available"

        self.status[dataset.name + dataset_key] = last_updated
        self._status["Last update attempt:"] = self.format_date(dataset.last_fetched, True)

    status = property(get_status, set_status)

    def update(self):
        self.status = self.app.vaccination_dataset

        # update overview based on new data
        self.overview = self.app.vaccination_dataset.data
        self.figure = self._overview

        # update graph
        self.view.update()

