import sys
import os.path
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import main

import random
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from sidebar import SideBar
from selector import Selector
from classes import *
from scale import *
from vehicleEditor import VehicleEditor
import pickle

path = os.path.abspath(os.path.dirname(__file__))

class Context:
    def __init__(self):
        self.main = None
        self.class_list = [Node, Port, WaitPoint, Path]
        self.scale = 1
        self.capa = 1
        self.simulation_speed = 1
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

        self.actual_length = None
        self.scale_pressed = None
        self.layout_name = None

        self.initUI()

    def initUI(self):
        self.initCentralWidget()    # 메인 화면 생성
        self.initMainMenu()     # 메인 메뉴 생성
        self.initSubMenu()      # 서브 메뉴 생성
        self.showFullScreen()   # 전체화면 모드
        self.setWindowTitle("물류 치료")    # 프로그램 제목
        self.setWindowIcon(QIcon(path + "/resources/image/favicon.png"))  # 프로그램 실행 아이콘

    # 메인 메뉴 생성
    def initMainMenu(self):
        menu_width = 110

        # 메뉴 바 생성.
        self.menu_wrapper = QWidget(self)
        self.menu_wrapper.resize(self.rect.width(), self.menu_wrapper_height)
        self.menu_wrapper.setObjectName("menu-wrapper")
        self.menu_wrapper.setStyleSheet("#menu-wrapper{"
                                       "background-color: #004761;"
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
                               "background-color: #004761;"
                               "color:white;"
                               "font-size: 17px;"
                               "border: none;"
                               "}"
                               "#main-menu:hover{"
                               "background-color: #93A9BB;"
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
                                            #"background-color: #CCCCCC;"
                                            "background-color: #DDDDDD;"
                                            #"border: 1px solid #AAAAAA;"
                                            "}")
        #"background-image: url('./resources/image/save.png')"
        # 서브 메뉴 항목 추가
        # file
        #btn_save = QPushButton("Save", self.sub_menu_wrapper)
        btn_save = QPushButton(self.sub_menu_wrapper)
        btn_save.clicked.connect(self.save)
        btn_save.setIcon(QIcon(QPixmap(path + "/resources/image/save2.png")))
        btn_save.setIconSize(QSize(80, 80))

        #btn_save_as = QPushButton("Save\nAs", self.sub_menu_wrapper)
        btn_save_as = QPushButton(self.sub_menu_wrapper)
        btn_save_as.clicked.connect(self.saveAs)
        btn_save_as.setIcon(QIcon(QPixmap(path + "/resources/image/save as2.png")))
        btn_save_as.setIconSize(QSize(80, 80))

        #btn_load = QPushButton("Load", self.sub_menu_wrapper)
        btn_load = QPushButton(self.sub_menu_wrapper)
        btn_load.clicked.connect(self.load)
        btn_load.setIcon(QIcon(QPixmap(path + "/resources/image/load2.png")))
        btn_load.setIconSize(QSize(80, 80))

        bar1 = QLabel(self.sub_menu_wrapper)
        bar1.setStyleSheet("background-color: #999999;")
        bar1.setGeometry(262, padding, 1, self.sub_menu_wrapper.height() - (2 * padding))

        #btn_open_layout = QPushButton("Open\nLayout", self.sub_menu_wrapper)
        btn_open_layout = QPushButton(self.sub_menu_wrapper)
        btn_open_layout.clicked.connect(self.openLayout)
        btn_open_layout.setIcon(QIcon(QPixmap(path + "/resources/image/open layout2.png")))
        btn_open_layout.setIconSize(QSize(80, 80))

        bar2 = QLabel(self.sub_menu_wrapper)
        bar2.setStyleSheet("background-color: #999999;")
        bar2.setGeometry(347, padding, 1, self.sub_menu_wrapper.height() - (2 * padding))

        #btn_set_scale = QPushButton("Set\nScale", self.sub_menu_wrapper)
        btn_set_scale = QPushButton(self.sub_menu_wrapper)
        btn_set_scale.clicked.connect(self.setScale)
        btn_set_scale.setCheckable(True)
        btn_set_scale.setIcon(QIcon(QPixmap(path + "/resources/image/set scale2.png")))
        btn_set_scale.setIconSize(QSize(80, 80))

        bar3 = QLabel(self.sub_menu_wrapper)
        bar3.setStyleSheet("background-color: #999999;")
        bar3.setGeometry(432, padding, 1, self.sub_menu_wrapper.height() - (2 * padding))

        #btn_close = QPushButton("Close", self.sub_menu_wrapper)
        btn_close = QPushButton(self.sub_menu_wrapper)
        btn_close.clicked.connect(self.close)
        btn_close.setIcon(QIcon(QPixmap(path + "/resources/image/close.png")))
        btn_close.setIconSize(QSize(80, 80))

        # draw
        self.draw_normal = [
            QPixmap(path + "/resources/image/nodes.png"),
            QPixmap(path + "/resources/image/port.png"),
            QPixmap(path + "/resources/image/wp.png"),
            QPixmap(path + "/resources/image/path.png"),
        ]
        self.draw_clicked = [
            QPixmap(path + "/resources/image/nodes selected.png"),
            QPixmap(path + "/resources/image/port selected.png"),
            QPixmap(path + "/resources/image/wp selected.png"),
            QPixmap(path + "/resources/image/path selected.png"),
        ]

        #btn_node = QPushButton("Node", self.sub_menu_wrapper)
        btn_node = QPushButton(self.sub_menu_wrapper)
        btn_node.toggled.connect(lambda: self.changeTools(0))
        btn_node.setCheckable(True)
        btn_node.setIcon(QIcon(self.draw_normal[0]))
        btn_node.setIconSize(QSize(80, 80))

        #btn_port = QPushButton("Port", self.sub_menu_wrapper)
        btn_port = QPushButton(self.sub_menu_wrapper)
        btn_port.toggled.connect(lambda: self.changeTools(1))
        btn_port.setCheckable(True)
        btn_port.setIcon(QIcon(self.draw_normal[1]))
        btn_port.setIconSize(QSize(80, 80))

        #btn_wait_point = QPushButton("Wait\nPoint", self.sub_menu_wrapper)
        btn_wait_point = QPushButton(self.sub_menu_wrapper)
        btn_wait_point.toggled.connect(lambda: self.changeTools(2))
        btn_wait_point.setCheckable(True)
        btn_wait_point.setIcon(QIcon(self.draw_normal[2]))
        btn_wait_point.setIconSize(QSize(80, 80))

        btn_path = QPushButton(self.sub_menu_wrapper)
        btn_path.toggled.connect(lambda: self.changeTools(3))
        btn_path.setCheckable(True)
        btn_path.setIcon(QIcon(self.draw_normal[3]))
        btn_path.setIconSize(QSize(80, 80))

        # Vehicle
        btn_vehicle_edit = QPushButton(self.sub_menu_wrapper)
        btn_vehicle_edit.clicked.connect(self.editVehicle)
        btn_vehicle_edit.setIcon(QIcon(QPixmap(path + "/resources/image/edit.png")))
        btn_vehicle_edit.setIconSize(QSize(80, 80))

        # Simulator
        btn_play = QPushButton(self.sub_menu_wrapper)
        btn_play.clicked.connect(self.play)
        btn_play.setIcon(QIcon(QPixmap(path + "/resources/image/play.png")))
        btn_play.setIconSize(QSize(80, 80))

        btn_stop = QPushButton(self.sub_menu_wrapper)
        btn_stop.clicked.connect(self.stop)
        btn_stop.setIcon(QIcon(QPixmap(path + "/resources/image/stop.png")))
        btn_stop.setIconSize(QSize(80, 80))

        btn_set_oper = QPushButton(self.sub_menu_wrapper)
        btn_set_oper.clicked.connect(self.setOperationData)
        btn_set_oper.setIcon(QIcon(QPixmap(path + "/resources/image/oper data.png")))
        btn_set_oper.setIconSize(QSize(80, 80))

        # report
        btn_util_rate = QPushButton(self.sub_menu_wrapper)
        btn_util_rate.clicked.connect(self.showUtilizationRate)
        btn_util_rate.setIcon(QIcon(QPixmap(path + "/resources/image/util rate.png")))
        btn_util_rate.setIconSize(QSize(80, 80))

        btn_charge_rate = QPushButton("Charge\nRate", self.sub_menu_wrapper)
        btn_charge_rate.clicked.connect(self.showChargeRate)

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
                btn_play,
                btn_stop,
                btn_set_oper,
            ],
            # report
            [
                btn_util_rate,
                btn_charge_rate,
            ],
        ]

        for mainMenu in self.subMenus:
            left = 0
            for menu in mainMenu:
                menu.setObjectName("sub-menu")
                menu.setStyleSheet("#sub-menu{"
                                   #"background-color:white;"
                                   "font-size: 17px;"
                                   "border:none;"
                                   "}"
                                   "#sub-menu:hover{"
                                   "background-color: #D7EDFF;"
                                   #A4BACC
                                   "}"
                                   "#sub-menu:pressed{"
                                   "background-color: #C5DCFF;"
                                   "}")
                menu.resize(sub_menu_size, sub_menu_size)
                left += padding + 5
                menu.move(left, padding)
                left += sub_menu_size
                menu.hide()
        self.subMenus[0].append(bar1)
        self.subMenus[0].append(bar2)
        self.subMenus[0].append(bar3)

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
                    self.context.scale = pickle.load(f)
                    self.context.capa = pickle.load(f)
                    self.context.simulation_speed = pickle.load(f)
                    self.context.v_count = pickle.load(f)

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
                pickle.dump(self.context.scale, f)
                pickle.dump(self.context.capa, f)
                pickle.dump(self.context.simulation_speed, f)
                pickle.dump(self.context.v_count, f)
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
                pickle.dump(self.context.scale, f)
                pickle.dump(self.context.capa, f)
                pickle.dump(self.context.simulation_speed, f)
                pickle.dump(self.context.v_count, f)
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

            self.image_original.load(fname[0])
            # 불러온 이미지와 같은 크기의 투명 도화지. 이 위에 그림을 그림.
            self.canvas = QImage(self.image_original.width(), self.image_original.height(),
                                 QImage.Format_ARGB32_Premultiplied)
            self.canvas.fill(0x00ffffff)

            self.canvas_height_scale = (self.rect.height() - self.canvas_label.y()) \
                                       * self.canvas.height() / self.canvas_label.height()

    def setOperationData(self):
        if self.image_original:
            qd = OperationData()
            qd.setGeometry(self.rect.width() * 0.3, self.rect.height() * 0.3,
                           self.rect.width() * 0.2, self.rect.height() * 0.2)
            qd.initUI(self.context.capa, self.context.simulation_speed)
            if qd.exec_() and qd.edit_capa.text() and qd.edit_speed.text():
                capa = int(qd.edit_capa.text())
                simulation_speed = int(qd.edit_speed.text())

                self.context.capa = capa
                self.context.simulation_speed = simulation_speed

    def setScale(self):
        # 다시 누른 경우 창이 뜨지 않음
        if self.image_original and self.subMenus[0][4].isChecked():
            length = 0
            if self.actual_length:
                length = self.actual_length

            qd = Scale(length)
            qd.setGeometry(self.rect.width() * 0.3, self.rect.height() * 0.3,
                           self.rect.width() * 0.2, self.rect.height() * 0.1)

            qd.initUI()
            result = qd.exec_()

            if result:
                if qd.edit_length.text():
                    self.actual_length = int(qd.edit_length.text())
            else:
                self.subMenus[0][4].setChecked(False)

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

    # 시뮬레이션 시작
    def play(self):
        # 테스트 시 XML이 변경될 가능성이 있으므로 주석처리 했음.
        # 그린 레이아웃을 적용하고 싶다면 주석 해제하고 사용.
        # self.XML()

        main.read_map()
        main.start_simulate()

    # 시뮬레이션 일시정지
    def stop(self):
        pass

    # XML 파일 추출
    def XML(self):
        # 전체 노드 수
        count_node = len(self.nodes)
        count_ports = len(self.ports)
        count_wp = len(self.wait_points)

        count = count_node + count_ports + count_wp

        # 방문중인 노드 제외
        visited = []
        for i in range(count):
            visited.append(False)

        # AGV의 각도
        angle = ["0", "90", "180", "270"]

        with open("data.xml", 'w', encoding="UTF-8") as f:
            # 인코딩 지정
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')

            # 레이아웃 저장
            f.write('<layout>\n')

            # 이미지 파일 저장
            f.write('\t<img>\n')
            # 경로
            f.write('\t\t<img_path>' + self.layout_name[0] + '</img_path>\n')
            # 이름
            f.write('\t\t<name>layout.jpg</name>\n')
            f.write('\t</img>\n')

            # 운영 데이터
            f.write('\t<map>\n')
            f.write("\t\t<width>" + str(self.rect.width()) + "</width>\n")    # 가로 길이
            f.write("\t\t<scale>" + str(self.context.scale) + "</scale>\n")   # 스케일 정보
            f.write("\t\t<capa>" + str(self.context.capa) + "</capa>\n")      # 일일 반송량
            f.write('\t</map>\n')

            # 포트
            f.write('\t<ports>\n')
            for port in self.ports:
                f.write('\t\t<port>\n')
                f.write("\t\t\t<num>" + str(port.NUM) + "</num>\n")
                x, y = self.convertCanvasToMonitor(port.X, port.Y)
                f.write("\t\t\t<x>" + str(x) + "</x>\n")
                f.write("\t\t\t<y>" + str(y) + "</y>\n")
                f.write("\t\t\t<name>" + str(port.PORT_NAME) + "</name>\n")
                f.write("\t\t\t<type>" + str(port.TYPE) + "</type>\n")
                f.write("\t\t\t<freq>" + str(port.FREQ) + "</freq>\n")
                f.write("\t\t\t<v_type>" + str(port.V_TYPE) + "</v_type>\n")
                # 연결된 unload 포트 목록
                f.write("\t\t\t<unload>")
                for connected_port in port.UNLOAD_LIST:
                    f.write(str(connected_port))    # Unload port NUM
                f.write("</unload>\n")
                f.write('\t\t</port>\n')
            f.write('\t</ports>\n')

            # 대기 장소
            f.write('\t<waits>\n')
            for wait_point in self.wait_points:
                f.write('\t\t<wait>\n')
                f.write("\t\t\t<num>" + str(wait_point.NUM) + "</num>\n")
                x, y = self.convertCanvasToMonitor(wait_point.X, wait_point.Y)
                f.write("\t\t\t<x>" + str(x) + "</x>\n")
                f.write("\t\t\t<y>" + str(y) + "</y>\n")
                f.write("\t\t\t<name>" + str(wait_point.WAIT_NAME) + "</name>\n")
                f.write("\t\t\t<charge>" + ("Y" if wait_point.CHARGE else "N") + "</charge>\n")
                f.write('\t\t</wait>\n')
            f.write('\t</waits>\n')

            # 노드
            f.write('\t<nodes>\n')
            for node in self.nodes:
                f.write('\t\t<node>\n')
                f.write("\t\t\t<num>" + str(node.NUM) + "</num>\n")
                x, y = self.convertCanvasToMonitor(node.X, node.Y)
                f.write("\t\t\t<x>" + str(x) + "</x>\n")
                f.write("\t\t\t<y>" + str(y) + "</y>\n")
                f.write("\t\t\t<isCross>" + ("Y" if node.isCross else "N") + "</isCross>\n")
                f.write('\t\t</node>\n')
            f.write('\t</nodes>\n')

            # 경로
            f.write('\t<paths>\n')
            for path in self.paths:
                f.write('\t\t<path>\n')
                f.write("\t\t\t<start>" + str(path.start.NUM) + "</start>\n")   # start NUM
                f.write("\t\t\t<end>" + str(path.end.NUM) + "</end>\n")         # end NUM
                f.write('\t\t</path>\n')
            f.write('\t</paths>\n')

            # AGV
            f.write('\t<vehicles>\n')
            for vtype in self.vehicles:
                for vehicle in vtype:
                    f.write('\t\t<vehicle>\n')
                    f.write("\t\t\t<num>" + str(vehicle.NUM) + "</num>\n")
                    f.write("\t\t\t<name>" + str(vehicle.NAME) + "</name>\n")
                    f.write("\t\t\t<type>" + str(vehicle.TYPE) + "</type>\n")

                    # AGV 랜덤 배치
                    idx = random.randrange(0, count)
                    while visited[idx]:
                        # 이미 배치된 노드 패스
                        idx = random.randrange(0, count)

                    visited[idx] = True
                    type = 0
                    if idx < count_node:    # Node. position[0][idx]
                        type = 0
                    elif idx < count_node + count_ports:  # Port. position[1][idx]
                        type = 1
                        idx -= (count_node)
                    else:
                        type = 2
                        idx -= (count_node + count_ports)

                    f.write("\t\t\t<node>" + str(self.positions[type][idx].NUM) + "</node>\n")
                    f.write("\t\t\t<angle>" + angle[random.randrange(0, 4)] + "</angle>\n")
                    f.write("\t\t\t<width>" + str(vehicle.WIDTH) + "</width>\n")
                    f.write("\t\t\t<height>" + str(vehicle.HEIGHT) + "</height>\n")
                    f.write("\t\t\t<diagonal>" + str(vehicle.DIAGONAL) + "</diagonal>\n")
                    f.write("\t\t\t<rotate_speed>" + str(vehicle.ROTATE_SPEED) + "</rotate_speed>\n")
                    f.write("\t\t\t<accel>" + str(vehicle.ACCEL) + "</accel>\n")
                    f.write("\t\t\t<max_speed>" + str(vehicle.MAX_SPEED) + "</max_speed>\n")
                    f.write("\t\t\t<lu_type>" + str(vehicle.LU_TYPE) + "</lu_type>\n")
                    f.write("\t\t\t<load_speed>" + str(vehicle.LOAD_SPEED) + "</load_speed>\n")
                    f.write("\t\t\t<charge_speed>" + str(vehicle.CHARGE_SPEED) + "</charge_speed>\n")
                    f.write("\t\t\t<discharge_work>" + str(vehicle.DISCHARGE_WORK) + "</discharge_work>\n")
                    f.write("\t\t\t<discharge_wait>" + str(vehicle.DISCHARGE_WAIT) + "</discharge_wait>\n")
                    # TODO: Erase and Refactoring Simulator. Dupleicated with `node`, `angle`.
                    f.write("\t\t\t<start_node>" + str(self.positions[type][idx].NUM) + "</start_node>\n")
                    f.write("\t\t\t<start_angle>" + angle[random.randrange(0, 4)] + "</start_angle>\n")
                    f.write('\t\t</vehicle>\n')
            f.write('\t</vehicles>\n')

            f.write('</layout>\n')
            f.close()

    # AGV 전체 가동률 그래프 출력
    def showUtilizationRate(self):
        pass

    # AGV의 충전률
    def showChargeRate(self):
        pass

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

                    qp.setPen(QPen(QColor(0, 0, 0), 5))
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

            qp.setPen(QPen(QColor(0, 0, 0), 5))
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

            ## Scale 범위 지정
            #  실제 길이를 입력했고, 버튼이 눌려있는 상태라면
            if self.actual_length and self.subMenus[0][4].isChecked():
                if self.scale_pressed:
                    start = self.scale_pressed
                    end = e.x()

                    diff = abs(end-start)
                    self.context.scale = round(self.actual_length / diff, 1)

                    self.subMenus[0][4].setChecked(False)

                    self.scale_pressed = None
                else:
                    self.scale_pressed = e.x()

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

                if type == -1:
                    return

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

    def convertCanvasToMonitor(self, x, y):
        nx = x / self.canvas.width() * self.canvas_label.width()
        ny = y / self.canvas_height_scale * self.rect.height()

        return int(nx), int(ny)

# Run App.
if __name__ == '__main__':
    # 이 파일로 실행한다면, play 함수 호출 시
    # 같은 디렉토리 내에 example.png, data.xml이 존재해야함.
    app = QApplication(sys.argv)
    screen = app.desktop()  # 컴퓨터 전체 화면 rect
    win = MainPage(screen.screenGeometry()) # 메인 화면 생성
    win.show()  # 화면 띄우기
    app.exec_() # 루프 실행