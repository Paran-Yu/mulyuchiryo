import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class MainPage(QWidget):
    def __init__(self, rect):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.initMainMenu()     # 메인 메뉴 생성
        self.showFullScreen()   # 전체화면 모드
        self.setWindowTitle("물류 치료")    # 프로그램 제목
        self.setWindowIcon(QIcon("./resources/image/favicon.png"))  # 프로그램 실행 아이콘

    # 메인 메뉴 생성
    def initMainMenu(self):
        self.menu_height = 35
        self.menu_width = 110

        self.menus = []
        self.menus.append(QPushButton("File", self))
        self.menus.append(QPushButton("Draw", self))
        self.menus.append(QPushButton("Vehicle", self))
        self.menus.append(QPushButton("Simulate", self))
        self.menus.append(QPushButton("Report", self))

        left = 0
        for idx, menu in enumerate(self.menus):
            font = QFont()
            font.setPointSize(13)   # font size 변경
            menu.setFont(font)      # font size 적용
            menu.setObjectName("main-menu")
            menu.setStyleSheet("#main-menu{"    # style 적용
                               "background-color: white;"
                               "}"
                               "#HI:hover{"
                               "background-color:red;"
                               "}")
            menu.resize(self.menu_width, self.menu_height)
            menu.move(left, 0)
            left += self.menu_width

        self.menus[0].clicked.connect(lambda: self.getSubMenu(0))
        self.menus[1].clicked.connect(lambda: self.getSubMenu(1))
        self.menus[2].clicked.connect(lambda: self.getSubMenu(2))
        self.menus[3].clicked.connect(lambda: self.getSubMenu(3))
        self.menus[4].clicked.connect(lambda: self.getSubMenu(4))

    def getSubMenu(self, idx):
        print(idx)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = app.desktop()  # 컴퓨터 전체 화면 rect
    win = MainPage(screen.screenGeometry()) # 메인 화면 생성
    win.show()  # 화면 띄우기
    app.exec_() # 루프 실행