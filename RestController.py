import xml.etree.ElementTree

import requests
from PySide.QtGui import QWidget

import RestView, RestModel


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

        self.model = RestModel.Model()

        self.view.bSubmit.clicked.connect(self.submit)

    def submit(self):
        """
        Is called when the submit button is pressed

        :return:
        """
        desc = []
        if self.view.tStart.text() != '' and self.view.tZiel.text() != '':
            if self.view.slider.value() == 1:  # When the slider points at XML
                self.model.jorx = "xml?"
            else:
                self.model.jorx = "json?"

            self.view.textBrowser.clear()  # Clear the textbrowser

            self.model.origin = self.view.tStart.text()
            self.model.destination = self.view.tZiel.text()

            url = self.model.getDirection(self.model.origin, self.model.destination, False)

            try:
                self.model.valid = True
                self.model.error = False
                if self.model.jorx == "json?":
                    # Clear the array


                    tree = url.json()

                    if tree["geocoded_waypoints"][0]["geocoder_status"] == "ZERO_RESULTS":
                        self.view.textBrowser.append("Diesen Startpunkt gibt es nicht!")
                        self.view.textBrowser.append("Tipp: Haben Sie sich verschrieben? <br/>")
                        self.model.valid = False
                        self.model.error = True

                    elif tree["geocoded_waypoints"][1]["geocoder_status"] == "ZERO_RESULTS":
                        self.view.textBrowser.append("Diesen Zielpunkt gibt es nicht!")
                        self.view.textBrowser.append("Tipp: Haben Sie sich verschrieben? <br/>")
                        self.model.valid = False
                        self.model.error = True

                    elif tree["status"] == "ZERO_RESULTS":
                        self.view.textBrowser.append("Keine möglichen Wege gefunden :(")
                        self.model.valid = False
                        self.model.error = True

                    if self.model.valid:

                        self.view.status.setText("ok")

                        leg = tree["routes"][0]["legs"][0]  # Start from legs-tag

                        dur = str(leg["duration"]["text"])  # Duration
                        dist = str(leg["distance"]["text"])  # Distance

                        self.header(leg["start_address"], leg["end_address"], dist, dur)

                        for i in leg["steps"]:  # Distance, duration and description per step
                            desc.append(str(i["html_instructions"]))
                            desc.append("<i>(" + str(i["distance"]["text"]) + " /")
                            desc.append(i["duration"]["text"] + ")</i>, ")

                        self.view.textBrowser.append(" ".join(desc))  # Append everything to the textBrowser

                else:
                    desc.clear()  # Clear the array

                    tree = xml.etree.ElementTree.fromstring(url.content)  # Parse to XML

                    print(tree[1][0].text)
                    print(tree[2][0].text)

                    if tree[1][0].text == "ZERO_RESULTS":
                        self.view.textBrowser.setText("Diesen Startpunkt gibt es nicht!")
                        self.view.textBrowser.append("Tipp: Haben Sie sich verschrieben?")
                        self.model.valid = False
                        self.model.error = True

                    elif tree[2][0].text == "ZERO_RESULTS":
                        self.view.textBrowser.setText("Diesen Zielpunkt gibt es nicht!")
                        self.view.textBrowser.append("Tipp: Haben Sie sich verschrieben?")
                        self.model.valid = False
                        self.model.error = True

                    elif tree.find("status").text == "ZERO_RESULTS":
                        self.view.textBrowser.append("Keine möglichen Wege gefunden :(")
                        self.model.valid = False
                        self.model.error = True



                    if self.model.valid:

                        self.view.status.setText("ok")

                        leg = tree.find("route").find("leg")  # Start from the leg-tag

                        dist = leg.find("distance")[1].text  # Distance
                        dur = leg.find("duration")[1].text  # Duration

                        self.header(leg.find("start_address").text, leg.find("end_address").text, dist, dur)

                        for child in leg.findall("step"):  # Distance, duration and description per step
                            desc.append(child[5].text)
                            desc.append("<i>(" + child[6][1].text + " /")
                            desc.append(child[4][1].text + ")</i><br>")

                        self.view.textBrowser.append(" ".join(desc))  # Append everything to the textBrowser

            except Exception:
                self.model.error = True
                self.view.status.setText("Fehlschlag")

            finally:
                if self.model.error:
                    self.view.status.setText("Fehlschlag")

            self.view.textBrowser.verticalScrollBar().setValue(0)  # Scrollbar on top

        else:
            self.view.textBrowser.setText("Eingabe fehlt!")
            self.view.status.setText("Fehlschlag")

    def header(self, start, ziel, dist, dur):
        """
        The header contains: duration, distance and the description-word

        :param dist: Distance
        :param dur: Duration
        :return:
        """
        self.view.textBrowser.append("Start: <b>" + start + "</b>")
        self.view.textBrowser.append("Ziel: <b>" + ziel + "</b>")
        self.view.textBrowser.append("<br/>")
        self.view.textBrowser.append("Entfernung: <b>" + dist + "</b>")
        self.view.textBrowser.append("Dauer: <b>" + dur + "</b>")
        self.view.textBrowser.append("<br/>")
        self.view.textBrowser.append("Wegbeschreibung: <br/>")
