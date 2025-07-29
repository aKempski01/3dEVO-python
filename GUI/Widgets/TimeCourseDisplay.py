import numpy as np
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QVBoxLayout, QSlider, QHBoxLayout, QLabel, QListView, QComboBox
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from poetry.console.commands import self
import matplotlib as mpl

from GUI.Logic.LogicHandler import LogicHandler


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100, n_phenotypes=2):
        self.fig = Figure(figsize=(width, height), dpi=dpi)

        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)





class TimeCourseDisplay(QtWidgets.QWidget):
    __logic_handler: LogicHandler
    displayed_epoch: int = 0
    history: np.ndarray

    def __init__(self, logic_handler: LogicHandler):
        super().__init__()

        self.__logic_handler = logic_handler

        self.pageLayout = QVBoxLayout()

        self.sc = MplCanvas(self, width = 5, height = 4, dpi = 100, n_phenotypes = self.__logic_handler.param_handler.num_phenotypes)

        self.pageLayout.addWidget(self.sc)
        self.setLayout(self.pageLayout)

        self.refresh_layout()


    def refresh_layout(self):

        if self.__logic_handler.param_handler is not None:
            self.update_history()
            self.update_plot()


    def update_plot(self):
        self.update_history()
        self.sc.ax.cla()
        self.sc.ax.plot(self.history, label = self.__logic_handler.param_handler.phenotype_names.values())
        self.sc.ax.legend()
        self.sc.ax.title.set_text("time plot")

        self.sc.draw()


    def update_history(self):
        self.history = self.__logic_handler.get_history()
