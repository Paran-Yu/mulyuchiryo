import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Selector:
    def __init__(self, context):
        super(Selector, self).__init__()
        self.context = context

    def selectNode(self, x, y):
        type = -1
        idx = -1
        for t in range(len(self.context.positions)):
            for i in range(len(self.context.positions[t])):
                if x - 10 < self.context.positions[t][i].point.x() < x + 10 \
                        and y - 10 < self.context.positions[t][i].point.y() < y + 10:
                    type = t
                    idx = i

        return type, idx

