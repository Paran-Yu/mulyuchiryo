<<<<<<< HEAD
from math import atan2, degrees, isclose, sqrt, dist
=======
from math import atan2, degrees, radians, sqrt, sin, cos
>>>>>>> feature/vehicle-routine


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
        self.BREAK_PARAM = 1.8
        self.NODE_TH = 200
        self.ROTATE_TH = -1

        self.x = -1
        self.y = -1
        self.node = -1
        self.desti_node = -1
        self.velocity = -1
        self.angle = -1
        self.status = 0
        self.loaded = 0
        self.battery = -1
<<<<<<< HEAD
        self.path = []
=======
        self.cmd = ""
        self.path = []
        self.turn_flag = 0
        self.last_flag = 0
        self.turning = -1
        self.dAngle = 0
        self.desti_angle = 0
>>>>>>> feature/vehicle-routine
        self.count = 0
        self.dCharge = 0

<<<<<<< HEAD
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
        coord_diff = tuple(map(lambda i, j: i - j, [node for node in NODE_LIST if node.NUM == self.path[0]][0].getPos(), self.getPos()))
        # 벡터->스칼라 변환 필요. 같은 방위각이므로 x,y 중 하나는 0일 것임.
        if isclose(coord_diff[0], 0):
            distance = coord_diff[1]
=======
    def command(self, path, cmd):
        self.path = path
        self.cmd = cmd
        self.desti_node = self.path[-1]

    def move(self, node_list):
        print("move!")
        # 1. 다음 목표 node가 정지하는 node인가
        next_node = node_list[self.path[0] - 1].getPos()
        dx = next_node[0] - self.x
        dy = next_node[1] - self.y
        print("dx, dy: ", dx, dy)
        if self.turn_flag == 1 or self.last_flag == 1:
            pass
        elif len(self.path) == 1:
            # next node가 마지막 목표라면 멈춤
            self.last_flag = 1
>>>>>>> feature/vehicle-routine
        else:
            # 회전하는 노드라면 멈춤
            nextnext_node = node_list[self.path[1] - 1].getPos()
            dx1 = nextnext_node[0] - next_node[0]
            dy1 = nextnext_node[1] - next_node[1]
            if dy == dy1 == 0:
                pass
            elif dy == 0 or dy1 == 0:
                self.turn_flag = 1
            elif dx/dy != dx1/dy1:
                self.turn_flag = 1

        # 2. 다음 목표 node와의 거리
        distance = sqrt(dx ** 2 + dy ** 2)
        print("distance: ", distance)
        print("brake: ", self.getBrakeDis())
        # 3. 회전 여부에 따른 가감속
        if self.turn_flag == 1 or self.last_flag == 1:
            if distance <= self.getBrakeDis():
                self.velocity -= self.ACCEL
            else:
                self.velocity += self.ACCEL
                if self.velocity > self.MAX_SPEED:  # 최고속도 제한
                    self.velocity = self.MAX_SPEED
        else:
            self.velocity += self.ACCEL
            if self.velocity > self.MAX_SPEED:  # 최고속도 제한
                self.velocity = self.MAX_SPEED

<<<<<<< HEAD
        # 어느 노드에 도착했다는 것은 어떻게 할까? distance, x, y가 정확히 0이 될 일은 거의 없을텐데->일정 threshold 이하면 그 위치로 보정
        if distance <= 0.000001 and self.velocity <= 0.01:
            self.x = [node for node in NODE_LIST if node.NUM == self.path[0]][0].X
            self.y = [node for node in NODE_LIST if node.NUM == self.path[0]][0].Y
                

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

    def load(self, NODE_LIST):
        if self.loaded == False:
            port = [node for node in NODE_LIST if node.NUM == self.node()][0]
            # 포트가 load가능한 상태인지 확인
            if port.status == 0:    # 1, -1일때는 load가능/load중
                return False
            # load 중으로 전환
            port.status = -1
            self.count += 1
            if self.count >= 30:
                self.count = 0
                # 포트 load 완료, status 업데이트
                port.status = 0
                # 대기 상태로 전환
                self.status = 11
                self.loaded = 1
                # Core에 load된 차량 있다고 알림
        else:
            return False

    def unload(self, NODE_LIST):
        if self.loaded:
            port = [node for node in NODE_LIST if node.NUM == self.node()][0]
            # 포트가 unload가능한 상태인지 확인
            if port.status == 0:    # 1, -1일때는 load가능/load중
                return False
            # unload 중으로 전환
            self.status = -1
            self.count += 1
            if self.count >= 30:
                self.count = 0
                # 포트 unload 완료, status 업데이트
                port.status = 0
                # 대기 상태로 전환
                self.status = 10
                self.loaded = 0
                # Core에 unload된 차량 있다고 알림
        else:
            return False
