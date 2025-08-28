import matplotlib.pyplot as plt
import numpy as np
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QVBoxLayout, QSlider, QHBoxLayout, QLabel, QListView, QComboBox, QCheckBox, QPushButton
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from poetry.console.commands import self
import matplotlib as mpl
from superqt import QLabeledRangeSlider, QCollapsible
import scipy.stats as stats


from GUI.Logic.LogicHandler import LogicHandler

from GUI.utils.save_functions import save_plt



class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100, n_phenotypes=2):
        self.fig = Figure(figsize=(width, height), dpi=dpi)

        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)




class AVGTimeCourseDisplay(QtWidgets.QWidget):
    __logic_handler: LogicHandler
    __experiment_names: dict
    __phenotype_names: list

    hist_sum: np.array
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

        self.dispersion_box = QComboBox()
        self.dispersion_box.addItems(["St. Dev.", "CI", "IQR"])
        self.dispersion_box.currentIndexChanged.connect(self.update_plot)


        self.choose_plot_collapsible = QCollapsible("Choose experiments to average")

        self.top_lay.addWidget(self.set_norm_btn)
        self.top_lay.addWidget(self.save_btn)
        self.top_lay.addWidget(self.dispersion_box)
        self.top_lay.addWidget(self.choose_plot_collapsible)
        self.top_lay.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)


        self.mainLayout = QVBoxLayout()

        self.sc = MplCanvas(self, width = 5, height = 4, dpi = 100, n_phenotypes = self.__logic_handler.param_handler.num_phenotypes)


        self.pageLayout.addLayout(self.top_lay)

        self.mainLayout.addWidget(self.sc)
        self.pageLayout.addLayout(self.mainLayout, stretch=1)

        self.setLayout(self.pageLayout)

        self.__load_experiment_names()

        self.checkboxes = []
        self.button_select_all = QPushButton("Select all")

        self.choose_plot_collapsible.addWidget(self.button_select_all)

        for k, v in self.experiment_names.items():
            checkbox = QCheckBox(k)
            checkbox.setChecked(v)
            checkbox.checkStateChanged.connect(self.__load_experiment_plots)
            checkbox.setDisabled(False)

            self.checkboxes.append(checkbox)
            self.choose_plot_collapsible.addWidget(checkbox)

        self.hist_sum = None
        self.__phenotype_names = []


    def refresh_layout(self):
        self.update_plot()


    def update_plot(self):
        self.sc.ax.cla()

        if self.hist_sum is None or len(self.hist_sum) == 0:
            self.sc.draw()
            return

        yerr = self.__get_yerr(plots=self.plots)
        for p in range(self.hist_sum.shape[-1]):
            self.sc.ax.errorbar(range(len(self.hist_sum)), self.hist_sum[:, p], yerr = yerr[:, p], label=self.__phenotype_names[p])

        self.sc.ax.legend()
        self.sc.ax.title.set_text("averaged time plot")

        if self.normalize_plot:
            self.sc.ax.set_ylim(-0.1, 1.1)

        self.sc.draw()



    def __load_experiment_names(self):
        self.experiment_names = {}
        for e in self.__logic_handler.experiment_list:
            self.experiment_names[e] = False



    def __load_experiment_plots(self):
        plots = []
        num_c = 0
        exp_name = ""

        for c in self.checkboxes:
            if c.isChecked():
                exp_name = c.text()
                plots.append(self.__logic_handler.get_history_by_name(exp_name))

                num_c += 1

        if num_c != 0:
            self.hist_sum = np.zeros_like(plots[0])
            for p in plots:
                self.hist_sum += p
            self.hist_sum /= num_c

            self.plots = np.array(plots)

            self.__phenotype_names = self.__logic_handler.get_phenotypes_by_name(exp_name)

        else:
            self.hist_sum = None

        self.update_plot()
        self.__update_checkboxes(num_c, exp_name)

    def __get_yerr(self, plots):
        if self.dispersion_box.currentText() == "St. Dev.":
            return np.std(self.plots, axis=0)


        if self.dispersion_box.currentText() == "CI":
            m, s, n = np.mean(plots, axis=0), np.std(plots, axis = 0, ddof=1), plots.shape[0]
            t = stats.t.ppf(0.95, df=n - 1)
            e = t * (s / np.sqrt(n))
            return e


        if self.dispersion_box.currentText() == "IQR":
            return stats.iqr(plots, axis=0)


    def __update_checkboxes(self, num_c: int, exp_name: str):
        if num_c == 0:
            for c in self.checkboxes:
                c.setDisabled(False)

        if num_c == 1:
            chosen_yaml = self.__logic_handler.get_yaml_by_name(exp_name)
            dim, prob_name, num_epochs, pop_len = chosen_yaml['num_dim'], chosen_yaml['problem_name'], chosen_yaml['num_epochs'], chosen_yaml['population_length']

            for c in self.checkboxes:
                compatible = self.__logic_handler.check_compatibility(c.text(), dim, prob_name, num_epochs, pop_len)
                c.setDisabled(not compatible)



    def normalize_plot_check_signal(self):
        self.normalize_plot = not self.normalize_plot
        self.update_plot()


    def save_plot_signal(self):
        save_plt(self.sc.fig, self.__logic_handler.chosen_exp, "avg_hist_err")

