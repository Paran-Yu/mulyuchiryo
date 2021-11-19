from PyQt5.QtWidgets import *

class Scale(QDialog):
    def __init__(self, length = 0):
        super().__init__()
        self.length = length

    def initUI(self):
        self.label_length = QLabel("길이(mm)", self)
        self.label_length.move(self.width() * 0.1, self.height() * 0.1)

        self.edit_length = QLineEdit(self)
        self.edit_length.move(self.width() * 0.4, self.height() * 0.1)
        self.edit_length.setText(str(self.length))
        self.edit_length.textChanged.connect(lambda: self.validate(self.edit_length))

        self.btn_OK = QPushButton("OK", self)
        self.btn_OK.move(self.width() * 0.4, self.height() * 0.7)
        self.btn_OK.clicked.connect(self.OK)

        self.btn_cancel = QPushButton("Cancel", self)
        self.btn_cancel.move(self.width() * 0.7, self.height() * 0.7)
        self.btn_cancel.clicked.connect(self.close)

    def OK(self):
        self.accept()

    def validate(self, edit):
        str = edit.text()

        for char in str:
            if not char.isdigit():
                str = str.replace(char, "")

        edit.setText(str)
