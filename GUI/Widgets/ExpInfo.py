from PySide6 import QtWidgets
from PySide6.QtWidgets import QFormLayout, QLabel
from poetry.console.commands import self

from GUI.Logic.LogicHandler import LogicHandler


class ExpInfo(QtWidgets.QWidget):
    __logic_handler: LogicHandler

    def __init__(self, logic_handler: LogicHandler):
        super().__init__()

        self.__logic_handler = logic_handler
        if self.__logic_handler.param_handler is not None:
            ph = self.__logic_handler.param_handler

            main_lay = QtWidgets.QVBoxLayout()

            col_lay = QtWidgets.QHBoxLayout()

            layout = QFormLayout()
            self.experiment_name = QLabel(ph.experiment_name.split("/")[-1])
            layout.addRow("Full experiment name:", self.experiment_name)
            self.num_phenotypes = QLabel(str(ph.num_phenotypes))
            layout.addRow("Number of phenotypes:", self.num_phenotypes)
            self.num_dim = QLabel(str(ph.num_dim))
            layout.addRow("Number of dimensions:", self.num_dim)
            self.num_epochs = QLabel(str(ph.num_epochs))
            layout.addRow("Number of epochs:", self.num_epochs)
            self.len_pop = QLabel(str(ph.population_length))
            layout.addRow("Length of population:", self.len_pop)


            self.layout1 = QFormLayout()
            self.problem_name = QLabel(str(ph.problem_name))
            self.layout1.addRow("Name of problem:", self.problem_name)

            self.layout1.addRow("Problem Parameters:", QLabel(""))
            self.problem_params = []

            for k, v in ph.problem_params.items():
                self.problem_params.append(QLabel(str(v)))
                self.layout1.addRow(str(k) + ":", self.problem_params[-1])

            col_lay.addLayout(layout)
            col_lay.addLayout(self.layout1)
            main_lay.addLayout(col_lay)

            col_lay_2 = QtWidgets.QHBoxLayout()

            self.layout2 = QFormLayout()
            self.neighbourhood_type = QLabel(ph.neighbourhood_type)
            self.layout2.addRow("Neighbourhood Type:", self.neighbourhood_type)
            self.mortality_strategy = QLabel(ph.mortality_strategy)
            self.layout2.addRow("Mortality Type:", self.mortality_strategy)
            if ph.mortality_strategy == "Probabilistic":
                self.mortality_rate = QLabel(str(ph.mortality_rate))
                self.layout2.addRow("Mortality Rate:", QLabel(self.mortality_rate))
            else:
                self.mortality_rate = QLabel(str(-1))

            layout3 = QFormLayout()
            self.spatiality_type = QLabel(ph.spatiality_strategy.name)
            layout3.addRow("Spatiality Type:", self.spatiality_type)

            col_lay_2.addLayout(self.layout2)
            col_lay_2.addLayout(layout3)

            main_lay.addLayout(col_lay_2)

            self.setLayout(main_lay)


    def refresh_layout(self):
        ph = self.__logic_handler.param_handler

        self.experiment_name.clear()
        self.experiment_name.setText(ph.experiment_name.split("/")[-1])

        self.num_phenotypes.clear()
        self.num_phenotypes.setText(str(ph.num_phenotypes))

        self.num_dim.clear()
        self.num_dim.setText(str(ph.num_dim))

        self.num_epochs.clear()
        self.num_epochs.setText(str(ph.num_epochs))

        self.len_pop.clear()
        self.len_pop.setText(str(ph.population_length))

        self.problem_name.clear()
        self.problem_name.setText(ph.problem_name)


        for i in range(len(self.problem_params)):
            self.layout1.removeRow(self.problem_params[i])

        self.problem_params = []

        for k, v in ph.problem_params.items():
            self.problem_params.append(QLabel(str(v)))
            self.layout1.addRow(str(k) + ":", self.problem_params[-1])

        self.neighbourhood_type.clear()
        self.neighbourhood_type.setText(ph.neighbourhood_type)

        self.mortality_strategy.clear()
        self.mortality_strategy.setText(ph.mortality_strategy)

        if ph.mortality_strategy == "Probabilistic":
            self.mortality_rate.clear()
            self.mortality_rate.setText(str(ph.mortality_rate))

            if self.mortality_rate.text() == "-1":
                self.layout2.addRow("Mortality Rate:", QLabel(self.mortality_rate))

        else:
            if self.mortality_rate.text() != "-1":
                self.layout2.removeRow(self.mortality_rate)
                self.mortality_rate.clear()
                self.mortality_rate.setText(str(-1))


        self.spatiality_type.clear()
        self.spatiality_type.setText(ph.spatiality_strategy.name)
