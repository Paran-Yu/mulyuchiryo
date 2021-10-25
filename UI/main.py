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
        self.menus = []
        self.menus.append(QPushButton("File", self))
        self.menus.append(QPushButton("Draw", self))
        self.menus.append(QPushButton("Vehicle", self))
        self.menus.append(QPushButton("Simulate", self))
        self.menus.append(QPushButton("Report", self))

        left = 0
        for menu in self.menus:
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
            menu.resize(110, 35)
            menu.move(left, 0)
            left += 110

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = app.desktop()  # 컴퓨터 전체 화면 rect
    win = MainPage(screen.screenGeometry()) # 메인 화면 생성
    win.show()  # 화면 띄우기
    app.exec_() # 루프 실행