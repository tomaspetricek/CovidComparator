from tkinter import *

class SearchBar:
    """
    Inspired: # https://www.geeksforgeeks.org/autocmplete-combobox-in-python-tkinter/
    """

    def __init__(self, items):
        self.items = items

        # create search box
        self.search_box = Entry(root)
        self.search_box.pack()
        self.search_box.bind('<KeyRelease>', self._check_search)

        # create advisor
        self.advisor = Listbox(root)
        self.advisor.pack()
        self.update_advisor(items)

    def _check_search(self, event):
        target = event.widget.get()

        if target == '':
            items_to_display = self.items
        else:
            items_to_display = []
            for item in self.items:
                if target.lower() in item.lower():
                    items_to_display.append(item)

        self.update_advisor(items_to_display)

    def update_advisor(self, items_to_display):
        # clear previous data
        self.advisor.delete(0, 'end')

        # put new data
        for item in items_to_display:
            self.advisor.insert('end', item)


# Driver code
items = ('C', 'C++', 'Java',
     'Python', 'Perl',
     'PHP', 'ASP', 'JS')

root = Tk()

search_bar = SearchBar(items)

root.mainloop()
