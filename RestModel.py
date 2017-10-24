import requests

class Model:
    def __init__(self):
        self.key = "&key=AIzaSyBW1HiEJEezAPLwE-1gJFm7Nk5_SabWxi4"
        self.origin = ""
        self.destination = ""
        self.jorx = "json?"
        self.url = "https://maps.googleapis.com/maps/api/directions/"
        self.tree = ""
        self.lang= "&language=de"
        self.valid = True
        self.error = False

    def getDirection(self, start, ziel, cert):
        """


        :param start:
        :param ziel:
        :param cert:
        :return:
        """
        return requests.get(self.url + self.jorx + "origin=" + start + "&destination=" + ziel + self.lang + self.key, verify=cert)
