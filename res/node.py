class Node:
    def __init__(self, num, x_input, y_input):
        super().__init__()

        self.NUM = num
        self.X = x_input
        self.Y = y_input
        self.isCross = False

    def __lt__(self, other):
        return self.NUM < other.NUM

    def getPos(self):
        return (self.X, self.Y)

class Port(Node):
    def __init__(self, num, x_input, y_input, name):
        super().__init__(num, x_input, y_input)
        self.PORT_NAME = name
        self.TYPE = ""
        self.FREQ = -1
        self.V_TYPE = ""
        self.UNLOAD_LIST = []

        self.status = 0
        self.count = 0

    def get_unload(self):
        return self.UNLOAD_LIST


class WaitPoint(Node):
    def __init__(self, num, x_input, y_input, name):
        super().__init__(num, x_input, y_input)
        self.WAIT_NAME = name
        self.CHARGE = False

        self.using = False

    def getName(self):
        return self.WAIT_NAME

    def isCharge(self):
        return self.CHARGE

    def isUsing(self):
        return self.using