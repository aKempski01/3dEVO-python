import numpy as np
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QVBoxLayout, QSlider, QHBoxLayout, QLabel, QListView, QComboBox, QCheckBox, QPushButton
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from poetry.console.commands import self
import matplotlib as mpl
from pyqttoast import Toast, ToastPreset

from GUI.Logic.LogicHandler import LogicHandler

from GUI.utils.save_functions import save_plt
from GUI.utils.toast_handling import show_save_plot_toast


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100, n_phenotypes=2):
        self.fig = Figure(figsize=(width, height), dpi=dpi)

        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)




class TimeCourseDisplay(QtWidgets.QWidget):
    __logic_handler: LogicHandler
    displayed_epoch: int = 0
    history: np.ndarray

    normalize_plot: bool = True

    def __init__(self, logic_handler: LogicHandler):
        super().__init__()

        self.__logic_handler = logic_handler

        self.pageLayout = QVBoxLayout()
        self.top_lay = QHBoxLayout()

        self.set_norm_btn = QPushButton("Normalize plot")
        self.set_norm_btn.pressed.connect(self.normalize_plot_check_signal)

        self.save_btn = QPushButton("Save plot")
        self.save_btn.pressed.connect(self.save_plot_signal)

        self.top_lay.addWidget(self.set_norm_btn)
        self.top_lay.addWidget(self.save_btn)
        self.top_lay.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)


        self.mainLayout = QVBoxLayout()

        self.sc = MplCanvas(self, width = 5, height = 4, dpi = 100, n_phenotypes = self.__logic_handler.param_handler.num_phenotypes)


        self.pageLayout.addLayout(self.top_lay)

        self.mainLayout.addWidget(self.sc)
        self.pageLayout.addLayout(self.mainLayout, stretch=1)

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

        if self.normalize_plot:
            self.sc.ax.set_ylim(-0.1, 1.1)


        self.sc.draw()


    def update_history(self):
        self.history = self.__logic_handler.get_history()


    def normalize_plot_check_signal(self):
        self.normalize_plot = not self.normalize_plot
        self.update_plot()


    def save_plot_signal(self):
        save_path = save_plt(self.sc.fig, self.__logic_handler.chosen_exp, "history")
        show_save_plot_toast(self, save_path)

