from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Scale(QDialog):
    def __init__(self):
        super().__init__()

    def initUI(self):
        self.label_mm = QLabel("길이(mm)", self)
        self.label_mm.move(self.width() * 0.1, self.height() * 0.1)

        self.edit_mm = QLineEdit(self)
        self.edit_mm.move(self.width() * 0.4, self.height() * 0.1)

        self.btn_OK = QPushButton("OK", self)
        self.btn_OK.move(self.width() * 0.4, self.height() * 0.5)
        self.btn_OK.clicked.connect(self.OK)

        self.btn_cancel = QPushButton("Cancel", self)
        self.btn_cancel.move(self.width() * 0.7, self.height() * 0.5)
        self.btn_cancel.clicked.connect(self.close)

    def OK(self):
        self.accept()