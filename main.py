import sys

from PySide import QtGui

from RestController import Controller

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ui = Controller()
    ui.show()
    sys.exit(app.exec_())
