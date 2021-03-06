from PyQt5.QtWidgets import *

class OperationData(QDialog):
    def __init__(self):
        super().__init__()

    def initUI(self, capa, speed):
        self.label_capa = QLabel("하루 반송량", self)
        self.label_capa.move(self.width() * 0.1, self.height() * 0.1)

        self.edit_capa = QLineEdit(self)
        self.edit_capa.move(self.width() * 0.4, self.height() * 0.1)
        self.edit_capa.setText(str(capa))
        self.edit_capa.textChanged.connect(lambda: self.validate(self.edit_capa))

        self.label_speed = QLabel("시뮬레이션 속도", self)
        self.label_speed.move(self.width() * 0.1, self.height() * 0.3)

        # self.edit_speed = QLineEdit(self)
        self.edit_speed = QComboBox(self)
        self.edit_speed.move(self.width() * 0.4, self.height() * 0.3)
        self.edit_speed.addItem("1")
        self.edit_speed.addItem("2")
        self.edit_speed.addItem("4")
        self.edit_speed.addItem("8")
        self.edit_speed.addItem("10")
        self.edit_speed.addItem("20")
        self.edit_speed.addItem("50")
        self.edit_speed.addItem("100")
        self.edit_speed.setStyleSheet("background-color: white;")
        # self.edit_speed.setText(str(speed))
        # self.edit_speed.textChanged.connect(lambda: self.validate(self.edit_speed))

        QLabel("화면 출력", self).move(self.width() * 0.1, self.height() * 0.5)
        self.chbx = QCheckBox(self)
        self.chbx.move(self.width() * 0.4, self.height() * 0.5)
        self.chbx.setChecked(True)

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