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
        self.axes = []
        self.fig = Figure(figsize=(width, height), dpi=dpi)

        for n in range(n_phenotypes):
            self.axes.append(self.fig.add_subplot(int(0.5 + 2/n_phenotypes), 2, n+1))
            self.fig.colorbar(mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(0, 1)), ax=self.axes[n],
                                 orientation='vertical')

        super().__init__(self.fig)





class PlotDisplayer(QtWidgets.QWidget):
    __logic_handler: LogicHandler
    displayed_epoch: int = 0
    game_matrix: np.ndarray

    def __init__(self, logic_handler: LogicHandler):
        super().__init__()

        self.__logic_handler = logic_handler

        self.slider_text = QLabel("Epoch Num: {}".format(self.displayed_epoch))
        self.slider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.slider.valueChanged.connect(self.slider_released)

        self.pageLayout = QVBoxLayout()
        self.botLayout = QHBoxLayout()
        self.botLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom)

        self.sc = MplCanvas(self, width = 5, height = 4, dpi = 100, n_phenotypes = self.__logic_handler.param_handler.num_phenotypes)

        self.pageLayout.addWidget(self.sc)
        self.pageLayout.addLayout(self.botLayout)

        self.botLayout.addWidget(self.slider_text)
        self.botLayout.addWidget(self.slider)


        self.setLayout(self.pageLayout)

        self.refresh_layout()


    def refresh_layout(self):
        if self.__logic_handler.param_handler is not None:
            self.slider.setDisabled(False)
            self.slider.setMinimum(0)
            self.slider.setMaximum(self.__logic_handler.param_handler.num_epochs)
            self.slider.setSingleStep(1)


        else:
            self.slider.setDisabled(True)


        if self.__logic_handler.param_handler is not None:
            self.update_matrix()
            self.update_plot()



    def update_plot(self):
        for n in range(self.__logic_handler.param_handler.num_phenotypes):
            self.sc.axes[n].cla()
            self.sc.axes[n].imshow(self.game_matrix[:, :, n], vmin=0, vmax=1)
            self.sc.axes[n].title.set_text(self.__logic_handler.param_handler.phenotype_names[n])

        self.sc.draw()


    def update_matrix(self):
        if self.__logic_handler.param_handler is not None:
            self.game_matrix = self.__logic_handler.get_array(self.displayed_epoch)


    def slider_released(self):
        self.displayed_epoch = self.slider.value()
        self.slider_text.setText("Epoch Num: {}".format(self.displayed_epoch))
        self.update_matrix()
        self.update_plot()

