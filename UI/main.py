import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class MainPage(QWidget):
    def __init__(self, rect):
        super().__init__()
        self.rect = rect

        self.menu_wrapper_height = 35
        self.sub_menu_wrapper_height = 90

        self.mainMenu = 0   # 선택된 메뉴, 초기탭은 file탭
        self.pm = 0

        self.zoom = QPointF()
        self.ctrl_pressed = False
        self.mouse_left = False

        self.current_tool = "path"
        self.paths = []

        self.initUI()

    def initUI(self):
        self.initCentralWidget()    # 메인 화면 생성
        self.initMainMenu()     # 메인 메뉴 생성
        self.initSubMenu()      # 서브 메뉴 생성
        self.showFullScreen()   # 전체화면 모드
        self.setWindowTitle("물류 치료")    # 프로그램 제목
        self.setWindowIcon(QIcon("./resources/image/favicon.png"))  # 프로그램 실행 아이콘

    # 메인 메뉴 생성
    def initMainMenu(self):
        menu_width = 110

        # 메뉴 바 생성.
        self.menu_wrapper = QWidget(self)
        self.menu_wrapper.resize(self.rect.width(), self.menu_wrapper_height)
        self.menu_wrapper.setObjectName("menu-wrapper")
        self.menu_wrapper.setStyleSheet("#menu-wrapper{"
                                       "background-color: #FFFFFF;"
                                       "}")

        self.menus = []
        self.menus.append(QPushButton("File", self.menu_wrapper))
        self.menus.append(QPushButton("Draw", self.menu_wrapper))
        self.menus.append(QPushButton("Vehicle", self.menu_wrapper))
        self.menus.append(QPushButton("Simulate", self.menu_wrapper))
        self.menus.append(QPushButton("Report", self.menu_wrapper))

        left = 0
        for idx, menu in enumerate(self.menus):
            font = QFont()
            font.setPointSize(13)   # font size 변경
            menu.setFont(font)      # font size 적용
            menu.setObjectName("main-menu")
            menu.setStyleSheet("#main-menu{"    # style 적용
                               "background-color: white;"
                               "}"
                               "#main-menu:hover{"
                               "background-color: #D7EDFF;"
                               "}"
                               "#main-menu:pressed{"
                               "background-color: #C5DCFF;"
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
        sub_menu_size = self.sub_menu_wrapper_height - (2 * padding) # 서브 메뉴 아이콘 크기

        # 서브 메뉴 바 생성.
        self.sub_menu_wrapper = QWidget(self)
        self.sub_menu_wrapper.move(0,self.menu_wrapper_height)
        self.sub_menu_wrapper.resize(self.rect.width(), self.sub_menu_wrapper_height)
        self.sub_menu_wrapper.setObjectName("sub-menu-wrapper")
        self.sub_menu_wrapper.setStyleSheet("#sub-menu-wrapper{"
                                       "background-color: #CCCCCC;"
                                       "border: 2px solid #AAAAAA;"
                                       "}")

        # 서브 메뉴 항목 추가
        # file
        btn_open_layout = QPushButton("Open\nLayout", self.sub_menu_wrapper)
        btn_open_layout.clicked.connect(self.openLayout)

        self.subMenus = [
            # file
            [
                QPushButton("Open", self.sub_menu_wrapper),
                QPushButton("Save", self.sub_menu_wrapper),
                QPushButton("Save\nAs", self.sub_menu_wrapper),
                QPushButton("Load", self.sub_menu_wrapper),
                btn_open_layout,
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
                                   "}"
                                   "#sub-menu:pressed{"
                                   "background-color: #C5DCFF;"
                                   "}")
                menu.resize(sub_menu_size, sub_menu_size)
                left += padding
                menu.move(left, padding)
                left += sub_menu_size
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

    # 메인 화면 생성
    def initCentralWidget(self):
        # 메인 화면의 시작점 (메뉴바, 서브메뉴바 크기를 제외한 위치부터 시작)
        height = self.menu_wrapper_height + self.sub_menu_wrapper_height
        self.centralWidget = QWidget(self)
        self.centralWidget.move(0, height)

        # 이미지를 넣을 label 생성.
        self.img_label = QLabel(self.centralWidget)
        self.img_label.resize(self.rect.width(), self.rect.height() - height)

        self.canvas_label = QLabel(self.centralWidget)
        self.canvas_label.resize(self.rect.width(), self.rect.height() - height)

        self.image_original = QImage()
        self.canvas = QImage()

    # 기존 작업 불러오기
    def load(self):
        pass

    # 현재 작업 저장
    def save(self):
        pass

    # 도면 열기
    def openLayout(self):
        # 파일 오픈
        fname = QFileDialog.getOpenFileName(self, 'Open file', './', "Image Files (*.jpg *.jpeg *.bmp *.png)")

        if fname[0]:
            self.img_label.show()
            self.pm = QPixmap(fname[0])

            # 라벨 사이즈 조정
            pm_scaled = self.pm.scaledToWidth(self.img_label.width())
            self.img_label.setGeometry(0, 0, pm_scaled.width(), pm_scaled.height())
            # 이미지 위에 그림을 그리면, 나중에 지울 수 없으므로 빈 라벨에 그릴 예정.
            self.canvas_label.setGeometry(0, 0, pm_scaled.width(), pm_scaled.height())

            # 가로크기에 맞추기
            #self.img_label.setPixmap(pm_scaled)

            self.image_original.load(fname[0])


    # 키보드 클릭 이벤트
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Control:
            self.ctrl_pressed = True

    # 키보드 떼는 이벤트
    def keyReleaseEvent(self, e):
        if e.key() == Qt.Key_Control:
            self.ctrl_pressed = False

    # 휠 이벤트
    def wheelEvent(self, e):
        if self.ctrl_pressed:
            self.zoom += e.angleDelta() / 120

            if self.pm != 0:
                scaled_width = self.centralWidget.width() + self.zoom.y() * 100
                self.pm_scaled = self.pm.scaledToWidth(scaled_width)
                self.img_label.setGeometry(self.img_label.geometry().x(), self.img_label.geometry().y(), self.pm_scaled.width(), self.pm_scaled.height())
                self.img_label.setPixmap(self.pm_scaled)

                self.canvas_label.setGeometry(self.img_label.geometry().x(), self.img_label.geometry().y(), self.pm_scaled.width(), self.pm_scaled.height())

    # 마우스 트래킹 이벤트
    def mouseMoveEvent(self, e):
        # 컨트롤을 누르고 왼쪽 마우스를 끌면
        if self.mouse_left and self.ctrl_pressed:
            nx = e.x() - self.dx
            ny = e.y() - self.dy
            self.img_label.move(nx, ny)
            # TODO: move canvas together.

        elif not self.ctrl_pressed:
            # path 그리기 도구일 때 왼쪽 마우스 처리.
            # TODO: move this for mousePressEvent. (We don't need draw line.)
            if self.mouse_left and self.current_tool == "path":
                # TODO: Paint at another label.
                qp = QPainter(self.image_original)

                # TODO: Change the Pen Size to Fit the Screen Size.
                qp.setPen(QPen(QColor(0, 0, 0), 15))
                nx = (e.x() - self.img_label.x()) * self.image_original.width() / self.img_label.width()
                ny = (e.y() - self.img_label.y() - self.sub_menu_wrapper_height - self.menu_wrapper_height)\
                     * self.image_original.height() / self.img_label.height()

                qp.drawPoint(nx, ny)

                # TODO: erase above drawPoint and draw all paths, ports, vehicles in paintEvent.
                self.paths.append(QPoint(nx, ny))
                qp.end()

    # 마우스 클릭 이벤트
    def mousePressEvent(self, e):
        if e.buttons() & Qt.LeftButton:
            self.mouse_left = True
            # 현재 마우스 위치와 라벨의 시작점간의 차이
            self.dx = e.x() - self.img_label.x()
            self.dy = e.y() - self.img_label.y()
        if e.buttons() & Qt.MidButton:
            pass
        if e.buttons() & Qt.RightButton:
            pass

    # 마우스 해제 이벤트
    def mouseReleaseEvent(self, e):
        self.mouse_left = False

    # 화면 갱신 이벤트
    def paintEvent(self, event):
        if self.image_original:
            self.image_scaled = self.image_original.scaledToWidth(self.img_label.width())

            # Convert QImage to QPixmap
            # QPixmap은 수정이, QImage는 출력이 안되기 때문.
            # TODO: print all nodes in here.
            pixmap = QPixmap(self.image_scaled)
            self.img_label.setPixmap(pixmap)

# Run App.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = app.desktop()  # 컴퓨터 전체 화면 rect
    win = MainPage(screen.screenGeometry()) # 메인 화면 생성
    win.show()  # 화면 띄우기
    app.exec_() # 루프 실행