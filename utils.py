import requests

# TODO rename Logger to Notifier
# TODO create Logger that logs into file -> logs errors that we wouldn't anticipate

class Logger:

    def __init__(self, url):
        self.URL = url
        pass

    def send_info(self, message):
        self._send(0, message)
        pass

    def send_error(self, message):
        self._send(2, message)
        pass

    def send_warning(self, message):
        self._send(1, message)
        pass

    def _send(self, type_, message):
        params = {"type": type_, "text": message}

        requests.post(self.URL, params)
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
