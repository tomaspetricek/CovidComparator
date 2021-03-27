from tkinter import *
from random import randint
import threading

# based on: https://stackoverflow.com/questions/14384739/how-can-i-add-a-background-thread-to-flask

DOWNLOAD_TIME = 5


class App:
    def __init__(self):
        self.root = Tk()
        self.root.title("App")
        self.root.geometry("500x400")

        self.label = Label(self.root, text="Our Application")
        self.label.pack(pady=20)

        self.button = Button(self.root, text="pick random number", command=self.change_label)
        self.button.pack(pady=20)

        self.label = Label(self.root, text="")
        self.label.pack(pady=20)
        self.downloader = None
        self.data = None
        self.data_lock = threading.Lock()

    def update_data(self):
        # change sensitive data
        with self.data_lock:
            self.label.config(text=f"downloaded")

    def download(self):
        self.update_data()

        # wait to make next download
        self.wait_to_download()

    def wait_to_download(self):
        # create new thread and wait till right time
        self.downloader = threading.Timer(DOWNLOAD_TIME, self.download, ())
        self.downloader.setDaemon(True)
        self.downloader.start()

    def change_label(self):
        self.label.config(text=f"random number: {randint(1, 100)}")

    def run(self):
        self.wait_to_download()
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()



