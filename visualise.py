import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

from GUI.MainWindow import MainWindow





def main():
    app = QtWidgets.QApplication([])
    widget = MainWindow()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())




if __name__ == "__main__":
    main()



