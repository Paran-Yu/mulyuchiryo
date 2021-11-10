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

        # 노드만 확인하기 위해서 -2를 해줌.
        for t in range(len(self.context.positions) - 2):
            for i in range(len(self.context.positions[t])):
                if x - 10 < self.context.positions[t][i].X < x + 10 \
                        and y - 10 < self.context.positions[t][i].Y < y + 10:
                    type = t
                    idx = i

        return type, idx

