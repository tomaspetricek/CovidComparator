class Logger:
    def __init__(self, url):
        pass

    def send_info(self, message):
        pass

    def send_error(self, message):
        pass

    def send_warning(self, message):
        pass

    def _send(self, type_, message):
        pass

class IntegrityComparator:
    pass


class VaccinationComparator:
    pass

class Callback:
    """
    Stores function and its arguments.
    When called, it calls the function passing stored arguments.
    """
    def __init__(self, fun, *args, **kwargs):
        self.fun = fun
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        self.fun(*self.args, **self.kwargs)
