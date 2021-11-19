import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Detail():
    def __init__(self, context, parent):
        super(Detail, self).__init__()
        self.widget = QWidget(parent)
        self.context = context

        QLabel("ID: ", self.widget).move(parent.width() * 0.05, parent.height() * 0.01)
        self.label_id = QLabel(self.widget)
        self.label_id.setGeometry(parent.width() * 0.1, parent.height() * 0.01, 100, 15)
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

        QLabel("Connected Node", self.widget).move(parent.width() * 0.05, parent.height() * 0.17)
        QLabel("------------------------------------------", self.widget)\
            .move(parent.width() * 0.05, parent.height() * 0.18)

        self.connected_node_list = QListWidget(self.widget)
        self.connected_node_list.setGeometry(parent.width() * 0.05, parent.height() * 0.20,
                                             parent.width() * 0.9, parent.height() * 0.1)
        self.connected_node_list.itemClicked.connect(self.selectPath)

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
        self.btn_delete.setGeometry(parent.width() * 0.65, parent.height() * 0.9,
                                    parent.width() * 0.3, self.y.height())

        QLabel("Detail", self.widget).move(parent.width() * 0.05, parent.height() * 0.33)
        QLabel("------------------------------------------", self.widget) \
            .move(parent.width() * 0.05, parent.height() * 0.34)

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

                self.context.main.selected_node.X = int(self.x.text())
                self.redraw()
            elif str[0] == '-':
                if len(str) > 1 and str[1:].isdigit():
                    self.context.main.selected_node.X = int(self.x.text())
                    self.redraw()
        else:
            self.x.setText("0")
            self.context.main.selected_node.X = 0
            self.redraw()

    def changedY(self):
        str = self.y.text()
        if str != "":
            if str.isdigit():
                if len(str) > 1 and str[0] == '0':
                    str = str.replace(str[0], "")
                    self.y.setText(str)

                self.context.main.selected_node.Y = (int(self.y.text()))
                self.redraw()
            elif str[0] == '-':
                if len(str) > 1 and str[1:].isdigit():
                    self.context.main.selected_node.Y = (int(self.y.text()))
                    self.redraw()
        else:
            self.y.setText("0")
            self.context.main.selected_node.Y = 0
            self.redraw()

    def deleteNode(self):
        if not self.context.main.selected_node:
            return

        while self.connected_node_list.count():
            _, p = self.connected_node_list.item(0).text().split('To: ')
            p = list(map(int, p.split(",")))
            p = QPoint(p[0], p[1])

            self.removePath(p)

        for i in self.context.main.positions:
            for j in i:
                if j == self.context.main.selected_node:
                    i.remove(j)
                    del j
                    self.context.main.selected_node = None

        self.redraw()

    def redraw(self):
        self.context.main.eraseCanvas()
        self.context.main.drawCanvas()

    def setDetail(self, obj):
        self.x.setText(str(obj.X))
        self.y.setText(str(obj.Y))
        self.label_id.setText(str(obj.NUM))
        self.updatePath()

    def updatePath(self):
        self.connected_node_list.clear()

        p = self.context.main.selected_node
        for path in self.context.main.paths:
            if p == path.start:
                self.connected_node_list.addItem("To: " + str(path.end.X) + "," + str(path.end.Y))
            if p == path.end:
                self.connected_node_list.addItem("To: " + str(path.start.X)+ "," + str(path.start.Y))

    def selectPath(self):
        _, p = self.connected_node_list.currentItem().text().split('To: ')
        p = list(map(int, p.split(",")))
        p = QPoint(p[0], p[1])

        self.removePath(p)

    def removePath(self, p):
        for path in self.context.main.paths:
            if p in [QPoint(path.start.X, path.start.Y), QPoint(path.end.X, path.end.Y)]:
                self.context.main.paths.remove(path)

                path.start.count -= 1
                if path.start.count < 3:
                    path.start.isCross = False
                path.end.count -= 1
                if path.end.count < 3:
                    path.end.isCross = False

                del path

                self.updatePath()
                self.redraw()

