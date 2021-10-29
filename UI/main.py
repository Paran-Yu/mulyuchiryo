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

        self.mainMenu = 0   # 초기 메뉴는 file탭

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

        # 메뉴 클릭 이벤트
        self.menus[0].clicked.connect(lambda: self.getSubMenu(0))
        self.menus[1].clicked.connect(lambda: self.getSubMenu(1))
        self.menus[2].clicked.connect(lambda: self.getSubMenu(2))
        self.menus[3].clicked.connect(lambda: self.getSubMenu(3))
        self.menus[4].clicked.connect(lambda: self.getSubMenu(4))

    # 서브 메뉴 생성
    def initSubMenu(self):
        padding = 10    # 메뉴 아이콘 여백
        self.sub_menu_size = 70 # 서브 메뉴 아이콘 크기

        # 서브 메뉴 바 생성.
        self.sub_menu_wrapper = QWidget(self)
        self.sub_menu_wrapper.move(0,self.menu_wrapper_height)
        self.sub_menu_wrapper.resize(self.rect.width(), padding*2 + self.sub_menu_size)
        self.sub_menu_wrapper.setObjectName("sub-menu-wrapper")
        self.sub_menu_wrapper.setStyleSheet("#sub-menu-wrapper{"
                                       "background-color: #CCCCCC;"
                                       "border: 2px solid #AAAAAA;"
                                       "}")

        # 서브 메뉴 항목 추가
        self.subMenus = [
            # file
            [
                QPushButton("Open", self.sub_menu_wrapper),
                QPushButton("Save", self.sub_menu_wrapper),
                QPushButton("Save\nAs", self.sub_menu_wrapper),
                QPushButton("Load", self.sub_menu_wrapper),
                QPushButton("Open\nLayout", self.sub_menu_wrapper),
                QPushButton("Set\nScale", self.sub_menu_wrapper),
                QPushButton("Close", self.sub_menu_wrapper),
            ],
            # draw
            [
                QPushButton("Path", self.sub_menu_wrapper),
                QPushButton("Port", self.sub_menu_wrapper),
                QPushButton("Wait\nPoint", self.sub_menu_wrapper),
            ],
            # vehicle
            [
                QPushButton("Add", self.sub_menu_wrapper),
                QPushButton("Delete\nAll", self.sub_menu_wrapper),
            ],
            # simulate
            [
                QPushButton("Play", self.sub_menu_wrapper),
                QPushButton("Stop", self.sub_menu_wrapper),
                QPushButton("Speed", self.sub_menu_wrapper),
            ],
            # report
            [
            ],
        ]

        for mainMenu in self.subMenus:
            left = 0
            for menu in mainMenu:
                menu.setObjectName("sub-menu")
                menu.setStyleSheet("#sub-menu{"
                                   "background-color:white;"
                                   "font-size: 17px;"
                                   "}"
                                   "#sub-menu:hover{"
                                   "background-color: #D7EDFF;"
                                   "}")
                menu.resize(self.sub_menu_size, self.sub_menu_size)
                left += padding
                menu.move(left, padding)
                left += self.sub_menu_size
                menu.hide()

        self.showSubMenu(self.mainMenu)

    def hideSubMenu(self, idx):
        for menu in self.subMenus[idx]:
            menu.hide()

    def showSubMenu(self, idx):
        for menu in self.subMenus[idx]:
            menu.show()

    # 메인 메뉴 버튼 클릭 이벤트
    def getSubMenu(self, idx):
        if idx != self.mainMenu:
            self.hideSubMenu(self.mainMenu)
            self.mainMenu = idx
            self.showSubMenu(idx)

# Run App.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = app.desktop()  # 컴퓨터 전체 화면 rect
    win = MainPage(screen.screenGeometry()) # 메인 화면 생성
    win.show()  # 화면 띄우기
    app.exec_() # 루프 실행