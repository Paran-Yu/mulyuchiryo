from math import atan2, degrees, radians, sqrt, sin, cos

class Vehicle:
    def __init__(self, name):
        super().__init__()

        self.NUM = -1
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
        self.BREAK_PARAM = 2
        self.NODE_TH = 200

        self.x = -1
        self.y = -1
        self.back = False
        self.node = -1
        self.desti_node = -1
        self.velocity = -1
        self.angle = -1
        self.status = 0
        self.loaded = 0
        self.battery = -1
        self.cmd = ""
        self.path = []
        self.turn_flag = 0
        self.last_flag = 0
        self.turning = -1
        self.dAngle = 0
        self.desti_angle = 0
        self.count = 0
        self.dCharge = 0
        self.interrupt = 0


    def __lt__(self, other):
        return self.NUM < other.NUM

    def emergency(self, cmd):
        if cmd == 0:
            self.interrupt = 0
        elif cmd == 1:
            self.interrupt = 1

    def command(self, path, cmd, node_list, loadable_port_list, unloadable_port_list):
        if self.cmd == 25:
            self.path += path
        else:
            self.path = path

        self.cmd = cmd
        self.desti_node = self.path[-1]
        self.status = 20
        self.count = 0

        # if cmd == 21 or cmd == 22:
        #     desti_node_instance = node_list[self.desti_node -1]
        #     if desti_node_instance in loadable_port_list:
        #         loadable_port_list.remove(desti_node_instance)
        #     elif desti_node_instance in unloadable_port_list:
        #         unloadable_port_list.remove(desti_node_instance)


    def move(self, node_list):
        print("move!")
        # 0. 후진 여부 확인
        if self.path[0] < 0:
            self.path[0] *= -1
            self.back = True

        # 1. 다음 목표 node가 정지하는 node인가
        next_node = node_list[self.path[0] - 1].getPos()
        dx = next_node[0] - self.x
        dy = next_node[1] - self.y
        print("cur next: ",self.node, self.path[0])
        print("dx, dy: ", dx, dy)
        if self.turn_flag == 1 or self.last_flag == 1:
            pass
        elif len(self.path) == 1:
            # next node가 마지막 목표라면 멈춤
            self.last_flag = 1
        else:
            # 회전하는 노드라면 멈춤
            if self.path[1] > 0:
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
        if self.turn_flag == 1 or self.last_flag == 1 or self.back:
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

        # 4. x, y 좌표 갱신
        print("angle: ", self.angle)
        print("velocity:", self.velocity)
        sin_dx = sin(radians(self.angle))
        cos_dy = cos(radians(self.angle))
        if abs(sin_dx) < 0.1: sin_dx = 0
        if abs(cos_dy) < 0.1: cos_dy = 0
        if self.back == False:
            self.x += self.velocity * sin_dx
            self.y -= self.velocity * cos_dy
        else:
            self.x -= self.velocity * sin_dx
            self.y += self.velocity * cos_dy
        print("sin,cos: ", sin_dx, cos_dy)
        print("x,y: ",self.x,self.y)

        # 5. node 근접시 도착한 것으로 보정
        if distance <= 400:
            # 전 node가 wait point였다면 비워주기
            if hasattr(node_list[self.node - 1], 'using'):
                node_list[self.node - 1].using = 0

            self.x = next_node[0]
            self.y = next_node[1]
            self.node = self.path[0]
            self.back = False
            # 6. 필요시 회전
            if self.turn_flag == 1:
                self.turning = 0
            else:
                self.path.pop(0)
                self.last_flag = 0

    def turn(self, node_list):
        self.velocity = 0
        print("turn!")
        # 1. 회전 방향 결정
        if self.turning == 0:
            next_node = node_list[self.path[0] - 1].getPos()
            nextnext_node = node_list[self.path[1] - 1].getPos()
            dx1 = nextnext_node[0] - next_node[0]
            dy1 = nextnext_node[1] - next_node[1]
            if self.angle == 0:
                old_angle = 360
            else:
                old_angle = self.angle
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
        if abs(self.angle - self.desti_angle) < self.ROTATE_SPEED:
            self.angle = self.desti_angle
            self.turn_flag = 0
            self.turning = -1
            self.path.pop(0)

    def brake(self):
        if self.velocity > 0:
            self.velocity -= self.ACCEL
            if self.velocity < 0:
                self.velocity = 0

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
        distance = sqrt((self.x - car.x)**2 + (self.y - car.y)**2)
        if distance <= self.DIAGONAL/2 + car.DIAGONAL/2:
            return True
        else:
            return False

    def isusable(self):
        if self.status == 10:
            return True
        elif self.status == 81:
            return True
        elif self.cmd == 20 and self.count <= 5:
            return True
        else:
            return False

    def get_angle(self, dx, dy):
        radian = atan2(dx, -dy)
        degree = degrees(radian)
        if degree < 0:
            degree += 360
        return degree

    def vehicle_routine(self, node_list, simul_db):
        result = 0
        # 1. 충돌 방지 명령
        if self.interrupt == 1:
            self.brake()

        # 2. 작업 - status 업데이트
        else:
            # path 이동
            print("cmd start!: ", self.NUM)
            if len(self.path) != 0:
                if self.turning == -1:
                    self.move(node_list)
                else:
                    self.turn(node_list)
            # 이동 완료시 작업 수행
            else:
                # status와 현재 받은 cmd를 분리
                # load
                if self.cmd == 21:
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
                elif self.cmd == 22:
                    if self.status != 40:
                        self.status = 40
                        node_list[self.desti_node - 1].status = -1
                    self.count += 1
                    if self.count >= self.LOAD_SPEED:
                        self.count = 0
                        self.cmd = 10
                        self.status = 10
                        self.loaded = 0
                        node_list[self.desti_node - 1].status = 0
                        result = 1
                    print("unload! - ", self.count)
                # wait
                elif self.cmd == 20:
                    self.cmd = 10
                    self.status = 10
                    node_list[self.node-1].using = self.NUM
                    print("wait!")
                # charge
                elif self.cmd == 23:
                    self.cmd = 10
                    self.status = 80
                    print("charge!")
                # append
                elif self.cmd == 25:
                    self.status = 11
                    print("append!")

            # wait to move 명령이면 5초 카운트
            if self.cmd == 20:
                self.count += 1

        # 3. 배터리 충/방전
        if self.status in [10, 11]:
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
        print("=====================")

        # 4. DB에 저장
        # 상위 경로에서 처리

        return result
