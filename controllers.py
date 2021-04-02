from views import *

class Controller:
    """
    Handles logic for view.
    """

    def __init__(self, app):
        self.app = app
        self.view = None
        #self.navigation_callbacks = ...

    def set_navigation_callbacks(self, value):
        self._navigation_callbacks = []

        # create call backs for all views except this one
        for view in self.app.views:
            if view != self:
                callback = lambda: self.app.show_view(view)
                self._navigation_callbacks.append(callback)

    def get_navigation_callbacks(self):
        return self._navigation_callbacks

    navigation_callbacks = property(get_navigation_callbacks, set_navigation_callbacks)

    def update(self):
        """
        Updates data for view.
        """
        pass

class MainController(Controller):
    def __init__(self, app):
        super().__init__(app)
        self.view = Main(app.frame, self)


class DatasetIntegrityController(Controller):
    def __init__(self, app):
        super().__init__(app)
        #self.data = self.app.international_dataset, self.app.local_dataset
        #self.status = ...
        #self.view = DatasetIntegrityOverview(app.frame, self)

    def get_data(self):
        return self._data

    def set_data(self, value):
        international_dataset, local_dataset = value
        columns = ["date posted", "diffrence daily increase of infected", "diffrence total number of infected", "difference date posted"]
        filtered_international_dataset = international_dataset.loc(international_dataset["country"] == "Czechia")
        print(filtered_international_dataset)
        #for czech_day in app.local_dataset

    data = property(get_data, set_data)

    def update(self):
        self.status = ...
        # update overview based on new data
        self.view.update()
        pass


class VaccinationController(Controller):
    def __init__(self, app):
        super().__init__(app)
        self.data = app.international_dataset
        self.selected_countries = ...
        self.status = ...
        self.view = VaccinationOverview(app.frame, self)


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
        self.status = ...
        # update overview based on new data
        self.view.update()
        pass

if __name__ == "__main__":
    controller = DatasetIntegrityController(None)
    controller.set_data()