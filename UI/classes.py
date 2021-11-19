class Node:
    def __init__(self, num, x_input, y_input):
        super().__init__()

        self.NUM = num
        self.X = x_input
        self.Y = y_input
        self.isCross = False

    def __lt__(self, other):
        return self.NUM < other.NUM

class Port(Node):
    def __init__(self, num, x_input, y_input, name="Port"):
        super().__init__(num, x_input, y_input)
        self.PORT_NAME = name
        self.TYPE = "unload"
        self.FREQ = -1
        self.V_TYPE = ""
        self.UNLOAD_LIST = []

        self.status = 0
        self.count = 0

    def get_unload(self):
        return self.UNLOAD_LIST

class WaitPoint(Node):
    def __init__(self, num, x_input, y_input, name="WaitPoint"):
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

class Path:
    def __init__(self, start, end):
        self.start = start
        self.end = end

class Vehicle:
    def __init__(self, name):
        super().__init__()
        self.NUM = -1
        self.NAME = name
        self.TYPE = "default"
        self.WIDTH = -1
        self.HEIGHT = -1
        self.DIAGONAL = -1
        self.ROTATE_SPEED = -1
        self.ACCEL = -1
        self.MAX_SPEED = -1
        self.LU_TYPE = "default"
        self.LOAD_SPEED = -1
        self.CHARGE_SPEED = -1
        self.DISCHARGE_WAIT = -1
        self.DISCHARGE_WORK = -1
        self.BREAK_PARAM = 1.8
        self.NODE_TH = 200
        self.ROTATE_TH = -1

        self.x = -1
        self.y = -1
        self.node = -1
        self.desti_node = -1
        self.velocity = -1
        self.angle = -1
        self.status = 0
        self.loaded = 0
        self.battery = -1
        self.cmd = ""
        self.path = []
        self.turn_flag = 0
        self.last_flag = 0
        self.turning = -1
        self.dAngle = 0
        self.desti_angle = 0
        self.count = 0
        self.dCharge = 0
