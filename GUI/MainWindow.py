from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QStackedLayout

from GUI.Logic.LogicHandler import LogicHandler
from GUI.Widgets.AVGPlotDisplayer import AVGPlotDisplayer
from GUI.Widgets.AVGTimeCourse import AVGTimeCourseDisplay
from GUI.Widgets.ExpInfo import ExpInfo
from GUI.Widgets.PlotDisplayer import PlotDisplayer
from GUI.Widgets.TimeCourseDisplay import TimeCourseDisplay


class MainWindow(QtWidgets.QWidget):

    logic_handler: LogicHandler


    def __init__(self):
        super().__init__()

        self.logic_handler = LogicHandler()
        self.plot_displayer = PlotDisplayer(self.logic_handler)
        self.avg_plot_displayer = AVGPlotDisplayer(self.logic_handler)
        self.exp_info = ExpInfo(self.logic_handler)
        self.time_course = TimeCourseDisplay(self.logic_handler)
        self.avg_time_course = AVGTimeCourseDisplay(self.logic_handler)

        self.outerLayout = QtWidgets.QVBoxLayout(self)
        self.top_layout = QtWidgets.QHBoxLayout()
        self.stackedLayout = QStackedLayout()




        self.exp_options_combo = QtWidgets.QComboBox()
        self.exp_options_combo.addItems(self.logic_handler.experiment_list)
        self.exp_options_combo.setCurrentIndex(0)
        self.exp_options_combo.currentTextChanged.connect(self.switch_experiment)


        self.exp_info_btn = QtWidgets.QPushButton("Experiment Information")
        self.exp_info_btn.clicked.connect(lambda: self.switch_page(0))

        self.plot_btn = QtWidgets.QPushButton("Plot Game Array")
        self.plot_btn.clicked.connect(lambda: self.switch_page(1))

        self.avg_plot_btn = QtWidgets.QPushButton("Average Game Array")
        self.avg_plot_btn.clicked.connect(lambda: self.switch_page(2))

        self.time_course_btn = QtWidgets.QPushButton("Time Course Plot")
        self.time_course_btn.clicked.connect(lambda: self.switch_page(3))

        self.avg_time_course_btn = QtWidgets.QPushButton("Avg. Time Course Plot")
        self.avg_time_course_btn.clicked.connect(lambda: self.switch_page(4))


        self.top_layout.addWidget(self.exp_options_combo)
        self.top_layout.addWidget(self.exp_info_btn)
        self.top_layout.addWidget(self.plot_btn)
        self.top_layout.addWidget(self.avg_plot_btn)
        self.top_layout.addWidget(self.time_course_btn)
        self.top_layout.addWidget(self.avg_time_course_btn)


        self.top_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.stackedLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.stackedLayout.addWidget(self.exp_info)
        self.stackedLayout.addWidget(self.plot_displayer)
        self.stackedLayout.addWidget(self.avg_plot_displayer)
        self.stackedLayout.addWidget(self.time_course)
        self.stackedLayout.addWidget(self.avg_time_course)


        self.outerLayout.addLayout(self.top_layout)
        self.outerLayout.addLayout(self.stackedLayout)



    def switch_page(self, idx: int):
        if idx == 0:
            self.exp_info.refresh_layout()

        if idx == 1:
            self.plot_displayer.refresh_layout()

        if idx == 2:
            self.avg_plot_displayer.refresh_layout()

        if idx == 3:
            self.time_course.refresh_layout()

        if idx == 4:
            self.avg_time_course.refresh_layout()

        self.stackedLayout.setCurrentIndex(idx)


    def switch_experiment(self, name: str):
        self.logic_handler.load_experiment(name)

        if self.stackedLayout.currentIndex() == 0:
            self.exp_info.refresh_layout()

        if self.stackedLayout.currentIndex() == 1:
            self.plot_displayer.refresh_layout()

        if self.stackedLayout.currentIndex() == 2:
            self.avg_plot_displayer.refresh_layout()

        if self.stackedLayout.currentIndex() == 3:
            self.time_course.refresh_layout()

        if self.stackedLayout.currentIndex() == 4:
            self.avg_time_course.refresh_layout()
