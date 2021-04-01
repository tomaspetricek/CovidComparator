class View:
    """
    Represents visual part of app.
    Works with data provided by controller
    """

    def __init__(self, parent, controller):
        self.controller = controller
        pass

    def update(self):
        """
        Updates whole view.
        """
        pass

class Main(View):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.navigation = ...


class VaccinationOverview(View):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.navigation = ...
        self.state = ...
        self.graph = ...
        self.search_bar = ...

    def update_graph(self):
        pass

    def update(self):
        pass


class DatasetIntegrityOverview(View):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.navigation = ...
        self.state = ...
        self.table = ...

    def update_table(self):
        self.controller.data
        pass

    def update(self):
        pass