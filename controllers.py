from views import *
from data import *
import matplotlib.pyplot as plt
import numpy as np


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


class MainController(Controller):
    VIEW_CLASS = MainView

    def __init__(self, app):
        super().__init__(app)
        self.view = self.VIEW_CLASS(app.frame, self)


class DatasetIntegrityController(Controller):
    VIEW_CLASS = DatasetIntegrityView

    def __init__(self, app):
        super().__init__(app)
        self.status = ""
        self.overview = self.app.international_dataset, self.app.local_dataset
        self.view = self.VIEW_CLASS(app.frame, self)

    def get_overview(self):
        return self._overview

    def set_overview(self, value):
        international_dataset, local_dataset = value
        filtered_international_dataset = international_dataset.loc[international_dataset["country"] == "Czechia"]
        filtered_international_dataset = filtered_international_dataset.dropna(how='any', axis=0)

        merged_dataset = pd.merge_asof(international_dataset, local_dataset, on='date posted')
        diff_daily_infected = merged_dataset["daily increase of infected_x"] - merged_dataset[
            "daily increase of infected_y"]
        diff_total_infected = merged_dataset["total number of infected_x"] - merged_dataset[
            "total number of infected_y"]
        diff_date_posted = merged_dataset["date loaded_x"] - merged_dataset["date loaded_y"]

        self._overview = pd.DataFrame(
            {'date posted': merged_dataset["date posted"], "diffrence daily increase of infected": diff_daily_infected,
             "diffrence total number of infected": diff_total_infected, "difference date posted": diff_date_posted})

    overview = property(get_overview, set_overview)

    def update(self):
        self.status = "Aktualizuji..."

        # update overview based on new data
        self.app.updater.update()
        self.overview = self.app.international_dataset, self.app.local_dataset

        self.view.update()


class VaccinationController(Controller):
    VIEW_CLASS = VaccinationView
    MAX_COUNTRIES_SELECTED = 4

    def __init__(self, app):
        super().__init__(app)
        self.overview = self.app.vaccination_dataset.data
        self.selectable_countries = app.countries
        self.selected_countries = []
        self.status = ""
        self.figure = self._overview
        self.view = self.VIEW_CLASS(app.frame, self)

    def get_overview(self):
        return self._overview

    def set_overview(self, value):
        vaccination_dataset = value
        self._overview = vaccination_dataset[["date posted", "country", "total vaccinations"]]
        self._overview = self._overview.fillna(0)

    overview = property(get_overview, set_overview)

    def set_figure(self, value):
        self._figure, ax = plt.subplots(nrows=1, ncols=1)

        # pick only countries from selected_countries and Czechia always

        for key, group in self._overview.groupby(["country"]):
            if key in self.selected_countries or key == "Czechia":
                ax.scatter(group["date posted"], group["total vaccinations"], label=key)

        plt.legend(loc='best')
        ax.set_xlabel("Date posted")
        ax.set_ylabel("Total vaccinations")
        #ax.set_title("")
        self._figure.tight_layout()

    def get_figure(self):
        return self._figure

    figure = property(get_figure, set_figure)

    def add_country(self, country):
        # add country to selected countries
        if country in self.selectable_countries:
            self.selected_countries.append(country)
            self.status = "Země byla přidána"
        else:
            self.status = "Tuto zemi nelze přidat"

        # update graph
        self.view.update_graph()

    def remove_country(self, country):
        # remove country from selected countries
        if country in self.selected_countries:
            self.selected_countries.remove(country)
            self.status = "Země byla odebrána"
        else:
            self.status = "Tuto zemi nelze odebrat"

        # update graph
        self.view.update_graph()

    def update(self):
        self.status = "Aktualizuji..."

        # update overview based on new data
        self.app.updater.update()
        self.overview = self.app.vaccination_dataset.data

        # update graph
        self.view.update_graph()

if __name__ == "__main__":
    test_data2 = [
        [datetime.datetime(2020, 1, 1), "Czechia", 110],
        [datetime.datetime(2020, 1, 2), "Slovakia", 110],
        [datetime.datetime(2020, 1, 2), "Poland", 110],
        [datetime.datetime(2020, 5, 18), "Slovakia", 130],
        [datetime.datetime(2020, 5, 19), "Slovakia", 130],
        [datetime.datetime(2020, 5, 20), "Slovakia", 140]
    ]

    df2 = pd.DataFrame(test_data2, columns=["date posted", "country", "total vaccinations"])
    controller = VaccinationController(None)
    #cr_data = MZCRFetcher().fetch(None)
    #controller.set_data((cr_data, cr_data))
