class Node:
    def __init__(self, name_input, x_input, y_input):
        super().__init__()

        self.NUM = name_input
        self.X = x_input
        self.Y = y_input
        self.isCross = False

class Port(Node):
    def __init__(self, name):
        self.PORT_NAME = name
        self.TYPE = ""
        self.FREQ = -1
        self.V_TYPE = ""

        self.isUsing = False

class WaitPoint(Node):
    def __init__(self, name):
        self.WAIT_NAME = name
        self.CHARGE = False

        self.using = False

    def getName(self):
        return self.WAIT_NAME

    def isCharge(self):
        return self.CHARGE

    def isUsing(self):
        return self.using