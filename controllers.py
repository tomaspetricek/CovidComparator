from views import Vacc

class Controller:
    """
    Handles logic for view.
    """

    def __init__(self, app):
        self.app = app
        self.view = None
        self.navigation_callbacks = ...

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


class DatasetIntegrityController(Controller):
    def __init__(self, app):
        super().__init__(app)
        self.data = ...
        self.status = ...
        self.view = DatasetIntegrityOverview(app, self)

    def update(self):
        self.status = ...
        # update overview based on new data
        self.view.update()
        pass


class VaccinationController(Controller):
    def __init__(self, app):
        super().__init__(app)
        self.data = ...
        self.selected_countries = ...
        self.status = ...
        self.view = VaccinationOverview(app, self)

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