import numpy as np
from PySide6 import QtGui
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QVBoxLayout, QSlider, QHBoxLayout, QLabel, QListView, QComboBox
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from poetry.console.commands import self
import matplotlib as mpl
from matplotlib import pyplot as plt
from GUI.Logic.LogicHandler import LogicHandler
from GUI.utils.save_functions import save_plt

class MplCanvas(FigureCanvasQTAgg):

    cmaps =['Blues', 'Reds', "viridis", "plasma", "cool", "winter", "copper"]
    chosen_cmap: str

    def __init__(self, parent=None, width=10, height=8, dpi=100, n_phenotypes=2, n_dim: int = 2):
        self.axes = []
        self.chosen_cmap = self.cmaps[0]

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.reload_axes(n_phenotypes=n_phenotypes, n_dim=n_dim)


        super().__init__(self.fig)


    def reload_axes(self, n_phenotypes: int = 2, n_dim: int = 2):
        self.fig.clear()
        # self.fig.clf()
        self.axes = []
        if n_dim == 2:
            for n in range(n_phenotypes):
                self.axes.append(self.fig.add_subplot(n_phenotypes-1, 2, n+1))
                self.fig.colorbar(mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(0, 1), cmap=self.chosen_cmap), ax=self.axes[n],
                                     orientation='vertical')

        elif n_dim == 3:
            for n in range(n_phenotypes):
                self.axes.append(self.fig.add_subplot(n_phenotypes-1, 2, n + 1, projection='3d'))
                self.fig.colorbar(mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(0, 1), cmap=self.chosen_cmap), ax=self.axes[n],
                                  orientation='vertical')

        else:
            ValueError("Number of dimensions is not supported.")



class PlotDisplayer(QtWidgets.QWidget):
    __logic_handler: LogicHandler
    displayed_epoch: int = 0
    game_matrix: np.ndarray

    def __init__(self, logic_handler: LogicHandler):
        super().__init__()

        self.__logic_handler = logic_handler
        self.sc = MplCanvas(self, width = 15, height = 15, dpi = 100, n_phenotypes = self.__logic_handler.param_handler.num_phenotypes)


        self.combo_c_map = QComboBox()

        self.combo_c_map.addItems(self.sc.cmaps)
        self.combo_c_map.setCurrentText(self.sc.chosen_cmap)
        self.combo_c_map.currentTextChanged.connect(self.__c_map_changed_signal)

        self.save_matrix_btn = QtWidgets.QPushButton("Save image")
        self.save_matrix_btn.pressed.connect(self.__save_btn_pressed_signal)


        self.up_lay = QtWidgets.QHBoxLayout()
        self.up_lay.addWidget(self.combo_c_map)
        self.up_lay.addWidget(self.save_matrix_btn)
        self.up_lay.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.slider_text = QLabel("Epoch Num: {}".format(self.displayed_epoch))
        self.slider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.slider.valueChanged.connect(self.__slider_released_signal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(self.__logic_handler.param_handler.num_epochs)
        self.slider.setSingleStep(1)


        self.pageLayout = QVBoxLayout()
        self.botLayout = QHBoxLayout()
        self.botLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom)

        self.pageLayout.addLayout(self.up_lay)
        self.pageLayout.addWidget(self.sc)
        self.pageLayout.addLayout(self.botLayout)

        self.botLayout.addWidget(self.slider_text)
        self.botLayout.addWidget(self.slider)


        self.setLayout(self.pageLayout)

        self.refresh_layout()


    def refresh_layout(self):
        self.slider.setMaximum(self.__logic_handler.param_handler.num_epochs)
        self.sc.reload_axes(self.__logic_handler.param_handler.num_phenotypes, self.__logic_handler.param_handler.num_dim)


        if self.__logic_handler.param_handler is not None:
            self.__update_matrix()
            self.__update_plot()

    def __update_plot(self):
        for n in range(self.__logic_handler.param_handler.num_phenotypes):
            self.sc.axes[n].cla()

            if self.__logic_handler.param_handler.num_dim == 2:
                self.sc.axes[n].imshow(self.game_matrix[:, :, n], vmin=0, vmax=1, cmap=self.sc.chosen_cmap)
            elif self.__logic_handler.param_handler.num_dim == 3:
                idx = np.argwhere(self.game_matrix[:, :, :, n] > -1)
                c = self.game_matrix[idx[:,0], idx[:,1], idx[:,2], n]
                self.sc.axes[n].scatter(idx[:,0], idx[:,1], idx[:,2], c=c, vmin=0, vmax=1, cmap=self.sc.chosen_cmap, alpha=0.5)

            self.sc.axes[n].title.set_text(self.__logic_handler.param_handler.phenotype_names[n])

        self.sc.draw()


    def __update_matrix(self):
        if self.__logic_handler.param_handler is not None:
            self.game_matrix = self.__logic_handler.get_array(self.displayed_epoch)


    def __slider_released_signal(self):
        self.displayed_epoch = self.slider.value()
        self.slider_text.setText("Epoch Num: {}".format(self.displayed_epoch))
        self.__update_matrix()
        self.__update_plot()


    def __c_map_changed_signal(self, text: str):
        self.sc.chosen_cmap = text
        self.sc.reload_axes(self.__logic_handler.param_handler.num_phenotypes, self.__logic_handler.param_handler.num_dim)
        self.__update_plot()


    def __save_btn_pressed_signal(self):
        save_plt(self.sc.fig, self.__logic_handler.chosen_exp, "matrix_epoch_" + str(self.displayed_epoch))


    def explode(self, data):
        size = np.array(data.shape) * 2
        data_e = np.zeros(size - 1, dtype=data.dtype)
        data_e[::2, ::2, ::2] = data
        return data_e

