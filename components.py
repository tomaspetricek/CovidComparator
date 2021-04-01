# components.py
class Component:
    def __init__(self, parent):
        pass


class AutocompleteSearchBar(Component):
    pass


class Graph(Component):
    """
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = ...
        self.toolbar = ... # removal buttons
        pass


class Table(Component):
    """
    Inspiration: https://www.geeksforgeeks.org/create-table-using-tkinter/
    """
    pass


class Navigation(Component):
    # Menu - https://www.youtube.com/watch?v=ZS2_v_zsPTg
    def __init__(self, parent, button_callbacks):
        super().__init__(parent)
        pass