class DetailPath(Detail):
    def __init__(self, context, parent):
        super(DetailPath, self).__init__(context, parent)
        QLabel("Cross", self.widget).move(parent.width() * 0.04, parent.height() * 0.38 + 5)

        self.cross = QCheckBox(self.widget)
        self.cross.setGeometry(parent.width() * 0.15, parent.height() * 0.38,
                              parent.width() * 0.3, self.y.height())
        self.cross.setEnabled(False)

    def setDetail(self, obj):
        super().setDetail(obj)
        self.setCross(obj)

    def setCross(self, obj):
        self.cross.setChecked(obj.isCross)

    def removePath(self, p):
        super().removePath(p)
        self.setCross(self.context.main.selected_node)

class DetailPort(Detail):
    def __init__(self, context, parent):
        super(DetailPort, self).__init__(context, parent)
        QLabel("name", self.widget).move(parent.width() * 0.04, parent.height() * 0.38 + 5)
        QLabel("type", self.widget).move(parent.width() * 0.54, parent.height() * 0.38 + 5)
        QLabel("freq", self.widget).move(parent.width() * 0.04, parent.height() * 0.43 + 5)
        QLabel("vtype", self.widget).move(parent.width() * 0.54-5, parent.height() * 0.43 + 5)
        QLabel("Unload Ports", self.widget).move(parent.width() * 0.05, parent.height() * 0.49)
        QLabel("------------------------------------------", self.widget) \
            .move(parent.width() * 0.05, parent.height() * 0.50)

        self.name = QLineEdit("port", self.widget)
        self.name.setGeometry(parent.width() * 0.15, parent.height() * 0.38,
                               parent.width() * 0.3, self.y.height())
        self.name.textChanged.connect(self.changedName)

        self.type = QComboBox(self.widget)
        self.type.setGeometry(parent.width() * 0.65, parent.height() * 0.38,
                              parent.width() * 0.3, self.y.height())
        self.type.setStyleSheet("background-color: white;")
        self.type.addItem("load")
        self.type.addItem("unload")
        self.type.addItem("both")
        self.type.currentIndexChanged.connect(self.changedType)

        self.freq = QLineEdit("8899", self.widget)
        self.freq.setGeometry(parent.width() * 0.15, parent.height() * 0.43,
                              parent.width() * 0.3, self.y.height())
        self.freq.textChanged.connect(self.changedFreq)

        self.vtype = QComboBox(self.widget)
        self.vtype.setGeometry(parent.width() * 0.65, parent.height() * 0.43,
                              parent.width() * 0.3, self.y.height())
        self.vtype.setStyleSheet("background-color: white;")
        self.vtype.addItem("저상형")
        self.vtype.addItem("Reel Direct")
        self.vtype.setCurrentIndex(-1)
        self.vtype.currentIndexChanged.connect(self.changedVtype)

        QLabel("Ports", self.widget).move(parent.width() * 0.05, parent.height() * 0.52)
        self.port_list = QListWidget(self.widget)
        self.port_list.setGeometry(parent.width() * 0.05, parent.height() * 0.54,
                                   parent.width() * 0.4, parent.height() * 0.3)

        QLabel("Connected Ports", self.widget).move(parent.width() * 0.55, parent.height() * 0.52)
        self.connected_port_list = QListWidget(self.widget)
        self.connected_port_list.setGeometry(parent.width() * 0.55, parent.height() * 0.54,
                                             parent.width() * 0.4, parent.height() * 0.3)

        self.port_list.itemClicked.connect(self.addList)
        self.connected_port_list.itemClicked.connect(self.removeList)

    def changedName(self):
        if self.context.main.selected_node:
            self.context.main.selected_node.PORT_NAME = self.name.text()

    def changedType(self):
        if self.context.main.selected_node:
            self.context.main.selected_node.TYPE = self.type.currentText()

    def changedFreq(self):
        if self.context.main.selected_node:
            str = self.freq.text()
            if str != "":
                if str.isdigit():
                    if len(str) > 1 and str[0] == '0':
                        str = str.replace(str[0], "")
                else:
                    str = "0"
            else:
                str = "0"

            self.context.main.selected_node.FREQ = int(str)
            self.freq.setText(str)

    def changedVtype(self):
        if self.context.main.selected_node:
            self.context.main.selected_node.V_TYPE = self.vtype.currentText()

    def setDetail(self, port):
        super().setDetail(port)
        if port.TYPE:
            self.type.setCurrentIndex(self.type.findText(port.TYPE))
        if port.V_TYPE:
            self.vtype.setCurrentIndex(self.vtype.findText(port.V_TYPE))
        else:
            self.vtype.setCurrentIndex(-1)
        self.name.setText(port.PORT_NAME)
        self.freq.setText(str(port.FREQ))
        self.updateList()

    def updateList(self):
        self.port_list.clear()
        self.connected_port_list.clear()

        port = self.context.main.selected_node
        for p in self.context.main.ports:
            if p.TYPE != "unload" or p.NUM == port.NUM:
                continue
            fail = True

            for unload_ports in port.UNLOAD_LIST:
                if p.NUM == int(unload_ports):
                    self.connected_port_list.addItem(str(p.NUM) + '\n' + p.PORT_NAME)
                    fail = False

            if fail:
                self.port_list.addItem(str(p.NUM) + '\n' + p.PORT_NAME)

    def addList(self):
        selected_id, selected_name = self.port_list.currentItem().text().split('\n')

        if selected_id:
            self.context.main.selected_node.UNLOAD_LIST.append(selected_id)
            self.updateList()

    def removeList(self):
        selected_id, selected_name = self.connected_port_list.currentItem().text().split('\n')

        if selected_id:
            self.context.main.selected_node.UNLOAD_LIST.remove(selected_id)
            self.updateList()

    def deleteNode(self):
        super().deleteNode()
        self.connected_node_list.clear()
        self.connected_port_list.clear()
        self.port_list.clear()

