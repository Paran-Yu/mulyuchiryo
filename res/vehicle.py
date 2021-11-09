from time import sleep
from math import atan2, degrees, isclose, sqrt, dist

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
        self.cmd = ""
        self.path = []
        self.count = 0
        self.dCharge = 0

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
            self.velocity -= self.ACCEL
        else:
            self.velocity += self.ACCEL
            if self.velocity > self.MAX_SPEED:  # 최고속도 제한
                self.velocity = self.MAX_SPEED
        # 속도는 현재 위치에 영향을 준다 (벡터값으로 바꾸거나, 각도에 따라 바꿔야할듯)->현재는 직각으로만 움직이므로...
        # 현재 위치를 벡터값으로 하고 velocity에 방향에 더해주는 방법...?
        if isclose(self.angle, 90):
            self.x += self.velocity
        elif isclose(self.angle, 270):
            self.x -= self.velocity
        elif isclose(self.angle, 0):
            self.y += self.velocity
        elif isclose(self.angle, 180):
            self.y -= self.velocity

        # 어느 노드에 도착했다는 것은 어떻게 할까? distance, x, y가 정확히 0이 될 일은 거의 없을텐데->일정 threshold 이하면 그 위치로 보정
        if distance <= 0.000001 and self.velocity <= 0.01:
            self.x = [node for node in NODE_LIST if node.NUM == self.path[0]][0].x
            self.y = [node for node in NODE_LIST if node.NUM == self.path[0]][0].y
                

    def turn(self):
        # 각도 차이에 따라 더할지 뺄지 로직 필요
        if self.getAngle([node for node in NODE_LIST if node.NUM == self.path[0]][0]) == 0:
            if 0 < self.angle <= 180:
                self.angle -= (self.ROTATE_SPEED)    # 초
            elif 180 < self.angle < 360:
                self.angle += (self.ROTATE_SPEED)    # 초
        elif self.getAngle([node for node in NODE_LIST if node.NUM == self.path[0]][0]) == 90:
            if 90 < self.angle <= 270:
                self.angle -= (self.ROTATE_SPEED)    # 초
            elif 270 < self.angle or self.angle < 90:
                self.angle += (self.ROTATE_SPEED)    # 초
        elif self.getAngle([node for node in NODE_LIST if node.NUM == self.path[0]][0]) == 180:
            if 180 < self.angle < 360:
                self.angle -= (self.ROTATE_SPEED)    # 초
            elif 0 <= self.angle < 180:
                self.angle += (self.ROTATE_SPEED)    # 초
        elif self.getAngle([node for node in NODE_LIST if node.NUM == self.path[0]][0]) == 270:
            if 270 < self.angle or self.angle <= 90:
                self.angle -= (self.ROTATE_SPEED)    # 초
            elif 90 < self.angle < 270:
                self.angle += (self.ROTATE_SPEED)    # 초
            
        # 360도는 0도다
        if 360 < self.angle:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360
                
        # 직각이 아닐때는 정확히 계산해줘야한다. 아직 로직 완성 못함
        # if (angle_diff%360) 
        # self.angle += (self.ROTATE_SPEED)    # 초

    def load(self, port_num):
        if self.loaded == False:
            # 포트가 load가능한 상태인지 확인
            pass
            self.count += 1
            if self.count >= 30:
                self.count = 0
                PORT_LIST[port_num].LOAD()
                # 대기 상태로 전환
                self.status = 11
                self.loaded = 1
        else:
            return False

    def unload(self, port_num):
        if self.loaded:
            # 포트가 unload가능한 상태인지 확인
            pass
            self.count += 1
            if self.count >= 30:
                self.count = 0
                PORT_LIST[port_num].UNLOAD()
                # 대기 상태로 전환
                self.status = 10
                self.loaded = 0
        else:
            return False

    def getNode(self):
        return self.node        # 이동중일때는 가장 최근 회전한 노드, 그렇지 않은 경우 현재 위치의 노드 반환

    def getPos(self):
        return (self.x, self.y)

    def getDesti(self):
        if self.path.length != 0:
            return self.path[-1]    # 최종 목표 노드 (self.desti_node와 동일)
        else:                       # 도착지가 없는 경우
            return -1

    def getBattery(self):
        return self.battery

    def getStatus(self):
        return self.status
    
    def getBrakeDis(self):
        return (self.velocity**2)/(2*self.ACCEL)

    def checkCrash(self, car):
        distance = sqrt((self.x - car.x)**2 + (self.y - car.y)**2)
        if distance <= self.diagonal/2 + car.diagonal/2:
            return True
        else:
            return False

    def getAngle(self, destination):
        # 벡터 말고 좌표평면계로 계산, 북이 0도, 동 90, 남 180, 서 270
        # atan2 결과값은 -180~180이므로, 방위각(정북과 타겟좌표 사이의 각도)을 구하자
        radian = atan2(destination.y - self.y , destination.x - self.x)
        degree = degrees(radian)
        if degree > 0:
            degree -= 360
        degree = abs(degree)
        degree = (degree+90)%360
        return degree

    def vehicle_routine(self, node_list):
        # 1. 충돌 감지
        # n^2의 위험이 있어 검토 필요

        # 2. 작업 - status 업데이트
        # path 이동
        if len(self.path) != 0:
            self.move(node_list)
        # 이동 완료시 작업 수행
        else:
            # status와 현재 받은 cmd를 분리
            # load
            if self.cmd == 22:
                if self.status != 30:
                    self.status = 30
                    node_list[self.desti_node - 1].status = -1
                self.count += 1
                if self.count == self.LOAD_SPEED:
                    self.count = 0
                    self.cmd = 10
                    self.status = 10
                    self.loaded = 1
                    node_list[self.desti_node - 1].status = 0
            # unload
            elif self.cmd == 21:
                if self.status != 40:
                    self.status = 40
                    node_list[self.desti_node - 1].status = -1
                self.count += 1
                if self.count == self.LOAD_SPEED:
                    self.count += 1
                    self.cmd = 10
                    self.status = 10
                    self.loaded = 0
                    node_list[self.desti_node - 1].status = 0
            # wait
            elif self.cmd == 20:
                self.cmd = 10
                self.status = 10
            # charge
            elif self.cmd == 23:
                self.cmd = 10
                self.status = 80

        # 3. 배터리 충/방전
        if self.status == 10:
            self.battery -= self.DISCHARGE_WAIT
        elif self.status == 80:     # 명령을 받을 수 없는 충전 상태
                self.cnt += 1
                self.dCharge += self.CHARGE_SPEED
                self.battery += self.CHARGE_SPEED
            # 종료조건
            if self.battery > 60:
                if self.cnt > 300 or self.dCharge > 10:
                    self.cnt = 0
                    self.dCharge = 0
                    self.status = 81
        elif self.status == 81:     # 명령을 받을 수 있는 충전 상태
            if self.battery < 100:
                self.battery += self.CHARGE_SPEED
        else:
            self.battery -= self.DISCHARGE_WORK

        # 4. DB에 저장
        # 상위 경로에서 처리