=======
        # 4. x, y 좌표 갱신
        print("angle: ", self.angle)
        print("velocity:", self.velocity)
        sin_dx = sin(radians(self.angle))
        cos_dy = cos(radians(self.angle))
        print(sin_dx, cos_dy)
        if abs(sin_dx) < 0.1: sin_dx = 0
        if abs(cos_dy) < 0.1: cos_dy = 0
        self.x += self.velocity * sin_dx
        self.y -= self.velocity * cos_dy
        print("sin,cos: ", sin_dx, cos_dy)
        print("x,y: ",self.x,self.y)

        # 5. node 근접시 도착한 것으로 보정
        if distance <= 200:
            self.x = next_node[0]
            self.y = next_node[1]
            # 6. 필요시 회전
            if self.turn_flag == 1:
                self.turning = 0
            else:
                self.path.pop(0)
                self.last_flag = 0


    def turn(self, node_list):
        print("turn!")
        # 1. 회전 방향 결정
        if self.turning == 0:
            cur_node = node_list[self.node - 1].getPos()
            next_node = node_list[self.path[0] - 1].getPos()
            nextnext_node = node_list[self.path[1] - 1].getPos()
            dx = next_node[0] - cur_node[0]
            dy = next_node[1] - cur_node[1]
            dx1 = nextnext_node[0] - next_node[0]
            dy1 = nextnext_node[1] - next_node[1]
            print(dx, dy, dx1, dy1)
            old_angle = self.get_angle(dx, dy)
            new_angle = self.get_angle(dx1, dy1)
            print(old_angle, new_angle)
            self.desti_angle = new_angle
            self.dAngle = new_angle - old_angle
            if self.dAngle > 180:
                self.dAngle = 360 - self.dAngle
            elif self.dAngle < -180:
                self.dAngle = 360 + self.dAngle
            print(self.dAngle)
            if self.dAngle > 0:
                # CW
                self.turning = 1
            else:
                # CCW
                self.turning = 2

            print(self.turning)
        # 2. 실제 회전
        # CW
        if self.turning == 1:
            self.angle += self.ROTATE_SPEED
            if self.angle >= 360:
                self.angle -= 360
        # CCW
        elif self.turning == 2:
            self.angle -= self.ROTATE_SPEED
            if self.angle < 0:
                self.angle += 360

        # 3. turn 완료 근사 및  관련 값 reset
        if abs(self.angle - self.desti_angle) < 18:
            self.angle = self.desti_angle
            self.turn_flag = 0
            self.turning = -1
            self.path.pop(0)
>>>>>>> feature/vehicle-routine

    def getNode(self):
        return self.node

    def getPos(self):
        return (self.x, self.y)

    def getDesti(self):
        if len(self.path) != 0:
            return self.path[-1]    # 최종 목표 노드 (self.desti_node와 동일)
        else:                       # 도착지가 없는 경우
            return -1

    def getBattery(self):
        return self.battery

    def getStatus(self):
        return self.status
    
    def getBrakeDis(self):
        return (self.velocity**2)/(2*self.ACCEL)*self.BREAK_PARAM

    def checkCrash(self, car):
<<<<<<< HEAD
        # 1. self와 car 두 점 사이의 거리 구하기
        # 1) 피타고라스 정리
        # distance = sqrt((self.x - car.x)**2 + (self.y - car.y)**2)
        # 2) math.dist()
        s = [self.x, self.y]
        c = [car.x, car.y]
        distance = dist(s, c)
        # 2. 두 점 사이의 거리 < self.diagonal/2 + car.diagonal/2 이면 충돌
=======
        distance = sqrt((self.x - car.x)**2 + (self.y - car.y)**2)
>>>>>>> feature/vehicle-routine
        if distance <= self.diagonal/2 + car.diagonal/2:
            return True
        else:
            return False

