from PyQt5.QtWidgets import *
from classes import Vehicle

def AddVehicle(num, type):
    v_name = "V"
    if num<10:
        v_name += "0" + str(num)
    else:
        v_name += str(num)

    v = Vehicle(v_name)

    if type == "저상형":
        v.NUM = num
        v.TYPE = "저상형"
        v.WIDTH = 900
        v.HEIGHT = 700
        v.DIAGONAL = 1140

    elif type == "Reel Direct":
        v.NUM = num
        v.TYPE = "Reel Direct"
        v.WIDTH = 1700
        v.HEIGHT = 1400
        v.DIAGONAL = 2200

    return v

class VehicleEditor(QDialog):
    def __init__(self, context, vehicles):
        super().__init__()
        self.context = context
        self.vehicles = vehicles

    def initUI(self):
        QLabel("대수", self).move(self.width() * 0.1, self.height() * 0.1)
        QLabel("타입", self).move(self.width() * 0.7, self.height() * 0.1)

        self.edit_vcount = QLineEdit(self)
        self.edit_vcount.move(self.width() * 0.15, self.height() * 0.1)
        self.edit_vcount.textChanged.connect(self.validate)

        self.combo_type = QComboBox(self)
        self.combo_type.addItem("저상형")
        self.combo_type.addItem("Reel Direct")
        self.combo_type.move(self.width() * 0.75, self.height() * 0.1)

        QLabel("Vehicle 수: ", self).move(self.width() * 0.1, self.height() * 0.25)
        self.types = {
            "저상형": 0,
            "Reel Direct": 1,
        }

        self.label_v_count = []
        left = 0.2
        for i in range(self.combo_type.count()):
            self.vehicles.append([])
            self.label_v_count.append(QLabel(self))
            self.label_v_count[i].setGeometry(self.width() * left, self.height() * 0.25,
                                              100, 15)
            left += 0.05


        self.vehicle_list = QListWidget(self)
        self.vehicle_list.setGeometry(self.width() * 0.1, self.height() * 0.3,
                                      self.width() * 0.8, self.height() * 0.3)

        self.btn_add = QPushButton("ADD", self)
        self.btn_add.move(self.width() * 0.25, self.height() * 0.7)
        self.btn_add.clicked.connect(self.add)

        self.btn_delete = QPushButton("DELETE", self)
        self.btn_delete.move(self.width() * 0.65, self.height() * 0.7)
        self.btn_delete.clicked.connect(self.delete)

        self.setVehicleList()

    def validate(self):
        str = self.edit_vcount.text()

        for char in str:
            if not char.isdigit():
                str = str.replace(char, "")

        self.edit_vcount.setText(str)

    def add(self):
        count = int(self.edit_vcount.text())
        v_type = self.combo_type.currentText()

        for _ in range(count):
            self.context.v_count += 1
            self.vehicles[self.types[v_type]].append(AddVehicle(self.context.v_count, v_type))

        self.setVehicleList()

    def delete(self):
        count = int(self.edit_vcount.text())
        v_type = self.combo_type.currentText()

        for _ in range(count):
            for vehicle in self.vehicles[self.types[v_type]]:
                if vehicle.TYPE == v_type:
                    self.vehicles[self.types[v_type]].remove(vehicle)
                    break

        '''if self.combo_type.currentIndex() == 0:
            for _ in range(count):
                for type in self.vehicles:
                    for vehicle in type:
                        if vehicle.TYPE == v_type:
                            self.vehicles[0].remove(vehicle)
                            break

        elif self.combo_type.currentIndex() == 1:
            for _ in range(count):
                for v_type in self.vehicles:
                    for vehicle in v_type:
                        if vehicle.TYPE == v_type:
                            self.vehicles[0].remove(vehicle)
                            break'''

        self.setVehicleList()

    def setVehicleList(self):
        for i in range(self.combo_type.count()):
            v_count = len(self.vehicles[i])
            self.label_v_count[i].setText(str(v_count))

        self.vehicle_list.clear()

        for v_type in self.vehicles:
            for vehicle in v_type:
                self.vehicle_list.addItem("NAME: " + vehicle.NAME + "\t\t"
                                          + "TYPE: " + vehicle.TYPE)