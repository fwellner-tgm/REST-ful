"""
    Author: Florian Wellner
    Created on: 18.10.2017
    Last modified on: 19.10.2017
    Python version: 3.4
"""

import sys

from PySide import QtGui

from RestController import Controller

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ui = Controller()
    ui.show()
    sys.exit(app.exec_())