<<<<<<< HEAD
    def getAngleTo(self, destination):
        # 벡터 말고 좌표평면계로 계산, 북이 0도, 동 90, 남 180, 서 270
        # atan2 결과값은 -180~180이므로, 방위각(정북과 타겟좌표 사이의 각도)을 구하자
        radian = atan2(destination.y - self.y , destination.x - self.x)
=======
    def get_angle(self, dx, dy):
        radian = atan2(dx, -dy)
>>>>>>> feature/vehicle-routine
        degree = degrees(radian)
        if degree < 0:
            degree += 360
        return degree

<<<<<<< HEAD
    def vehicle_routine(self, NODE_LIST):
        # 충돌여부 조사 (다른 차량 정보 모두 필요) -> 모든 차량 정보일텐데 본인은 어떻게 제외시킬까?->main.py에서 별도 스레드로 관리

        # 로직 설명
        # 중요한 2가지 변수: status, path(node, desti_node 포함함)
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
                
            self.battery -= self.DISCHARGE_WORK

        # LOAD
        elif self.status == 30:
            self.load(NODE_LIST)
            self.battery -= self.DISCHARGE_WORK
            
        # UNLOAD
        elif self.status == 40:
            self.unload(NODE_LIST)
            self.battery -= self.DISCHARGE_WORK
        
        # 충전 / 물건 들고 충전
        elif self.status == 80 or self.status == 81:
            charger = [node for node in NODE_LIST if node.NUM == self.node()][0]
            # 충전소가 충전이 가능한 상태인가?
            pass    # 다른 차량과 충돌한게 아니라면 충전소에는 제약이 없는 것으로 알고 있음
            # 충전기를 충전중 상태로 전환
            charger.using = True
            # 배터리 충전
            self.battery += self.CHARGE_SPEED
            # 배터리 과충전 불가, 충전 종료?
            if self.battery >= 100:
                self.battery = 100
                # 충전 완료 됐다고 Core에 알리기
                pass
                # 충전 완료 했으니 충전기로 부터 해제
                charger.using = False
                # 대기로 status 전환
                self.status = 10


        # 에러
        elif self.status == 91 or self.status == 99:
            pass
        
=======
    def vehicle_routine(self, node_list):
        # 1. 충돌 감지
        # n^2의 위험이 있어 검토 필요

        # 2. 작업 - status 업데이트
        # path 이동
        print("cmd start!: ", self.cmd)
        if len(self.path) != 0:
            if self.turning == -1:
                self.move(node_list)
            else:
                self.turn(node_list)
        # 이동 완료시 작업 수행
        else:
            # status와 현재 받은 cmd를 분리
            # load
            if self.cmd == 22:
                if self.status != 30:
                    self.status = 30
                    node_list[self.desti_node - 1].status = -1
                self.count += 1
                if self.count >= self.LOAD_SPEED:
                    self.count = 0
                    self.cmd = 10
                    self.status = 10
                    self.loaded = 1
                    node_list[self.desti_node - 1].status = 0
                print("load! - ", self.count)
            # unload
            elif self.cmd == 21:
                if self.status != 40:
                    self.status = 40
                    node_list[self.desti_node - 1].status = -1
                self.count += 1
                if self.count >= self.LOAD_SPEED:
                    self.count += 1
                    self.cmd = 10
                    self.status = 10
                    self.loaded = 0
                    node_list[self.desti_node - 1].status = 0
                print("unload! - ", self.count)
            # wait
            elif self.cmd == 20:
                self.cmd = 10
                self.status = 10
                print("wait!")
            # charge
            elif self.cmd == 23:
                self.cmd = 10
                self.status = 80
                print("charge!")

        # 3. 배터리 충/방전
        if self.status == 10:
            self.battery -= self.DISCHARGE_WAIT
        elif self.status == 80:     # 명령을 받을 수 없는 충전 상태
            self.count += 1
            self.dCharge += self.CHARGE_SPEED
            self.battery += self.CHARGE_SPEED
            # 종료 조건
            if self.battery > 60:
                if self.count > 300 or self.dCharge > 10:
                    self.count = 0
                    self.dCharge = 0
                    self.status = 81
        elif self.status == 81:     # 명령을 받을 수 있는 충전 상태
            if self.battery < 100:
                self.battery += self.CHARGE_SPEED
        else:
            self.battery -= self.DISCHARGE_WORK
        print("status: ", self.status)
        print("battery: ", self.battery)

        # 4. DB에 저장
        # 상위 경로에서 처리
>>>>>>> feature/vehicle-routine
