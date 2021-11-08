import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Detail():
    def __init__(self, context, parent):
        super(Detail, self).__init__()
        self.widget = QWidget(parent)
        self.context = context

        QLabel("Position", self.widget).move(parent.width() * 0.05, parent.height() * 0.05)
        QLabel("------------------------------------------", self.widget).move(parent.width() * 0.05, parent.height() * 0.06)
        QLabel("x", self.widget).move(parent.width() * 0.05, parent.height() * 0.1 + 5)
        QLabel("y", self.widget).move(parent.width() * 0.55, parent.height() * 0.1 + 5)

        self.x = QLineEdit(self.widget)
        self.x.textChanged.connect(self.changedX)
        self.x.setGeometry(parent.width() * 0.15, parent.height() * 0.1,
                           parent.width() * 0.3, self.x.height())

        self.y = QLineEdit(self.widget)
        self.y.textChanged.connect(self.changedY)
        self.y.setGeometry(parent.width() * 0.65, parent.height() * 0.1,
                           parent.width() * 0.3, self.y.height())

        QLabel("Detail", self.widget).move(parent.width() * 0.05, parent.height() * 0.17)
        QLabel("------------------------------------------", self.widget)\
            .move(parent.width() * 0.05, parent.height() * 0.18)

        self.btn_delete = QPushButton("Delete", self.widget)
        self.btn_delete.setObjectName("btn-delete")
        self.btn_delete.clicked.connect(self.deleteNode)
        self.btn_delete.setStyleSheet("#btn-delete{"
                                       "background-color:white;"
                                       "}"
                                       "#btn-delete:hover{"
                                       "background-color: #D7EDFF;"
                                       "}"
                                       "#btn-delete:pressed{"
                                       "background-color: #C5DCFF;"
                                       "}")
        self.btn_delete.setGeometry(parent.width() * 0.65, parent.height() * 0.7,
                                    parent.width() * 0.3, self.y.height())

    def hide(self):
        self.widget.hide()

    def show(self):
        self.widget.show()

    def changedX(self):
        str = self.x.text()
        if str != "":
            if str.isdigit():
                if len(str) > 1 and str[0] == '0':
                    str = str.replace(str[0], "")
                    self.x.setText(str)

                self.context.main.selected_node.setX(int(self.x.text()))
                self.redraw()
            elif str[0] == '-':
                if len(str) > 1 and str[1:].isdigit():
                    self.context.main.selected_node.setX(int(self.x.text()))
                    self.redraw()
        else:
            self.x.setText("0")
            self.context.main.selected_node.setX(0)
            self.redraw()

    def changedY(self):
        str = self.y.text()
        if str != "":
            if str.isdigit():
                if len(str) > 1 and str[0] == '0':
                    str = str.replace(str[0], "")
                    self.y.setText(str)

                self.context.main.selected_node.setY(int(self.y.text()))
                self.redraw()
            elif str[0] == '-':
                if len(str) > 1 and str[1:].isdigit():
                    self.context.main.selected_node.setY(int(self.y.text()))
                    self.redraw()
        else:
            self.y.setText("0")
            self.context.main.selected_node.setY(0)
            self.redraw()

    def deleteNode(self):

        for i in self.context.main.positions:
            for j in i:
                if j == self.context.main.selected_node:
                    i.remove(j)

        self.redraw()

    def redraw(self):
        self.context.main.eraseCanvas()
        self.context.main.drawCanvas()

class DetailPath(Detail):
    def __init__(self, context, parent):
        super(DetailPath, self).__init__(context, parent)
        QLabel("Cross", self.widget).move(parent.width() * 0.04, parent.height() * 0.22 + 5)

        self.cross = QCheckBox(self.widget)
        self.cross.setGeometry(parent.width() * 0.15, parent.height() * 0.22,
                              parent.width() * 0.3, self.y.height())
        self.cross.setEnabled(False)

class DetailPort(Detail):
    def __init__(self, context, parent):
        super(DetailPort, self).__init__(context, parent)
        QLabel("name", self.widget).move(parent.width() * 0.04, parent.height() * 0.22 + 5)
        QLabel("type", self.widget).move(parent.width() * 0.54, parent.height() * 0.22 + 5)
        QLabel("freq", self.widget).move(parent.width() * 0.04, parent.height() * 0.27 + 5)
        QLabel("vtype", self.widget).move(parent.width() * 0.54-5, parent.height() * 0.27 + 5)

        self.name = QLineEdit("port", self.widget)
        self.name.setGeometry(parent.width() * 0.15, parent.height() * 0.22,
                               parent.width() * 0.3, self.y.height())

        self.type = QComboBox(self.widget)
        self.type.setGeometry(parent.width() * 0.65, parent.height() * 0.22,
                              parent.width() * 0.3, self.y.height())
        self.type.setStyleSheet("background-color: white;")
        self.type.addItem("load")
        self.type.addItem("unload")
        self.type.addItem("both")

        self.freq = QLineEdit("8899", self.widget)
        self.freq.setGeometry(parent.width() * 0.15, parent.height() * 0.27,
                              parent.width() * 0.3, self.y.height())

        self.vtype = QComboBox(self.widget)
        self.vtype.setGeometry(parent.width() * 0.65, parent.height() * 0.27,
                              parent.width() * 0.3, self.y.height())
        self.vtype.setStyleSheet("background-color: white;")
        self.vtype.addItem("저상형")
        self.vtype.addItem("Reel Direct")
        self.vtype.setCurrentIndex(0)

class DetailWaitPoint(Detail):
    def __init__(self, context, parent):
        super(DetailWaitPoint, self).__init__(context, parent)

class SideBar(QWidget):
    def __init__(self, context, parent):
        super(SideBar, self).__init__()
        self.context = context
        self.widget = QWidget(parent)
        self.widget.setGeometry(parent.width() * 0.8, 0,
                         parent.width() * 0.2, parent.height())
        self.widget.setObjectName("side-bar")
        self.widget.setStyleSheet("#side-bar{"
                                    "border-left: 2px solid #CCCCCC;"
                                    "background-color: #DDDDDD;"
                                    "}")
        self.path = DetailPath(context, self.widget)
        self.port = DetailPort(context, self.widget)
        self.wait_point = DetailWaitPoint(context, self.widget)
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
        self.details[self.current].x.setText(str(obj.x))
        self.details[self.current].y.setText(str(obj.y))