class DetailWaitPoint(Detail):
    def __init__(self, context, parent):
        super(DetailWaitPoint, self).__init__(context, parent)
        QLabel("name", self.widget).move(parent.width() * 0.04, parent.height() * 0.38 + 5)
        QLabel("charge", self.widget).move(parent.width() * 0.54, parent.height() * 0.38 + 5)

        self.name = QLineEdit("port", self.widget)
        self.name.setGeometry(parent.width() * 0.15, parent.height() * 0.38,
                              parent.width() * 0.3, self.y.height())
        self.name.textChanged.connect(self.changedName)

        self.charge = QCheckBox(self.widget)
        self.charge.setGeometry(parent.width() * 0.7, parent.height() * 0.38,
                               parent.width() * 0.3, self.y.height())
        self.charge.stateChanged.connect(self.changedCharge)
    def changedName(self):
        if self.context.main.selected_node:
            self.context.main.selected_node.WAIT_NAME = self.name.text()

    def changedCharge(self):
        if self.context.main.selected_node:
            self.context.main.selected_node.CHARGE = self.charge.isChecked()

    def setDetail(self, obj):
        super().setDetail(obj)
        self.charge.setChecked(self.context.main.selected_node.CHARGE)

class DetailVehicle():
    def __init__(self, context, parent):
        super(DetailVehicle, self).__init__()
        self.widget = QWidget(parent)
        self.context = context

        QLabel("ID: ", self.widget).move(parent.width() * 0.05, parent.height() * 0.01)
        self.label_id = QLabel(self.widget)
        self.label_id.setGeometry(parent.width() * 0.1, parent.height() * 0.01, 100, 15)
        QLabel("Position", self.widget).move(parent.width() * 0.05, parent.height() * 0.05)
        QLabel("------------------------------------------", self.widget).move(parent.width() * 0.05, parent.height() * 0.06)
        QLabel("node", self.widget).move(parent.width() * 0.05-5, parent.height() * 0.1 + 5)
        QLabel("angle", self.widget).move(parent.width() * 0.55 - 5, parent.height() * 0.1 + 5)
        QLabel("x", self.widget).move(parent.width() * 0.05, parent.height() * 0.15 + 5)
        QLabel("y", self.widget).move(parent.width() * 0.55, parent.height() * 0.15 + 5)

        self.node = QLineEdit(self.widget)
        self.node.setGeometry(parent.width() * 0.15, parent.height() * 0.10,
                              parent.width() * 0.3, self.node.height())

        self.angle = QLineEdit(self.widget)
        self.angle.setGeometry(parent.width() * 0.65, parent.height() * 0.10,
                              parent.width() * 0.3, self.node.height())
        self.angle.textChanged.connect(self.changedAngle)

        self.x = QLineEdit(self.widget)
        self.x.setEnabled(False)
        self.x.setGeometry(parent.width() * 0.15, parent.height() * 0.15,
                           parent.width() * 0.3, self.x.height())

        self.y = QLineEdit(self.widget)
        self.y.setEnabled(False)
        self.y.setGeometry(parent.width() * 0.65, parent.height() * 0.15,
                           parent.width() * 0.3, self.y.height())

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
        self.btn_delete.setGeometry(parent.width() * 0.65, parent.height() * 0.9,
                                    parent.width() * 0.3, self.y.height())

        QLabel("Detail", self.widget).move(parent.width() * 0.05, parent.height() * 0.33)
        QLabel("------------------------------------------", self.widget) \
            .move(parent.width() * 0.05, parent.height() * 0.34)

        QLabel("name", self.widget).move(parent.width() * 0.04, parent.height() * 0.38 + 5)
        QLabel("type", self.widget).move(parent.width() * 0.54, parent.height() * 0.38 + 5)

        self.name = QLineEdit("port", self.widget)
        self.name.setGeometry(parent.width() * 0.15, parent.height() * 0.38,
                              parent.width() * 0.3, self.y.height())
        self.name.textChanged.connect(self.changedName)

        self.type = QComboBox(self.widget)
        self.type.setGeometry(parent.width() * 0.65, parent.height() * 0.38,
                              parent.width() * 0.3, self.y.height())
        self.type.setStyleSheet("background-color: white;")
        self.type.addItem("저상형")
        self.type.addItem("Reel Direct")
        self.type.currentIndexChanged.connect(self.changedType)

    def hide(self):
        self.widget.hide()

    def show(self):
        self.widget.show()

    def changedName(self):
        if self.context.main.selected_vehicle:
            self.context.main.selected_vehicle.NAME = self.name.text()

    def changedAngle(self):
        if self.angle.text():
            str = self.angle.text()

            for char in str:
                if not char.isdigit():
                    str = str.replace(char, "")

            if self.context.main.selected_vehicle:
                self.context.main.selected_vehicle.angle = int(str)

            self.angle.setText(str)

    def changedType(self):
        if self.context.main.selected_vehicle:
            self.context.main.selected_vehicle.TYPE = self.type.currentText()

    def deleteNode(self):
        if not self.context.main.selected_vehicle:
            return

        for v in self.context.main.vehicles:
            if v == self.context.main.selected_vehicle:
                self.context.main.vehicles.remove(v)
                del v
                self.context.main.selected_vehicle = None

        self.redraw()

    def redraw(self):
        self.context.main.eraseCanvas()
        self.context.main.drawCanvas()

    def setDetail(self, obj):
        self.node.setText(str(obj.node))
        self.x.setText(str(obj.x))
        self.y.setText(str(obj.y))
        self.label_id.setText(str(obj.NUM))
        self.name.setText(obj.NAME)
        self.angle.setText(str(obj.angle))

        if obj.TYPE:
            self.type.setCurrentIndex(self.type.findText(obj.TYPE))
        else:
            self.type.setCurrentIndex(-1)

        self.redraw()


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
        self.vehicle = DetailVehicle(context, self.widget)
        self.details = [
            self.path,
            self.port,
            self.wait_point,
            self.vehicle,
        ]

        for idx, detail in enumerate(self.details):
            detail.hide()

        self.current = 0
        self.widget.hide()

    def getDetail(self, idx):
        if idx == 4:
            idx -= 1
        self.hide(self.current)
        self.current = idx
        self.show(self.current)

    def hide(self, idx):
        self.details[idx].hide()

    def show(self, idx):
        self.details[idx].show()

    def setDetail(self, obj):
        self.details[self.current].setDetail(obj)
