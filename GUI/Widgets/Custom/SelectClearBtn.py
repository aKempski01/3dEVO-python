from PySide6 import QtWidgets
from PySide6.QtWidgets import QPushButton


class SelectClearBtn(QtWidgets.QWidget):
    """
    Custom Qt Widget to show a power bar and dial.
    Demonstrating compound and custom-drawn widget.
    """

    def __init__(self, select_function, clear_function):
        super().__init__()

        layout = QtWidgets.QHBoxLayout()


        self.button_select_all = QPushButton("Select all")
        self.button_select_all.pressed.connect(select_function)

        self.clear_selection_btn = QPushButton("Clear selection")
        self.clear_selection_btn.pressed.connect(clear_function)

        layout.addWidget(self.button_select_all)
        layout.addWidget(self.clear_selection_btn)

        self.setLayout(layout)
