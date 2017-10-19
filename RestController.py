"""
    Author: Florian Wellner
    Created on: 18.10.2017
    Last modified on: 19.10.2017
    Python version: 3.4
"""

import xml.etree.ElementTree

import requests
from PySide.QtGui import QWidget

import RestView


class Controller(QWidget):
    """
    Controller Class
    """

    def __init__(self, parent=None):
        """
        Initialise
        :param parent:
        """
        super().__init__(parent)
        self.view = RestView.Ui_Form()
        self.view.setupUi(self)

        self.key = "&key=AIzaSyBW1HiEJEezAPLwE-1gJFm7Nk5_SabWxi4"
        self.origin = ""
        self.destination = ""
        self.jorx = "json"
        self.url = "https://maps.googleapis.com/maps/api/directions/"
        self.tree = ""

        self.view.bSubmit.clicked.connect(self.submit)

    def submit(self):
        """
        Is called when the submit button is pressed
        :return:
        """
        desc = []
        if self.view.tStart.text() != '' and self.view.tZiel.text() != '':
            if self.view.slider.value() == 1: #When the slider points at XML
                self.jorx = "xml"
            else:
                self.jorx = "json"

            self.view.status.setText("ok")
            self.view.textBrowser.clear() #Clear the textbrowser

            self.origin = self.view.tStart.text()
            self.destination = self.view.tZiel.text()

            try:
                url = self.url + self.jorx \
                      + "?origin=" + self.origin \
                      + "&destination=" + self.destination \
                      + "&language=de" + self.key #The url the information is drawn from
                with requests.get(url, verify=False) as geturl:
                    if self.isjson():
                        desc.clear() #Clear the array
                        self.tree = geturl.json()

                        jhelp = self.tree["routes"][0]["legs"][0] #Start from legs-tag

                        dur = str(jhelp["duration"]["text"]) #Duration
                        dist = str(jhelp["distance"]["text"]) #Distance

                        self.header(dist, dur)

                        for i in jhelp["steps"]: #Distance, duration and description per step
                            desc.append(str(i["html_instructions"]))
                            desc.append("<i>(" + str(i["distance"]["text"]) + " /")
                            desc.append(i["duration"]["text"] + ")</i>, ")

                        self.view.textBrowser.append(" ".join(desc)) #Append everything to the textBrowser

                    else:
                        desc.clear() #Clear the array
                        self.tree = xml.etree.ElementTree.fromstring(geturl.content) #Parse to XML

                        leg = self.tree.find("route").find("leg") #Start from the leg-tag

                        dist = leg.find("distance")[1].text #Distance
                        dur = leg.find("duration")[1].text #Duration

                        self.header(dist, dur)

                        for child in leg.findall("step"): #Distance, duration and description per step
                            desc.append(child[5].text)
                            desc.append("<i>(" + child[6][1].text + " /")
                            desc.append(child[4][1].text + ")</i><br>")

                        self.view.textBrowser.append(" ".join(desc)) #Append everything to the textBrowser

            except Exception:
                self.view.status.setText("Fehlschlag")

            self.view.textBrowser.verticalScrollBar().setValue(0) #Scrollbar on top

        else:
            self.view.status.setText("Eingabe fehlt")

    def isjson(self):
        """
        Checks if the slider is on JSON or XML
        :return: True or False
        """
        isj = False
        if self.jorx == "json":
            isj = True
        return isj

    def header(self, dist, dur):
        """
        The header contains: duration, distance and the description-word
        :param dist: Distance
        :param dur: Duration
        :return:
        """
        self.view.textBrowser.append("Entfernung: <b>" + dist + "</b>")
        self.view.textBrowser.append("Dauer: <b>" + dur + "</b>")
        self.view.textBrowser.append("<br>")
        self.view.textBrowser.append("Wegbeschreibung: <br>")
