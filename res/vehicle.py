from time import sleep
from math import atan2, degrees, isclose

PORT_LIST = []
NODE_LIST = []
TIME = 1

class Vehicle:
    def __init__(self, name):
        super().__init__()

        self.NAME = name
        self.TYPE = "default"
        self.WIDTH = -1
        self.HEIGHT = -1
        self.DIAGONAL = -1
        self.ROTATE_SPEED = -1
        self.ACCEL = -1
        self.MAX_SPEED = -1
        self.LU_TYPE = "default"
        self.LOAD_SPEED = -1
        self.CHARGE_SPEED = -1
        self.DISCHARGE_WAIT = -1
        self.DISCHARGE_WORK = -1

        self.x = -1
        self.y = -1
        self.node = -1
        self.desti_node = -1
        self.velocity = -1
        self.angle = -1
        self.status = 0
        self.loaded = 0
        self.battery = -1
        self.path = []  # 각 노드(경유지)가 object일지 좌표일지 정해야할듯
        self.command_list = []
        self.count = 0

    # new_node로 이동
    def command(self, path, status):
        if self.status in [00, 10, 20, 22, 80] or self.path.length == 0:    
            self.count = 0
            self.path = path    
            self.desti_node = path[-1]  # desti_node는 path의 마지막 (path[-1]), self.node는 도착할때마다 업데이트
            self.status = status    # 충전소로 가서 충전하는건지, 대기하러 가는건지 명령 정보 필요. 20, 22 등 명령을 오버라이드 가능.
            return True
        else:
            # Core에 에러쏴주기: 이미 명령받고 이동(21, 40, 80) 중인 경우
            pass
            return False

    def move(self):
        coord_diff = [node for node in NODE_LIST if node.NUM == self.path[0]][0].getPos() - self.getPos() # 현재 목적지와의 거리 # (x, y)
        # 벡터->스칼라 변환 필요. 같은 방위각이므로 x,y 중 하나는 0일 것임.
        if isclose(coord_diff[0], 0):
            distance = coord_diff[1]
        else:
            distance = coord_diff[0]
        if distance <= self.getBrakeDis():  # 지금부터 브레이크를 밟아야 현재 목적지에서 정지
            self.velocity -= self.ACCEL/60 # velocity: m/min, ACCEL: m/min
        else:
            self.velocity += self.ACCEL/60 # velocity: m/min, ACCEL: m/min
            if self.velocity > self.MAX_SPEED:  # 최고속도 제한
                self.velocity = self.MAX_SPEED
        # 속도는 현재 위치에 영향을 준다 (벡터값으로 바꾸거나, 각도에 따라 바꿔야할듯)->현재는 직각으로만 움직이므로...
        # 현재 위치를 벡터값으로 하고 velocity에 방향에 더해주는 방법...?
        if isclose(self.angle, 90):
            self.x += self.velocity*100/6/TIME # m/min->1000mm/60sec->배속
        elif isclose(self.angle, 270):
            self.x -= self.velocity*100/6/TIME # m/min->1000mm/60sec->배속
        elif isclose(self.angle, 0):
            self.y += self.velocity*100/6/TIME # m/min->1000mm/60sec->배속
        elif isclose(self.angle, 180):
            self.y -= self.velocity*100/6/TIME # m/min->1000mm/60sec->배속

    def load(self, port_num):
        pass

    def unload(self, port_num):
        pass

    def getNode(self):
        pass

    def getPos(self):
        pass

    def getDesti(self):
        pass

    def getBattery(self):
        pass

    def getStatus(self):
        pass