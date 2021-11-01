import mapreader

port_list = []
wait_list = []
node_list = []
path_list = []
vehicle_list = []

img, map = mapreader.read_layout()
port_list, wait_list, node_list, path_list, vehicle_list = mapreader.read_component()
