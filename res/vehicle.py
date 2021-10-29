from time import sleep
from math import atan2, degrees, isclose
import matplotlib.pyplot as plt

TIME = 1
class Vehicle:
    def __init__(self, name):
        super().__init__()

        self.time = 1*TIME
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
        self.STAT_LIST = {
            00: "INIT",
            10: "WAITING",
            20: "MOVING",
            30: "LOADING",
            40: "UNLOADING",
            80: "CHARGING",
            91: "COLLIDED",
            99: "ERROR",
        }


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
    def move(self, new_node, path, status):
        if self.status in [00, 10, 20, 22, 80] or self.path.length == 0:    
            self.path = path    
            self.desti_node = new_node  # new_node는 path의 마지막 (path[-1])
            self.status = status    # 충전소로 가서 충전하는건지, 대기하러 가는건지 status 정보 필요
        else:
            # Core에 에러쏴주기: 이미 명령받고 이동(21, 40, 80) 중인 경우
            pass

    def load(self, port_num):
        self.loaded = 1
        # PORT[port_num].LOAD()
        pass

    def unload(self, port_num):
        self.loaded = 0
        # PORT[port_num].UNLOAD()
        pass

    def getNode(self):
        return self.node        # 이동중일때는 경유하게 될 노드, 그렇지 않은 경우 현재 위치의 노드 반환

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
        # 다른 차량타입이라 크기 다르면? 둘다 메서드 들어가니까 ㄱㅊ
        # 라운드턴 등으로 직각이 아닐 때는? 1) (언제나)여유롭게 대각선으로 2) 매0.1초마다 영역 계산 -> 일단 라운드턴 배제하고 진행
        # 가로로 있는지 세로로 있는지에 따라 달라져야할거같은데?
        if self.angle == 0 or self.angle == 180:    #가로
            if (self.x + self.WIDTH > car.x) and (self.x < car.x + car.WIDTH) and (self.y > car.y + car.HEIGHT) and (self.y + self.HEIGHT > car.y):
                return True
            else:
                return False
        elif self.angle == 90 or self.angle == 270: #세로
            if (self.x + self.HEIGHT > car.x) and (self.x < car.x + car.HEIGHT) and (self.y > car.y + car.WIDTH) and (self.y + self.WIDTH > car.y):
                return True
            else:
                return False
        else:   # 그 외
            if (self.x + self.DIAGONAL > car.x) and (self.x < car.x + car.DIAGONAL) and (self.y > car.y + car.DIAGONAL) and (self.y + self.DIAGONAL > car.y):
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

    # 매 1초마다 실행
    def threadFunc(self):
        while True:
            # 충돌여부 조사 (다른 차량 정보 모두 필요) -> 모든 차량 정보일텐데 본인은 어떻게 제외시킬까?
            for i in range(len(CARS_LIST)):
                if self is CARS_LIST[i]: # 이게 될까?
                    continue
                crashed = self.checkCrash(CARS_LIST[i])
                if crashed:
                    self.status = 91
                    return -1   # 종료..?
            # 현재 상태를 파악
            # 초기상태 / 대기
            if self.status == 00 or self.status == 10:
                # Core에서 명령 있는지 확인->명령생기면 self.status바뀌므로 여기서 처리ㄴㄴ
                # 대기 카운트 += 1초
                self.count += 1
                if self.count >= 5:
                    self.count = 0
                    # Core에 알림! 복귀, 충전 명령은 Core에서 해주는걸로?
                    pass
                # 대기 배터리 방전
                self.battery -= self.DISCHARGE_WAIT/60/self.time   # 분->초->배속
            # 반송 중
            elif self.status == 21:
                # 더 이상 목적지가 추가적으로 없다면 최종 목적지이므로 상하차
                if self.path.length == 0:
                    # LOAD/UNLOAD
                    if self.loaded:
                        # 포트가 unload가능한 상태인지 확인
                        pass
                        self.status = 40
                        sleep(30*self.time)   # 그냥 30초 쉴지, count 방식으로 쉴지
                        self.unload()
                        # 대기 상태로 전환
                        self.status = 10
                    else:
                        # 포트가 load가능한 상태인지 확인
                        pass
                        self.status = 30
                        sleep(30*self.time)
                        self.load()
                        # 대기 상태로 전환
                        self.status = 10

                # 현재 경유지에 도착했다면
                elif self.getPos() == NODE_LIST[self.node].getPos():
                    self.node = self.path.pop(0)    # node 갱신, path에서 삭제
                # 목적지가 있다면
                # 회전 & 가감속
                angle_diff = self.getAngle(NODE_LIST[self.node]) - self.angle
                if angle_diff==0:   # 현재 목적지를 향해 보고 있다
                    distance = NODE_LIST[self.node].getPos() - self.getPos() # 현재 목적지와의 거리 # (x, y)
                    # 벡터->스칼라 변환 필요. 같은 방위각이므로 x,y 중 하나는 0일 것임.
                    if isclose(distance[0], 0):
                        distance = distance[1]
                    else:
                        distance = distance[0]
                    pass
                    if distance <= self.getBrakeDis():  # 지금부터 브레이크를 밟아야 현재 목적지에서 정지
                        self.velocity -= self.ACCEL # velocity: m/min, ACCEL: m/min
                    else:
                        self.velocity += self.ACCEL # velocity: m/min, ACCEL: m/min
                        if self.velocity > self.MAX_SPEED:  # 최고속도 제한
                            self.velocity = self.MAX_SPEED
                    # 속도는 현재 위치에 영향을 준다 (벡터값으로 바꾸거나, 각도에 따라 바꿔야할듯)->현재는 직각으로만 움직이므로...
                    if isclose(self.angle, 90):
                        self.x += self.velocity/100*6/self.time # m/min->1000mm/60sec->배속
                    elif isclose(self.angle, 270):
                        self.x -= self.velocity/100*6/self.time # m/min->1000mm/60sec->배속
                    elif isclose(self.angle, 0):
                        self.y += self.velocity/100*6/self.time # m/min->1000mm/60sec->배속
                    elif isclose(self.angle, 180):
                        self.y -= self.velocity/100*6/self.time # m/min->1000mm/60sec->배속

                    # 도착했다는 것은 어떻게 할까? distance, x, y가 정확히 0이 될 일은 거의 없을텐데->일정 threshold 이하면 그 위치로 보정
                    if distance <= 0.000001 and self.velocity <= 0.01:
                        self.x = self.getDesti().x
                        self.y = self.getDesti().y
                        continue

                else:   # 현재 목적지를 보고 있지 않다면, 회전을 해야겠지
                    # 각도 차이에 따라 더할지 뺄지 로직 필요
                    if self.getAngle(self.getDesti()) == 0:
                        if 0 < self.angle <= 180:
                            self.angle -= (self.ROTATE_SPEED)/self.time    # 초->배속
                        elif 180 < self.angle < 360:
                            self.angle += (self.ROTATE_SPEED)/self.time    # 초->배속
                    elif self.getAngle(self.getDesti()) == 90:
                        if 90 < self.angle <= 270:
                            self.angle -= (self.ROTATE_SPEED)/self.time    # 초->배속
                        elif 270 < self.angle or self.angle < 90:
                            self.angle += (self.ROTATE_SPEED)/self.time    # 초->배속
                    elif self.getAngle(self.getDesti()) == 180:
                        if 180 < self.angle < 360:
                            self.angle -= (self.ROTATE_SPEED)/self.time    # 초->배속
                        elif 0 <= self.angle < 180:
                            self.angle += (self.ROTATE_SPEED)/self.time    # 초->배속
                    elif self.getAngle(self.getDesti()) == 270:
                        if 270 < self.angle or self.angle <= 90:
                            self.angle -= (self.ROTATE_SPEED)/self.time    # 초->배속
                        elif 90 < self.angle < 270:
                            self.angle += (self.ROTATE_SPEED)/self.time    # 초->배속
                        
                    # 360도는 0도다
                    if 360 < self.angle:
                        self.angle -= 360
                    elif self.angle < 0:
                        self.angle += 360
                            
                    # 직각이 아닐때는 정확히 계산해줘야한다. 아직 로직 완성 못함
                    # if (angle_diff%360) 
                    # self.angle += (self.ROTATE_SPEED)/self.time    # 초->배속
                    
                # 동작 배터리 방전
                self.battery -= self.DISCHARGE_WORK/60/self.time   # 분->초->배속

            # 충전소로 복귀
            elif self.status == 22:
                # 복귀 (어...? 사실상 반송이랑 똑같은데?)
                # 동작 배터리 방전
                self.battery -= self.DISCHARGE_WORK/60/self.time   # 분->초->배속
            # 충전
            elif self.status == 80:
                # 배터리 충전
                self.battery += self.CHARGE_SPEED/60/self.time   # 분->초->배속
                # 배터리 과충전 불가
                if self.battery > 100:
                    self.battery = 100
                # 충전 완료 됐다고 Core에 알리기
            # 에러
            elif self.status == 91 or self.status == 99:
                pass
            sleep(self.time)


X=[[0]*100 for _ in range(100)]
plt.imshow(X)
v = Vehicle('1번')
v.x = v.y = 50
plt.title("test")
plt.show()