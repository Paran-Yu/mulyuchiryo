import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class DetailPath(QWidget):
    def __init__(self, parent):
        super(DetailPath, self).__init__()
        self.widget = QWidget(parent)
        #self.widget.setStyleSheet("background-color:white;")
        QLabel("Position", self.widget).move(parent.width() * 0.05, parent.height() * 0.05)
        QLabel("------------------------------------------", self.widget).move(parent.width() * 0.05, parent.height() * 0.06)
        lbl_x = QLabel("x", self.widget)
        lbl_y = QLabel("y", self.widget)

        lbl_x.move(parent.width() * 0.05, parent.height() * 0.1 + 5)
        lbl_y.move(parent.width() * 0.55, parent.height() * 0.1 + 5)

        QLabel("Detail", self.widget).move(parent.width() * 0.05, parent.height() * 0.17)
        QLabel("------------------------------------------", self.widget).move(parent.width() * 0.05,                                                                      parent.height() * 0.18)
        lbl_type = QLabel("type", self.widget)

        lbl_type.move(parent.width() * 0.04, parent.height() * 0.22+ 5)

        self.x = QLineEdit(self.widget)
        self.y = QLineEdit(self.widget)
        self.type = QLineEdit(self.widget)

        self.x.setGeometry(parent.width() * 0.15, parent.height() * 0.1,
                           parent.width() * 0.3, self.x.height())
        self.y.setGeometry(parent.width() * 0.65, parent.height() * 0.1,
                           parent.width() * 0.3, self.y.height())
        self.type.setGeometry(parent.width() * 0.15, parent.height() * 0.22,
                           parent.width() * 0.3, self.y.height())

        self.x.setText("12")
        self.y.setText("34")

    def hide(self):
        self.widget.hide()

    def show(self):
        self.widget.show()

class DetailPort(QWidget):
    def __init__(self, parent):
        super(DetailPort, self).__init__()
        self.widget = QWidget(parent)
        #self.widget.setStyleSheet("background-color:white;")
        QLabel("Position", self.widget).move(parent.width() * 0.05, parent.height() * 0.05)
        QLabel("------------------------------------------", self.widget).move(parent.width() * 0.05, parent.height() * 0.06)
        lbl_x = QLabel("x", self.widget)
        lbl_y = QLabel("y", self.widget)

        lbl_x.move(parent.width() * 0.05, parent.height() * 0.1 + 5)
        lbl_y.move(parent.width() * 0.55, parent.height() * 0.1 + 5)

        QLabel("Detail", self.widget).move(parent.width() * 0.05, parent.height() * 0.17)
        QLabel("------------------------------------------", self.widget).move(parent.width() * 0.05,
                                                                               parent.height() * 0.18)
        lbl_type = QLabel("type", self.widget)

        lbl_type.move(parent.width() * 0.04, parent.height() * 0.22+ 5)

        self.x = QLineEdit(self.widget)
        self.y = QLineEdit(self.widget)
        self.type = QLineEdit(self.widget)

        self.x.setGeometry(parent.width() * 0.15, parent.height() * 0.1,
                           parent.width() * 0.3, self.x.height())
        self.y.setGeometry(parent.width() * 0.65, parent.height() * 0.1,
                           parent.width() * 0.3, self.y.height())
        self.type.setGeometry(parent.width() * 0.15, parent.height() * 0.22,
                           parent.width() * 0.3, self.y.height())

    def hide(self):
        self.widget.hide()

    def show(self):
        self.widget.show()

class DetailWaitPoint(QWidget):
    def __init__(self, parent):
        super(DetailWaitPoint, self).__init__()
        self.widget = QWidget(parent)
        #self.widget.setStyleSheet("background-color:white;")
        QLabel("Position", self.widget).move(parent.width() * 0.05, parent.height() * 0.05)
        QLabel("------------------------------------------", self.widget).move(parent.width() * 0.05, parent.height() * 0.06)
        lbl_x = QLabel("x", self.widget)
        lbl_y = QLabel("y", self.widget)

        lbl_x.move(parent.width() * 0.05, parent.height() * 0.1 + 5)
        lbl_y.move(parent.width() * 0.55, parent.height() * 0.1 + 5)

        QLabel("Detail", self.widget).move(parent.width() * 0.05, parent.height() * 0.17)
        QLabel("------------------------------------------", self.widget).move(parent.width() * 0.05,
                                                                               parent.height() * 0.18)
        lbl_type = QLabel("type", self.widget)

        lbl_type.move(parent.width() * 0.04, parent.height() * 0.22+ 5)

        self.x = QLineEdit(self.widget)
        self.y = QLineEdit(self.widget)
        self.type = QLineEdit(self.widget)

        self.x.setGeometry(parent.width() * 0.15, parent.height() * 0.1,
                           parent.width() * 0.3, self.x.height())
        self.y.setGeometry(parent.width() * 0.65, parent.height() * 0.1,
                           parent.width() * 0.3, self.y.height())
        self.type.setGeometry(parent.width() * 0.15, parent.height() * 0.22,
                           parent.width() * 0.3, self.y.height())

    def hide(self):
        self.widget.hide()

    def show(self):
        self.widget.show()

class SideBar(QWidget):
    def __init__(self, parent):
        super(SideBar, self).__init__()
        self.widget = QWidget(parent)
        self.widget.setGeometry(parent.width() * 0.8, 0,
                         parent.width() * 0.2, parent.height())
        self.widget.setObjectName("side-bar")
        self.widget.setStyleSheet("#side-bar{"
                                    "border-left: 2px solid #CCCCCC;"
                                    "background-color: #DDDDDD;"
                                    "}")
        self.path = DetailPath(self.widget)
        self.port = DetailPort(self.widget)
        self.wait_point = DetailWaitPoint(self.widget)
        self.details = [
            self.path,
            self.port,
            self.wait_point,
        ]

        for idx, detail in enumerate(self.details):
            detail.hide()

        self.current = 0
        self.widget.hide()

    def getDetail(self, idx):
        self.hide(self.current)
        self.current = idx
        self.show(self.current)

    def hide(self, idx):
        self.details[idx].hide()

    def show(self, idx):
        self.details[idx].show()

    def setDetail(self, obj):
        self.details[self.current].x.setText(obj.x)
        self.details[self.current].y.setText(obj.y)
