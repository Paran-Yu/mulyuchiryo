import mapreader
from simulator import simulator
from Core.a_star import a_star, heuristic


# simulate attribute
simulate_speed = 1

# layout component
port_list = []
wait_list = []
node_list = []
path_list = []
vehicle_list = []

# 짐을 내려놓을 수 있는 포트만 모아놓은 리스트 추가
# 반송을 시작하려면 짐을 내려놓을 수 있는 포트가 존재해야 하기 때문에, 체크를 위해서 추가했습니다.
# 짐이 새로 나오면 아래 리스트를 확인하고
# 비어있지 않다면 가장 가까이 있는 AGV에게 job을 할당하여 포트로 불러들입니다.
unloadable_port_list = []

VEHICLE_STATUS = {
    00: "INIT",
    10: "WAITING",
    11: "WAITING&LOADED",
    20: "MOVING TO WAIT",
    21: "MOVING TO UNLOAD",
    22: "MOVING TO LOAD",
    23: "MOVING TO CHARGE",
    30: "LOADING",
    40: "UNLOADING",
    80: "CHARGING",
    81: "CHARGING&LOADED",
    91: "COLLIDED",
    99: "ERROR"
}

img, map_data = mapreader.read_layout()
port_list, wait_list, node_list, path_list, vehicle_list = mapreader.read_component()

# simulate 시작하면 simulator 함수 시작하도록
simulator.simulate(simulate_speed, port_list, wait_list, vehicle_list)

# 출발지와 도착지를 첫 번째, 두 번째 인자로 넣어준다.
a_star(29, 11, path_list, node_list)