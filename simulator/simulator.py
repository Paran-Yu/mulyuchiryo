import random

# simulate 초기화
def simulate_init(simulate_speed, port_list, wait_list, vehicle_list):
    port_init(port_list)
    pass

# PORT
# port의 time cnt를 0~FREQ 사이의 랜덤값으로 지정
def port_init(port_list):
    for x in port_list:
        cnt = random.randrange(0, x.FREQ+1)
        x.count = cnt

def port_update(port_list):
    for x in port_list:
        # LOAD: 반송물이 사라져야 카운트 시작
        # UNLOAD: 반송물을 받은 후에야 count가 reset 된다.
        if x.status == 0:
            x.count += 1
            if x.count == x.FREQ:
                x.status = 1
                x.count = 0

# WAIT POINT

# VEHICLE