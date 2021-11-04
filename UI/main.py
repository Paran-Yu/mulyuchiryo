import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from sidebar import SideBar

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

        self.tools = [
            "path",
            "port",
            "wait_point",
            "vehicle",
            "mouse",
        ]
        self.current_tool = 4
        self.paths = []
        self.ports = []
        self.wait_points = []
        self.vehicles = []

        self.positions = [
            self.paths,
            self.ports,
            self.wait_points,
            self.vehicles,
        ]

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

        # draw
        btn_path = QPushButton("Path", self.sub_menu_wrapper)
        btn_path.toggled.connect(lambda: self.changeTools(0))
        btn_path.setCheckable(True)

        btn_port = QPushButton("Port", self.sub_menu_wrapper)
        btn_port.toggled.connect(lambda: self.changeTools(1))
        btn_port.setCheckable(True)

        btn_wait_point = QPushButton("Wait\nPoint", self.sub_menu_wrapper)
        btn_wait_point.toggled.connect(lambda: self.changeTools(2))
        btn_wait_point.setCheckable(True)

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
                btn_path,
                btn_port,
                btn_wait_point,
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
        self.centralWidget.setGeometry(0, height, self.rect.width(), self.rect.height() - height)

        # 이미지를 넣을 label 생성.
        self.img_label = QLabel(self.centralWidget)
        self.img_label.resize(self.rect.width(), self.rect.height() - height)

        self.canvas_label = QLabel(self.centralWidget)
        self.canvas_label.resize(self.rect.width(), self.rect.height() - height)
        self.image_original = None

        # 객체들의 정보를 수정, 확인할 수 있는 사이드바 생성
        self.side_bar = SideBar(self.centralWidget)

    def changeTools(self, idx):
        # 버튼을 누른 경우
        if self.subMenus[1][idx].isChecked():
            self.current_tool = idx
            # 누른 버튼을 제외한 버튼 모두 해제.
            for i, btn in enumerate(self.subMenus[1]):
                if i != idx:
                    btn.setChecked(False)

        # 버튼을 해제한 경우
        else:
            # 포인터로 변경.
            for i, btn in enumerate(self.subMenus[1]):
                if btn.isChecked():
                    return

            self.current_tool = 4

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
            # 원본 이미지를 저장할 객체
            self.image_original = QImage()

            self.img_label.show()
            self.pm = QPixmap(fname[0])

            # 라벨 사이즈 조정
            pm_scaled = self.pm.scaledToWidth(self.img_label.width())
            self.img_label.setGeometry(0, 0, pm_scaled.width(), pm_scaled.height())
            self.canvas_label.setGeometry(0, 0, pm_scaled.width(), pm_scaled.height())

            # 가로크기에 맞추기
            #self.img_label.setPixmap(pm_scaled)

            self.image_original.load(fname[0])
            # 불러온 이미지와 같은 크기의 투명 도화지. 이 위에 그림을 그림.
            self.canvas = QImage(self.image_original.width(), self.image_original.height(),
                                 QImage.Format_ARGB32_Premultiplied)
            self.canvas.fill(0x00ffffff)

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
            self.canvas_label.move(nx, ny)

        '''
        끌기 작업에서 불필요하다고 판단해서 주석처리.
        나중에 필요할 지도 몰라서 냅둠
        elif not self.ctrl_pressed:
            # path 그리기 도구일 때 왼쪽 마우스 처리.
            # TODO: move this for mousePressEvent. (We don't need draw line.)
            if self.mouse_left and self.current_tool == "path":
                # TODO: Paint at another label.
                #qp = QPainter(self.image_original)
                qp = QPainter(self.canvas)

                # TODO: Change the Pen Size to Fit the Screen Size.
                qp.setPen(QPen(QColor(0, 0, 0), 15))
                #nx = (e.x() - self.img_label.x()) * self.image_original.width() / self.img_label.width()
                #ny = (e.y() - self.img_label.y() - self.sub_menu_wrapper_height - self.menu_wrapper_height)\
                #     * self.image_original.height() / self.img_label.height()

                nx = (e.x() - self.canvas_label.x()) * self.canvas.width() / self.canvas_label.width()
                ny = (e.y() - self.canvas_label.y() - self.sub_menu_wrapper_height - self.menu_wrapper_height) \
                     * self.canvas.height() / self.canvas_label.height()

                qp.drawPoint(nx, ny)

                # TODO: erase above drawPoint and draw all paths, ports, vehicles in paintEvent.
                self.paths.append(QPoint(nx, ny))
                qp.end()
                self.drawCanvas()
        '''

    # 모든 객체들을 화면에 그림.
    def drawCanvas(self):
        for path in self.paths:
            qp = QPainter(self.canvas)

            qp.setPen(QPen(QColor(0, 0, 0), 15))
            qp.drawPoint(path)
            qp.drawEllipse(path, 4, 4)

            qp.end()
        for port in self.ports:
            qp = QPainter(self.canvas)

            qp.setPen(QPen(QColor(255, 0, 0), 15))
            qp.drawPoint(port)
            qp.setPen(QPen(QColor(255, 0, 0), 1))
            qp.drawRect(port.x()-7.5, port.y()-7.5, 15, 15)

            qp.end()

        for wait_point in self.wait_points:
            qp = QPainter(self.canvas)

            qp.setPen(QPen(QColor(0, 0, 255), 15))
            qp.drawPoint(wait_point)

            qp.end()
        # TODO: Add Ports, Wait Points and Vehicles

    # 화면에 그려진 객체들을 지움.
    def eraseCanvas(self):
        self.canvas.fill(0x00ffffff)

    # 마우스 클릭 이벤트
    def mousePressEvent(self, e):
        if e.buttons() & Qt.LeftButton:
            self.mouse_left = True
            # 현재 마우스 위치와 라벨의 시작점간의 차이
            self.dx = e.x() - self.img_label.x()
            self.dy = e.y() - self.img_label.y()

            # 컨트롤이 눌리지 않았고, 편집할 이미지가 오픈 된 경우
            if not self.ctrl_pressed and self.image_original:
                # 그리기 도구일 때 좌표를 찾아서 저장.
                if self.mouse_left and self.tools[self.current_tool] != "mouse":
                    nx = (e.x() - self.canvas_label.x()) * self.canvas.width() / self.canvas_label.width()
                    ny = (e.y() - self.canvas_label.y() - self.sub_menu_wrapper_height - self.menu_wrapper_height) \
                         * self.canvas.height() / self.canvas_label.height()

                    self.positions[self.current_tool].append(QPoint(nx, ny))
                    self.drawCanvas()

        if e.buttons() & Qt.MidButton:
            pass
        if e.buttons() & Qt.RightButton:
            self.eraseCanvas()
            pass

    # 마우스 해제 이벤트
    def mouseReleaseEvent(self, e):
        self.mouse_left = False

    # 화면 갱신 이벤트
    def paintEvent(self, event):
        if self.image_original:
            self.image_scaled = self.image_original.scaledToWidth(self.img_label.width())
            self.canvas_scaled = self.canvas.scaled(self.canvas_label.width(), self.canvas_label.height())

            # Convert QImage to QPixmap
            # QPixmap은 수정이, QImage는 출력이 안되기 때문.
            # TODO: print all nodes in here.
            pixmap = QPixmap(self.image_scaled)
            self.img_label.setPixmap(pixmap)

            pixmap = QPixmap(self.canvas_scaled)
            self.canvas_label.setPixmap(pixmap)

# Run App.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = app.desktop()  # 컴퓨터 전체 화면 rect
    win = MainPage(screen.screenGeometry()) # 메인 화면 생성
    win.show()  # 화면 띄우기
    app.exec_() # 루프 실행