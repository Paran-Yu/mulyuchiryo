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

img, mapdata = mapreader.read_layout()
port_list, wait_list, node_list, path_list, vehicle_list = mapreader.read_component()

# simulate 시작하면 simulator 함수 시작하도록
simulator.simulate(simulate_speed, port_list, wait_list, vehicle_list)