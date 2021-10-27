from math import atan2, pi, degrees

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
        self.STAT_LIST = {}

        self.x = -1
        self.y = -1
        self.node = -1
        self.next_node = -1
        self.velocity = -1
        self.angle = -1
        self.status = 0
        self.loaded = 0
        self.battery = -1
        self.path = []
        self.command_list = []

    # new_node로 이동
    def move(self, new_node):
        pass

    def load(self, port_num):
        pass

    def unload(self, port_num):
        pass

    def getNode(self):
        pass

    def getPos(self):
        return (self.x, self.y)

    def getDesti(self):
        pass

    def getBattery(self):
        return self.battery

    def getStatus(self):
        return self.status
    
    def getBrakeDis(self):
        return (self.velocity**2)/(2*self.ACCEL)

    def checkCrash(self, car):
        # 다른 차량타입이라 크기 다르면? 둘다 메서드 들어가니까 ㄱㅊ
        # 라운드턴 등으로 직각이 아닐 때는? 1) (언제나)여유롭게 대각선으로 2) 매0.1초마다 영역 계산
        if (self.x + self.width > car.x) and (self.x < car.x + car.width) and (self.y > car.y + car.height) and (self.y + self.height > car.y):
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

    # 매 0.1초마다 실행
    def threadFunc(self):
        while True:
            # 충돌여부 조사 (다른 차량 정보 모두 필요)
            for i in range(len(cars)):
                crashed = self.checkCrash(cars[i])
                if crashed:
                    self.status = 4
                    return -1   # 종료..?
            # 현재 상태를 파악
            # 대기
            if self.status == 0:
                # Core에서 명령 있는지 확인
                # 대기 카운트 += 0.1초
                # 대기 카운트 >= 5: 복귀 명령은 Core에서 해주는걸로?
                # 대기 배터리 방전
                self.battery -= self.DISCHARGE_WAIT/60/10   # 분->초->0.1초
            # 반송 중
            elif self.status == 1:
                # 더 이상 목적지가 추가적으로 없다면 최종 목적지이므로 상하차
                if self.path.length == 0:
                    # LOAD/UNLOAD
                    if self.loaded:
                        sleep(30)   # 그냥 30초 쉴지, count 방식으로 쉴지
                        self.loaded = not self.loaded
                    else:
                        sleep(30)
                        self.loaded = not self.loaded
                # 더 목적지가 있다면
                else:
                    current_destination = self.path.pop(0)
                # 회전 & 가감속
                angle_diff = self.angleBetweenVector(self.getDesti(current_destination)) - self.angle # 위치벡터-위치벡터는 스칼라 각도
                if angle_diff==0:   # 현재 목적지를 향해 보고 있다
                    distance = self.getDesti() - self.getPosition() # 현재 목적지와의 거리
                    if distance <= self.getBrakeDis():  # 지금부터 브레이크를 밟아야 현재 목적지에서 정
                        self.velocity -= self.ACCEL
                    else:
                        self.velocity += self.ACCEL
                        if self.velocity > self.MAX_SPEED:
                            self.velocity = self.MAX_SPEED
                    # 속도는 현재 위치에 영향을 준다 (벡터값으로 바꿔야할듯)
                    self.x += self.velocity
                    self.y += self.velocity
                else:   # 현재 목적지를 보고 있지 않다면, 회전을 해야겠지
                    # 각도 차이에 따라 더할지 뺄지 로직 필요
                    self.angle += (self.ROTATE_SPEED)/10    # 초->01.초
                # 동작 배터리 방전
                self.battery += self.CHARGE_SPEED/60/10   # 분->초->0.1초
                # 충돌시 에러
                # 반송 완료 후 충전 요건 충족시
            # 복귀
            elif self.status == 2:
                # 복귀 (어...? 사실상 반송이랑 똑같은데?)
                # 새로운 명령 확인
                # 동작 배터리 방전
                self.battery -= self.DISCHARGE_WORK/60/10   # 분->초->0.1초
            # 충전
            elif self.status == 3:
                # 배터리 충전 완료시 / 업무 할당 가능시
                # 새로운 명령 확인?
                # 배터리 충전
                self.battery += self.CHARGE_SPEED/60/10   # 분->초->0.1초
            # 에러
            elif self.status == 4:
                pass

# 방위각 테스팅
d = Vehicle('d')
d.x = -1
d.y = 1
v = Vehicle('v')
print(d.getAngle(v))
