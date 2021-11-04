import random

# main func of simulator
def simulate(simulate_speed, port_list, wait_list, vehicle_list):
    port_init(port_list)
    pass


# port의 time cnt를 0~FREQ 사이의 랜덤값으로 지정
def port_init(port_list):
    for x in port_list:
        cnt = random.randrange(0, x.FREQ+1)
        x.count = cnt

def port_update(port_list):
    for x in port_list:
        # LOAD: 반송물이 있어도 생산은 계속된다
        if x.TYPE == "load":
            x.count += 1
            if x.count == x.FREQ:
                x.status = 1
                x.count = 0
        # UNLOAD: 반송물을 받은 후에야 count가 reset 된다.
        elif x.TYPE == "unload":
            if x.status == 0:
                x.count += 1
                if x.count == x.FREQ:
                    x.status = 1
                    x.count = 0

        # TODO
        # 1. load/unload 동작 중에 주기가 다시 오는 경우 어떻게 처리?
