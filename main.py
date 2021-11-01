import mapreader
from simulator import simulator

port_list = []
wait_list = []
node_list = []
path_list = []
vehicle_list = []

img, map = mapreader.read_layout()
port_list, wait_list, node_list, path_list, vehicle_list = mapreader.read_component()

# simulate 시작하면 simulator 함수 시작하도록
simulator(port_list, wait_list, vehicle_list)