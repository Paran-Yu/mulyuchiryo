class Port:
    def __init__(self, name):
        self.NAME = name
        self.TYPE = ""
        self.NODE = -1
        self.FREQ = -1
        self.V_TYPE = ""

        self.isUsing = False