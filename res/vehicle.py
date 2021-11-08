from math import atan2, degrees, isclose, sqrt, dist


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
        self.path = []
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
            return False

    def move(self, NODE_LIST):
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
                

    def turn(self, NODE_LIST):
        if self.getAngleTo([node for node in NODE_LIST if node.NUM == self.path[0]][0]) == 0:
            if 0 < self.angle <= 180:
                self.angle -= (self.ROTATE_SPEED)    # 초
            elif 180 < self.angle < 360:
                self.angle += (self.ROTATE_SPEED)    # 초
        elif self.getAngleTo([node for node in NODE_LIST if node.NUM == self.path[0]][0]) == 90:
            if 90 < self.angle <= 270:
                self.angle -= (self.ROTATE_SPEED)    # 초
            elif 270 < self.angle or self.angle < 90:
                self.angle += (self.ROTATE_SPEED)    # 초
        elif self.getAngleTo([node for node in NODE_LIST if node.NUM == self.path[0]][0]) == 180:
            if 180 < self.angle < 360:
                self.angle -= (self.ROTATE_SPEED)    # 초
            elif 0 <= self.angle < 180:
                self.angle += (self.ROTATE_SPEED)    # 초
        elif self.getAngleTo([node for node in NODE_LIST if node.NUM == self.path[0]][0]) == 270:
            if 270 < self.angle or self.angle <= 90:
                self.angle -= (self.ROTATE_SPEED)    # 초
            elif 90 < self.angle < 270:
                self.angle += (self.ROTATE_SPEED)    # 초

        if 360 < self.angle:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360
                
        # 직각이 아닐때는 정확히 계산해줘야한다. 아직 로직 완성 못함
        # if (angle_diff%360) 
        # self.angle += (self.ROTATE_SPEED)    # 초

    def load(self, PORT_LIST):
        if self.loaded == False:
            # 포트가 load가능한 상태인지 확인
            pass
            self.count += 1
            if self.count >= 30:
                self.count = 0
                PORT_LIST[self.node()].LOAD()  # PORT.LOAD() 메서드 필요
                # 대기 상태로 전환
                self.status = 11
                self.loaded = 1
        else:
            return False

    def unload(self, PORT_LIST):
        if self.loaded:
            # 포트가 unload가능한 상태인지 확인
            pass
            self.count += 1
            if self.count >= 30:
                self.count = 0
                PORT_LIST[self.node()].UNLOAD()    # PORT.UNLOAD() 메서드 필요
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
        # 1. self와 car 두 점 사이의 거리 구하기
        # 1) 피타고라스 정리
        # distance = sqrt((self.x - car.x)**2 + (self.y - car.y)**2)
        # 2) math.dist()
        s = [self.x, self.y]
        c = [car.x, car.y]
        distance = dist(s, c)
        # 2. 두 점 사이의 거리 < self.diagonal/2 + car.diagonal/2 이면 충돌
        if distance <= self.diagonal/2 + car.diagonal/2:
            return True
        else:
            return False

    def getAngleTo(self, destination):
        # 벡터 말고 좌표평면계로 계산, 북이 0도, 동 90, 남 180, 서 270
        # atan2 결과값은 -180~180이므로, 방위각(정북과 타겟좌표 사이의 각도)을 구하자
        radian = atan2(destination.y - self.y , destination.x - self.x)
        degree = degrees(radian)
        if degree > 0:
            degree -= 360
        degree = abs(degree)
        degree = (degree+90)%360
        return degree

    # 매 1초마다 실행
    def threadFunc(self, NODE_LIST, PORT_LIST):
        while True:
            # 충돌여부 조사 (다른 차량 정보 모두 필요) -> 모든 차량 정보일텐데 본인은 어떻게 제외시킬까?->main.py에서 별도 스레드로 관리

            # 로직 설명
            # 중요한 3가지 변수: status, path(node, desti_node 포함함), status
            # Core에서 명령이 내려오면 path, status 변화됨. (명령은 스레드 초 단위와 상관 없이 전달)
            # status와 path에 따라 차량은 이동을 시작하며
            # 목적지에 도착하면 path는 empty하며 status에 적힌 다음 명령을 실행함(대기, 충전, L, U 등), status 업데이트
            # 해당 명령이 종료되면(충전, L, U 끝), 대기로 전환, status 업데이트
            # 대기인 경우 명령을 받을 수 있음

            # 초기상태 / 대기 / 물건 들고 대기
            if self.status == 00 or self.status == 10 or self.status == 11:
                self.count += 1
                if self.count >= 5:
                    # 예외사항! count가 2일때 명령이 발생하면 count 초기화가 없음-> 명령 메서드에 count 초기화 추가
                    self.count = 0
                    # Core에 알림!
                    pass
                # 대기 배터리 방전
                self.battery -= self.DISCHARGE_WAIT

            # 대기를 위해 이동, UNLOAD 위해 이동 중, LOAD 위해 이동, 충전소로 이동
            elif self.status in [20, 21, 22, 23]:

                # 현재 경유지에 도착했다면
                if self.getPos() == [node for node in NODE_LIST if node.NUM == self.path[0]][0].getPos():
                    self.node = self.path.pop(0)    # node 갱신, path에서 삭제

                # 더 이상 목적지가 추가적으로 없다면 최종 목적지이므로 다음 명령 확인
                if self.path.length == 0:
                    if self.status == 20:
                        self.status = 10    # WAITING
                    elif self.status == 21: 
                        self.status = 40    # UNLOAD
                    elif self.status == 22:
                        self.status = 30    # LOAD
                    elif self.status == 23:
                        self.status = 80    # CHARGING
                
                # 목적지가 있다면 회전 & 가감속
                else:
                    angle_diff = self.getAngleTo([node for node in NODE_LIST if node.NUM == self.path[0]][0]) - self.angle
                    if angle_diff==0:   # 현재 목적지를 향해 보고 있다
                        self.move(NODE_LIST)
                    else:   # 현재 목적지를 보고 있지 않다면, 회전을 해야겠지
                        self.turn(NODE_LIST)
                    
                # 동작 배터리 방전
                self.battery -= self.DISCHARGE_WORK

            # LOAD
            elif self.status == 30:
                self.load(PORT_LIST)
                # 동작 배터리 방전
                self.battery -= self.DISCHARGE_WORK
                
            # UNLOAD
            elif self.status == 40:
                self.unload(PORT_LIST)
                # 동작 배터리 방전
                self.battery -= self.DISCHARGE_WORK
            
            # 충전 / 물건 들고 충전
            elif self.status == 80 or self.status == 81:
                # 충전소가 충전이 가능한 상태인가?
                # 배터리 충전
                self.battery += self.CHARGE_SPEED
                # 충전기를 충전중 상태로 전환
                WAIT_LIST[self.node()].CHARGE()
                # 배터리 과충전 불가
                if self.battery > 100:
                    self.battery = 100
                    # 충전 완료 됐다고 Core에 알리기
                    # 충전 완료 했으니 충전기로 부터 해제


            # 에러
            elif self.status == 91 or self.status == 99:
                pass
            