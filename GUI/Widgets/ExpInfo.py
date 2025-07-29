from PySide6 import QtWidgets
from PySide6.QtWidgets import QFormLayout, QLabel

from GUI.Logic.LogicHandler import LogicHandler


class ExpInfo(QtWidgets.QWidget):
    __logic_handler: LogicHandler

    def __init__(self, logic_handler: LogicHandler):
        super().__init__()

        self.__logic_handler = logic_handler
        if self.__logic_handler.param_handler is not None:
            self.init_layout()

    def init_layout(self):

        ph = self.__logic_handler.param_handler

        main_lay = QtWidgets.QVBoxLayout()

        col_lay = QtWidgets.QHBoxLayout()

        layout = QFormLayout()
        layout.addRow("Full experiment name:", QLabel(ph.experiment_name.split("/")[-1]))
        layout.addRow("Number of phenotypes:", QLabel(str(ph.num_phenotypes)))
        layout.addRow("Number of dimensions:", QLabel(str(ph.num_dim)))
        layout.addRow("Number of epochs:", QLabel(str(ph.num_epochs)))
        layout.addRow("Length of population:", QLabel(str(ph.population_length)))

        layout1 = QFormLayout()

        layout1.addRow("Name of problem:", QLabel(str(ph.problem_name)))

        layout1.addRow("Problem Parameters:", QLabel(""))

        for k, v in ph.problem_params.items():
            layout1.addRow(str(k) + ":", QLabel(str(v)))


        col_lay.addLayout(layout)
        col_lay.addLayout(layout1)
        main_lay.addLayout(col_lay)

        col_lay_2 = QtWidgets.QHBoxLayout()

        layout2 = QFormLayout()
        layout2.addRow("Neighbourhood Type:", QLabel(ph.neighbourhood_type))
        layout2.addRow("Mortality Type:", QLabel(ph.mortality_strategy))
        if ph.mortality_strategy == "Probabilistic":
            layout2.addRow("Mortality Rate:", QLabel(str(ph.mortality_rate)))

        layout3 = QFormLayout()
        layout3.addRow("Spatiality Type:", QLabel(ph.spatiality_strategy.name))

        col_lay_2.addLayout(layout2)
        col_lay_2.addLayout(layout3)

        main_lay.addLayout(col_lay_2)

        self.setLayout(main_lay)

