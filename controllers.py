from views import *
from data import *
import matplotlib.pyplot as plt


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


class MainController(Controller):
    VIEW_CLASS = MainView

    def __init__(self, app):
        super().__init__(app)
        self.view = self.VIEW_CLASS(app.frame, self)


class DatasetIntegrityController(Controller):
    VIEW_CLASS = DatasetIntegrityView

    def __init__(self, app):
        super().__init__(app)
        # self.data = self.app.international_dataset, self.app.local_dataset
        # self.status = ...
        self.view = self.VIEW_CLASS(app.frame, self)

    def get_data(self):
        return self._data

    def set_data(self, value):
        international_dataset, local_dataset = value
        filtered_international_dataset = international_dataset.loc[international_dataset["country"] == "Czechia"]
        filtered_international_dataset = filtered_international_dataset.dropna(how='any', axis=0)

        merged_dataset = pd.merge_asof(international_dataset, local_dataset, on='date posted')
        diff_daily_infected = merged_dataset["daily increase of infected_x"] - merged_dataset[
            "daily increase of infected_y"]
        diff_total_infected = merged_dataset["total number of infected_x"] - merged_dataset[
            "total number of infected_y"]
        diff_date_posted = merged_dataset["date loaded_x"] - merged_dataset["date loaded_y"]

        self._data = pd.DataFrame(
            {'date posted': merged_dataset["date posted"], "diffrence daily increase of infected": diff_daily_infected,
             "diffrence total number of infected": diff_total_infected, "difference date posted": diff_date_posted})

    data = property(get_data, set_data)

    def update(self):
        # self.status = ...
        # update overview based on new data
        self.view.update()
        pass


class VaccinationController(Controller):
    VIEW_CLASS = VaccinationView

    def __init__(self, app):
        super().__init__(app)
        #self.overview = app.international_dataset
        # self.selected_countries = ...
        # self.status = ...
        #self.figure =self._overview
        self.view = self.VIEW_CLASS(app.frame, self)

    def set_figure(self, value):
        overview = value
        self._figure = plt.Figure(figsize=(5, 4))
        ax = self._figure.add_subplot(111)
        x = overview[...]
        y = overview[...]
        ax.scatter(x, y, color='g')
        ax.legend([...])
        ax.set_xlabel(...)
        ax.set_title(...)

    def get_figure(self):
        return self._figure

    figure = property(get_figure, set_figure)

    def add_country(self, country):
        # add country to selected countries
        # update graph
        self.view.update_graph()
        pass

    def remove_country(self, country):
        # remove country from selected countries
        # update graph
        self.view.update_graph()
        pass

    def update(self):
        # self.status = ...
        # update overview based on new data
        self.view.update()
        pass


class Overview:
    pass


class VaccinationOverview(Overview):
    pass


class DatasetIntegrityOverview(Overview):
    pass


if __name__ == "__main__":
    controller = DatasetIntegrityController(None)
    cr_data = MZCRFetcher().fetch(None)
    controller.set_data((cr_data, cr_data))
