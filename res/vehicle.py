class Vehicle:
    def __init__(self, name):
        super().__init__()

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
        self.STAT_LIST = {}

        self.x = -1
        self.y = -1
        self.node = -1
        self.next_node = -1
        self.velocity = -1
        self.angle = -1
        self.status = 0
        self.loaded = 0
        self.battery = -1
        self.command_list = []

    # new_node로 이동
    def move(self, new_node):
        pass

    def load(self, port_num):
        pass

    def unload(self, port_num):
        pass

    def getNode(self):
        pass

    def getPos(self):
        pass

    def getDesti(self):
        pass

    def getBattery(self):
        pass

    def getStatus(self):
        pass