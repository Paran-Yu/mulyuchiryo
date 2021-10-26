import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class MainPage(QWidget):
    def __init__(self, rect):
        super().__init__()
        self.rect = rect
        self.initUI()

    def initUI(self):
        self.initMainMenu()     # 메인 메뉴 생성
        self.initSubMenu()      # 서브 메뉴 생성
        self.showFullScreen()   # 전체화면 모드
        self.setWindowTitle("물류 치료")    # 프로그램 제목
        self.setWindowIcon(QIcon("./resources/image/favicon.png"))  # 프로그램 실행 아이콘

    # 메인 메뉴 생성
    def initMainMenu(self):
        self.menu_wrapper_height = 35
        menu_width = 110

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
            menu.resize(menu_width, self.menu_wrapper_height)
            menu.move(left, 0)
            left += menu_width

        self.menus[0].clicked.connect(lambda: self.getSubMenu(0))
        self.menus[1].clicked.connect(lambda: self.getSubMenu(1))
        self.menus[2].clicked.connect(lambda: self.getSubMenu(2))
        self.menus[3].clicked.connect(lambda: self.getSubMenu(3))
        self.menus[4].clicked.connect(lambda: self.getSubMenu(4))

    # 서브 메뉴 생성
    def initSubMenu(self):
        padding = 10
        sub_menu_size = 70

        self.subMenus = []
        sub_menu_wrapper = QWidget(self)
        sub_menu_wrapper.move(0,self.menu_wrapper_height)
        sub_menu_wrapper.resize(self.rect.width(), padding*2 + sub_menu_size)
        sub_menu_wrapper.setObjectName("sub-menu-wrapper")
        sub_menu_wrapper.setStyleSheet("#sub-menu-wrapper{"
                                       "background-color: #CCCCCC;"
                                       "border: 2px solid #AAAAAA;"
                                       "}")

        file = [
            QPushButton("Open", sub_menu_wrapper),
            QPushButton("Save", sub_menu_wrapper),
            QPushButton("Save\nAs", sub_menu_wrapper),
            QPushButton("Load", sub_menu_wrapper),
            QPushButton("Load\nLayout", sub_menu_wrapper),
            QPushButton("Set\nScale", sub_menu_wrapper),
            QPushButton("Close", sub_menu_wrapper),
        ]

        left = 0

        for menu in file:
            menu.setObjectName("sub-menu")
            menu.setStyleSheet("#sub-menu{"
                               "background-color:white;"
                               "font-size: 17px;"
                               "}"
                               "#sub-menu:hover{"
                               "background-color: #D7EDFF;"
                               "}")
            left += padding
            menu.resize(sub_menu_size, sub_menu_size)
            menu.move(left, padding)
            left += sub_menu_size

    # 메인 메뉴 버튼 클릭 이벤트
    def getSubMenu(self, idx):
        print(idx)
        self.mainMenu = idx
        #self.showSubMenu(idx)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = app.desktop()  # 컴퓨터 전체 화면 rect
    win = MainPage(screen.screenGeometry()) # 메인 화면 생성
    win.show()  # 화면 띄우기
    app.exec_() # 루프 실행