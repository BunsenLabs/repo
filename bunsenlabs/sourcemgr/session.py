import requests

class Session:
    def __init__(self):
        self.__requests = requests.Session()

    @property
    def requests(self) -> requests.Session:
        return self.__requests
