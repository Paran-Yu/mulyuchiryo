import sys
from PyQt5.QtWidgets import *

class SceneSelector(QDialog):
    def __init__(self):
        super().__init__()

    def initUI(self, scenes):
        QLabel("Scene #", self).move(self.width() * 0.1, self.height() * 0.1)

        self.cmbx = QComboBox(self)
        self.cmbx.move(self.width() * 0.4, self.height() * 0.1)
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