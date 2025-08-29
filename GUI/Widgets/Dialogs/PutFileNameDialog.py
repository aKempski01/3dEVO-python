from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QLineEdit


class CustomDialog(QDialog):
    file_name: str = ""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Save Plot File")

        QBtn = (
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        message = QLabel("Please, put the plot file name below.")
        file_name_edit = QLineEdit()

        file_name_edit.setPlaceholderText("Put the plot file name.")
        file_name_edit.textChanged.connect(self.text_changed)

        layout.addWidget(message)
        layout.addWidget(file_name_edit)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)


    def text_changed(self, text: str):
        self.file_name = text


    def get_file_name(self):
        if '.' in self.file_name:
            self.file_name = self.file_name.split('.')[0]
        return self.file_name

