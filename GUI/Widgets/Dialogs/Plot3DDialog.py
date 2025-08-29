from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QDialog
import matplotlib as mpl
# matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    cmaps =['Blues', 'Reds', "viridis", "plasma", "cool", "winter", "copper"]
    chosen_cmap: str

    def __init__(self, parent=None, width=10, height=8, dpi=100):
        self.axes = []
        self.chosen_cmap = self.cmaps[0]

        self.fig = Figure(figsize=(width, height), dpi=dpi)


        super().__init__(self.fig)


    def load_matrix(self, arr):
        self.fig.clear()
        arr_bin = arr.copy()
        arr_bin[arr_bin > 0.5] = 1
        arr_bin[arr_bin != 1] = 0

        ax = self.fig.add_subplot(111, projection='3d')
        ax.voxels(arr_bin[:, :, :, 0], facecolors=(0,1,0,0.5))




class PlotWidget(QDialog):
    matrix: np.array

    def __init__(self, matrix: np.array):
        super().__init__()
        self.matrix = matrix

        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)

        self.sc = MplCanvas(self, width=15, height=15, dpi=100)
        self.sc.load_matrix(self.matrix)

        layout.addWidget(self.sc)

        self.sc.draw()

        self.setLayout(layout)




