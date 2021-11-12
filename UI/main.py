import sys
import os.path
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from sidebar import SideBar
from selector import Selector
from classes import *
from scale import Scale
from vehicleEditor import VehicleEditor
import pickle

class Context:
    def __init__(self):
        self.main = None
        self.class_list = [Node, Port, WaitPoint, Path]
        self.scale = 1
        self.v_count = 0

class MainPage(QWidget):
    # auto increment ID.
    count = 0

    def __init__(self, rect):
        super().__init__()
        self.rect = rect
        self.context = Context()
        self.context.main = self

        self.menu_wrapper_height = 35
        self.sub_menu_wrapper_height = 90

        self.mainMenu = 0   # 선택된 메뉴, 초기탭은 file탭
        self.pm = 0

        self.zoom = QPointF()
        self.ctrl_pressed = False
        self.shift_pressed = False
        self.mouse_left = False
        self.node_selected = False
        self.draw_path = False

        self.tools = [
            "node",
            "port",
            "wait_point",
            "path",
            "vehicle",
            "mouse",
        ]
        self.current_tool = 5
        self.nodes = []
        self.ports = []
        self.wait_points = []
        self.paths = []
        self.vehicles = []

        self.positions = [
            self.nodes,
            self.ports,
            self.wait_points,
            self.paths,
            self.vehicles,
        ]

        self.selector = Selector(self)
        self.context.selector = self.selector

        self.layout_name = None

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

        btn_save = QPushButton("Save", self.sub_menu_wrapper)
        btn_save.clicked.connect(self.save)

        btn_save_as = QPushButton("Save\nAs", self.sub_menu_wrapper)
        btn_save_as.clicked.connect(self.saveAs)

        btn_load = QPushButton("Load", self.sub_menu_wrapper)
        btn_load.clicked.connect(self.load)

        btn_set_scale = QPushButton("Set\nScale", self.sub_menu_wrapper)
        btn_set_scale.clicked.connect(self.setScale)

        btn_close = QPushButton("Close", self.sub_menu_wrapper)
        btn_close.clicked.connect(self.close)

        # draw
        btn_node = QPushButton("Node", self.sub_menu_wrapper)
        btn_node.toggled.connect(lambda: self.changeTools(0))
        btn_node.setCheckable(True)

        btn_port = QPushButton("Port", self.sub_menu_wrapper)
        btn_port.toggled.connect(lambda: self.changeTools(1))
        btn_port.setCheckable(True)

        btn_wait_point = QPushButton("Wait\nPoint", self.sub_menu_wrapper)
        btn_wait_point.toggled.connect(lambda: self.changeTools(2))
        btn_wait_point.setCheckable(True)

        btn_path = QPushButton("Path", self.sub_menu_wrapper)
        btn_path.toggled.connect(lambda: self.changeTools(3))
        btn_path.setCheckable(True)

        # Vehicle
        btn_vehicle_edit = QPushButton("Edit", self.sub_menu_wrapper)
        btn_vehicle_edit.clicked.connect(self.editVehicle)

        self.subMenus = [
            # file
            [
                btn_save,
                btn_save_as,
                btn_load,
                btn_open_layout,
                btn_set_scale,
                btn_close,
            ],
            # draw
            [
                btn_node,
                btn_port,
                btn_wait_point,
                btn_path,
            ],
            # vehicle
            [
                btn_vehicle_edit,
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
        self.canvas_prev = None

        # 객체들의 정보를 수정, 확인할 수 있는 사이드바 생성
        self.side_bar = SideBar(self.context, self.centralWidget)

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

            self.current_tool = 5

    # 기존 작업 불러오기
    def load(self):
        # TODO: 불러온 뒤 패스가 노드에 연결되게 설정하기.
        self.layout_name = QFileDialog.getOpenFileName(self, 'Load Layout', './', "Layout 파일 (*.layout)")

        if self.layout_name[0]:
            with open(self.layout_name[0], 'rb') as f:
                # 이미지 파일 경로를 불러옴
                self.fname = pickle.load(f)

                # 이미지 파일 존재 확인 후 나머지 정보도 불러옴
                if os.path.exists(self.fname[0]):
                    self.count = pickle.load(f)
                    self.nodes = pickle.load(f)
                    self.ports = pickle.load(f)
                    self.wait_points = pickle.load(f)
                    self.paths = pickle.load(f)
                    self.vehicles = pickle.load(f)

                # 경로에 이미지가 더 이상 존재하지 않는다면 경고 메시지 출력
                else:
                    alert = QMessageBox()
                    alert.setWindowTitle("No Such File")  # 메세지창의 상단 제목
                    alert.setIcon(QMessageBox.Information)  # 메세지창 내부에 표시될 아이콘
                    alert.setText("저장된 이미지가 존재하지 않습니다.")  # 메세지 제목
                    alert.setInformativeText("src: " + self.fname[0])  # 메세지 내용
                    alert.setStandardButtons(QMessageBox.Ok)  # 메세지창의 버튼
                    alert.setDefaultButton(QMessageBox.Ok)  # 포커스가 지정된 기본 버튼

                    alert.exec_()
                    return

            self.openImage(self.fname)
            self.positions = [
                self.nodes,
                self.ports,
                self.wait_points,
                self.paths,
                self.vehicles,
            ]

            # path 정보를 기준으로 노드간 연결.
            for path in self.paths:
                for type in range(3):
                    for node in self.positions[type]:
                        if node.NUM == path.start.NUM:
                            path.start = node
                        if node.NUM == path.end.NUM:
                            path.end = node

            self.eraseCanvas()
            self.drawCanvas()

    # 현재 작업 내용 저장
    def save(self):
        # TODO: Change Image src to real Image by use numpy.
        if self.layout_name is None:
            if self.saveAs():
                return True
            return False

        else:
            with open(self.layout_name[0], 'wb') as f:
                pickle.dump(self.fname, f)
                pickle.dump(self.count, f)
                pickle.dump(self.nodes, f)
                pickle.dump(self.ports, f)
                pickle.dump(self.wait_points, f)
                pickle.dump(self.paths, f)
                pickle.dump(self.vehicles, f)
            return True

    # 다른 이름으로 저장
    def saveAs(self):
        # 이미지를 불러온 상태가 아니라면 저장하지 않는다.
        if not self.image_original:
            return

        name = QFileDialog.getSaveFileName(self, 'Save file', './', "Layout 파일 (*.layout)")
        if name[0]:
            self.layout_name = name
            # 이미지 경로 및 기타 정보 저장
            with open(self.layout_name[0], 'wb') as f:
                pickle.dump(self.fname, f)
                pickle.dump(self.count, f)
                pickle.dump(self.nodes, f)
                pickle.dump(self.ports, f)
                pickle.dump(self.wait_points, f)
                pickle.dump(self.paths, f)
                pickle.dump(self.vehicles, f)

            return True
        return False

    # 도면 열기
    def openLayout(self):
        # 파일 오픈
        self.fname = QFileDialog.getOpenFileName(self, 'Open file', './', "Image Files (*.jpg *.jpeg *.bmp *.png)")

        self.openImage(self.fname)

    def openImage(self, fname):
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

    def setScale(self):
        if self.image_original:
            qd = Scale()
            qd.setGeometry(self.rect.width() * 0.3, self.rect.height() * 0.3,
                           self.rect.width() * 0.2, self.rect.height() * 0.1)
            qd.initUI()
            if qd.exec_():
                mm = qd.edit_mm.text()
                if mm.isdigit():
                    mm = int(mm)
                    pixel = self.rect.width()

                    scale = round(mm / pixel, 1)
                    self.context.scale = scale

    def close(self):
        # 작업 내용 없으면 그냥 종료
        if not self.image_original:
            super().close()
            return

        reply = QMessageBox.question(self, 'Message', 'Are you sure to save and quit?',
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if self.save():
                super().close()
        elif reply == QMessageBox.No:
            super().close()

    def editVehicle(self):
        editor = VehicleEditor(self.context, self.vehicles)
        editor.setGeometry(self.width()*0.1, self.height()*0.1,
                           self.width()*0.4, self.height()*0.3)
        editor.initUI()

        editor.exec_()

        self.vehicles = editor.vehicles

    # 키보드 클릭 이벤트
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Control:
            self.ctrl_pressed = True

        if e.key() == Qt.Key_Shift:
            self.shift_pressed = True

    # 키보드 떼는 이벤트
    def keyReleaseEvent(self, e):
        if e.key() == Qt.Key_Control:
            self.ctrl_pressed = False

        if e.key() == Qt.Key_Shift:
            self.shift_pressed = False

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
        if self.ctrl_pressed:
            if self.mouse_left:
                nx = e.x() - self.dx
                ny = e.y() - self.dy
                self.img_label.move(nx, ny)
                self.canvas_label.move(nx, ny)
        else:
            if self.node_selected:
                nx = (e.x() - self.canvas_label.x()) * self.canvas.width() / self.canvas_label.width()
                ny = (e.y() - self.canvas_label.y() - self.sub_menu_wrapper_height - self.menu_wrapper_height) \
                     * self.canvas.height() / self.canvas_label.height()
                # path 메뉴인 경우, 선을 미리 보여줌.
                if self.draw_path:
                    self.canvas_prev = QImage(self.canvas)
                    qp = QPainter(self.canvas_prev)

                    qp.setPen(QPen(QColor(0, 0, 0), 10))
                    qp.drawLine(self.selected_node.X, self.selected_node.Y, nx, ny)

                    qp.end()

                else:
                    # 쉬프트를 누르고 끌 경우, 직선상으로 이동
                    if self.shift_pressed:
                        dx = abs(self.sp.x() - nx)
                        dy = abs(self.sp.y() - ny)

                        if dx < dy:
                            self.selected_node.X = self.sp.x()
                            self.selected_node.Y = int(ny)
                        else:
                            self.selected_node.X = int(nx)
                            self.selected_node.Y = self.sp.y()
                    else:
                        self.selected_node.X = int(nx)
                        self.selected_node.Y = int(ny)

                    self.side_bar.widget.show()

                    self.side_bar.setDetail(self.selected_node)

    # 모든 객체들을 화면에 그림.
    def drawCanvas(self):
        for node in self.nodes:
            qp = QPainter(self.canvas)

            qp.setPen(QPen(QColor(0, 0, 0), 15))
            qp.drawPoint(node.X, node.Y)
            qp.drawEllipse(node.X, node.Y, 4, 4)

            qp.end()
        for port in self.ports:
            qp = QPainter(self.canvas)

            qp.setPen(QPen(QColor(255, 0, 0), 15))
            qp.drawPoint(port.X, port.Y)
            qp.setPen(QPen(QColor(255, 0, 0), 1))
            qp.drawRect(port.X-7.5, port.Y-7.5, 15, 15)

            qp.end()

        for wait_point in self.wait_points:
            qp = QPainter(self.canvas)

            qp.setPen(QPen(QColor(0, 0, 255), 15))
            qp.drawPoint(wait_point.X, wait_point.Y)

            qp.end()

        for path in self.paths:
            qp = QPainter(self.canvas)

            qp.setPen(QPen(QColor(0, 0, 0), 10))
            qp.drawLine(path.start.X, path.start.Y, path.end.X, path.end.Y)

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
                # 메뉴바 이상을 눌렀을 때 무반응.
                if e.y() < self.menu_wrapper_height + self.sub_menu_wrapper_height:
                    return

                nx = (e.x() - self.canvas_label.x()) * self.canvas.width() / self.canvas_label.width()
                ny = (e.y() - self.canvas_label.y() - self.sub_menu_wrapper_height - self.menu_wrapper_height) \
                     * self.canvas.height() / self.canvas_label.height()

                if self.canvas.pixel(nx, ny) != 0x00ffffff:
                    self.node_selected = True
                    # select clicked node.
                    type, idx = self.selector.selectNode(nx, ny)

                    if idx != -1:
                        self.selected_node = self.positions[type][idx]
                        self.sp = QPoint(self.selected_node.X, self.selected_node.Y)

                        self.side_bar.widget.show()
                        self.side_bar.getDetail(type)
                        self.side_bar.setDetail(self.selected_node)

                        if self.tools[self.current_tool] == "path":
                            self.draw_path = True

                # 그리기 도구일 때 좌표를 찾아서 저장.
                elif self.tools[self.current_tool] not in ["mouse", "path"]:
                    '''self.mouse_left and '''
                    self.node_selected = True

                    # Count increment per every node creation
                    self.count += 1
                    self.selected_node = self.context.class_list[self.current_tool](self.count, int(nx), int(ny))
                    self.selected_node.count = 0    # 연결된 node 수를 알기 위한 변수.
                    self.positions[self.current_tool].append(self.selected_node)
                    self.drawCanvas()

                    self.sp = QPoint(nx, ny)

                    self.side_bar.widget.show()
                    self.side_bar.getDetail(self.current_tool)
                    self.side_bar.setDetail(self.selected_node)

                elif self.tools[self.current_tool] == "mouse":
                    self.side_bar.widget.hide()

        if e.buttons() & Qt.MidButton:
            pass
        if e.buttons() & Qt.RightButton:
            if self.side_bar.widget.isHidden():
                self.side_bar.widget.show()
            else:
                self.side_bar.widget.hide()

    # 마우스 해제 이벤트
    def mouseReleaseEvent(self, e):
        self.mouse_left = False
        self.node_selected = False
        self.draw_path = False

        # 노드와 노드를 정상적으로 연결하면, Edge를 등록함.
        if self.tools[self.current_tool] == "path" and self.canvas_prev:
            self.canvas_prev = None
            nx = (e.x() - self.canvas_label.x()) * self.canvas.width() / self.canvas_label.width()
            ny = (e.y() - self.canvas_label.y() - self.sub_menu_wrapper_height - self.menu_wrapper_height) \
                 * self.canvas.height() / self.canvas_label.height()

            if self.canvas.pixel(nx, ny) != 0x00ffffff:
                type, idx = self.selector.selectNode(nx, ny)

                start = self.selected_node
                end = self.positions[type][idx]

                # 스스로에게 연결되는 path 제외
                if start == end:
                    return

                # 쉬프트를 누른 경우, 두 노드가 직선상에 있도록 만듬.
                if self.shift_pressed:
                    dx = abs(start.X - nx)
                    dy = abs(start.Y - ny)

                    if dx == dy == 0:
                        return

                    if dx < dy:
                        end.X = start.X
                    else:
                        end.Y = start.Y

                    # 노드의 위치가 변경될 수 있으므로, 화면을 지워줌.
                    self.eraseCanvas()

                path = Path(start, end)

                # 두 노드사이 중복되는 path 제외
                for p in self.paths:
                    if path.start == p.start and path.end == p.end\
                            or path.start == p.end and path.end == p.start:
                        return

                start.count += 1
                if start.count > 2:
                    start.isCross = True

                end.count += 1
                if end.count > 2:
                    end.isCross = True

                self.paths.append(path)

                self.side_bar.setDetail(self.selected_node)

                self.drawCanvas()

    # 화면 갱신 이벤트
    def paintEvent(self, event):
        if self.image_original:
            self.image_scaled = self.image_original.scaledToWidth(self.img_label.width())
            self.canvas_scaled = self.canvas.scaled(self.canvas_label.width(), self.canvas_label.height())

            # Convert QImage to QPixmap
            # QPixmap은 수정이, QImage는 출력이 안되기 때문.
            pixmap = QPixmap(self.image_scaled)
            self.img_label.setPixmap(pixmap)

            pixmap = QPixmap(self.canvas_scaled)
            self.canvas_label.setPixmap(pixmap)

            # path의 미리보기가 있다면 보여줌.
            if self.canvas_prev:
                pixmap = QPixmap(self.canvas_prev.scaled(self.canvas_label.width(), self.canvas_label.height()))
                self.canvas_label.setPixmap(pixmap)

# Run App.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = app.desktop()  # 컴퓨터 전체 화면 rect
    win = MainPage(screen.screenGeometry()) # 메인 화면 생성
    win.show()  # 화면 띄우기
    app.exec_() # 루프 실행