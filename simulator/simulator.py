import random

# main func of simulator
def simulate(simulate_speed, port_list, wait_list, vehicle_list):
    port_init(port_list)
    pass


# port의 time cnt를 0~FREQ 사이의 랜덤값으로 지정
def port_init(port_list):
    # port init
    port_count = []
    for x in port_list:
        cnt = random.randrange(0, x.FREQ+1)
        port_count.append(cnt)