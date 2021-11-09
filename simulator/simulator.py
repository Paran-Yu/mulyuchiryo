import random

# simulate 초기화
def simulate_init(port_list, wait_list, vehicle_list):
    port_init(port_list)
    wait_init(wait_list, vehicle_list)

# simulate_speed초 마다 한번씩 호출된다.
def simulate_routine(node_list, port_list, vehicle_list):
    print("routine start")
    port_update(port_list)
    vehicle_update(node_list, vehicle_list)


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
def wait_init(wait_list, vehicle_list):
    for x in vehicle_list:
        used_wait = [wait for wait in wait_list if wait.NUM == x.node][0]
        used_wait.using = True

# VEHICLE
def vehicle_update(node_list, vehicle_list):
    for vehicle in vehicle_list:
        vehicle.vehicle_routine(node_list)
        # TODO: DB에 기록

