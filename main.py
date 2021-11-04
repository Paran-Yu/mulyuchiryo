import time
import threading
import mapreader
from simulator import simulator

# simulate attribute
simulate_speed = 1

# layout component
port_list = []
wait_list = []
node_list = []
path_list = []
vehicle_list = []

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

# map data 읽어오기
img, map_data = mapreader.read_layout()
port_list, wait_list, node_list, path_list, vehicle_list = mapreader.read_component()


# UI에서 simulate 버튼을 누르면 simulate 시작
def start_simulate():
    simulator.simulate(simulate_speed, port_list, wait_list, vehicle_list)
    simulate_routine()

# simulate_speed마다 루틴 실행
def simulate_routine():
    threading.Timer(simulate_speed, simulate_routine()).start()