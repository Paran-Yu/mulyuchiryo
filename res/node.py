class Node:
    def __init__(self, name_input, x_input, y_input):
        super().__init__()

        self.name = name_input
        self.x = x_input
        self.y = y_input
        self.isCross = False
        self.isPort = False
        self.isWait = False