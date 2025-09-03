from typing import Optional

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QDialog, QHBoxLayout, QListWidget, QComboBox, QCheckBox, \
    QPushButton
from superqt import QLabeledDoubleSlider, QCollapsible
from PySide6.QtCore import Qt
import matplotlib as mpl
# matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from poetry.console.commands import self

from GUI.Logic.LogicHandler import LogicHandler
from GUI.utils.save_functions import save_plt
from GUI.utils.toast_handling import show_save_plot_toast
from utils.Enums import SpatialityStrategy


class MplCanvas(FigureCanvasQTAgg):

    cmaps =['Blues', 'Reds', "viridis", "plasma", "cool", "winter", "copper"]
    chosen_cmap: str

    def __init__(self, parent=None, width=10, height=8, dpi=100):
        self.axes = []
        self.chosen_cmap = self.cmaps[0]

        self.fig = Figure(figsize=(width, height), dpi=dpi)


        super().__init__(self.fig)


    def load_matrix(self, arr, indices, colors, cut_offs, alpha):
        self.fig.clear()
        ax = self.fig.add_subplot(111, projection='3d')

        for i in range(len(indices)):

            arr_bin = arr.copy()
            arr_bin[arr_bin > cut_offs[i]] = 1
            arr_bin[arr_bin != 1] = 0

            ax.voxels(arr_bin[:, :, :, indices[i]], facecolors=(colors[i][0], colors[i][1], colors[i][2], alpha))


class OptionsRow(QWidget):
    colors = ['red', 'green', 'blue', 'black', 'purple', 'yellow']
    colors_rgb = [(1,0,0), (0,1,0), (0,0,1), (0,0,0), (1,0,1), (0,1,1)]

    color_combo: QComboBox
    checkbox: QCheckBox
    cut_off_slider: Optional[QLabeledDoubleSlider]

    is_mixed: bool
    idx: int

    def __init__(self, idx, name, is_mixed: bool):
        super().__init__()
        self.is_mixed = is_mixed
        self.idx = idx
        layout = QHBoxLayout()

        idx_label = QLabel(str(idx))
        name_label = QLabel(name)

        self.color_combo = QComboBox()
        self.color_combo.addItems(self.colors)

        if idx < len(self.colors):
            self.color_combo.setCurrentIndex(idx)

        else:
            self.color_combo.setCurrentIndex(0)

        self.checkbox = QCheckBox("Display")

        if is_mixed:
            self.cut_off_slider = QLabeledDoubleSlider()
            self.cut_off_slider.setRange(0, 1.0)
            self.cut_off_slider.setValue(0.5)


        layout.addWidget(idx_label)
        layout.addWidget(name_label)
        layout.addWidget(self.color_combo)

        if is_mixed:
            layout.addWidget(self.cut_off_slider)

        layout.addWidget(self.checkbox)
        self.setLayout(layout)


    def get_options(self):

        color = self.colors_rgb[[i for i in range(len(self.colors)) if self.colors[i] == self.color_combo.currentText()][0]]

        if self.is_mixed:
            return self.idx, self.checkbox.isChecked(), color, self.cut_off_slider.value()

        return self.idx, self.checkbox.isChecked(), color, 0.1




class PlotWidget(QDialog):
    matrix: np.array
    chosen_exp_name: str
    displayed_epoch: int

    def __init__(self, matrix: np.array, logic_handler: LogicHandler, displayed_epoch: int) -> None:
        super().__init__()
        self.matrix = matrix
        self.chosen_exp_name = logic_handler.chosen_exp
        self.displayed_epoch = displayed_epoch

        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)

        self.sc = MplCanvas(self, width=15, height=15, dpi=100)


        top_layout = QHBoxLayout()
        bot_layout = QVBoxLayout()

        self.save_btn = QPushButton("Save")
        self.save_btn.pressed.connect(self.save_signal)

        options_collapsible = QCollapsible("Select phenotypes")
        self.options = []
        for idx, name in logic_handler.param_handler.phenotype_names.items():
            self.options.append(OptionsRow(idx, name, logic_handler.param_handler.spatiality_strategy == SpatialityStrategy.MIXED))

        for o in self.options:
            options_collapsible.addWidget(o)


        update_plot_btn = QPushButton("Update Plot")
        update_plot_btn.pressed.connect(self.update_plot_signal)

        top_layout.addWidget(self.save_btn)
        top_layout.addWidget(options_collapsible)
        top_layout.addWidget(update_plot_btn)

        top_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        alpha_label = QLabel("Opacity")
        self.alpha_slider = QLabeledDoubleSlider(Qt.Orientation.Horizontal)
        self.alpha_slider.setRange(0, 1)
        self.alpha_slider.setValue(0.5)
        # self.alpha_slider.valueChanged.connect(self.alpha_slider_signal)

        bot_layout.addWidget(alpha_label)
        bot_layout.addWidget(self.alpha_slider)
        bot_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)


        layout.addLayout(top_layout)
        layout.addWidget(self.sc)
        layout.addLayout(bot_layout)

        # self.sc.load_matrix(self.matrix, alpha=self.alpha_slider.value())
        # self.sc.draw()
        self.update_plot_signal()

        self.setLayout(layout)

    def update_plot_signal(self):
        indices = []
        colors = []
        cut_offs = []

        for o in self.options:
            idx, is_checked, color, cut_off = o.get_options()
            if is_checked:
                indices.append(idx)
                colors.append(color)
                cut_offs.append(cut_off)

        self.sc.load_matrix(self.matrix, indices, colors, cut_offs, self.alpha_slider.value())
        self.sc.draw()


        if len(indices) == 0:
            self.save_btn.setEnabled(False)
        else:
            self.save_btn.setEnabled(True)



    def save_signal(self):
        save_path = save_plt(self.sc.fig, self.chosen_exp_name, "matrix_epoch_" + str(self.displayed_epoch))
        show_save_plot_toast(self, save_path)
