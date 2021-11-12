from xml.etree import ElementTree
from res import vehicle, node

tree = ElementTree.parse('data.xml')
root = tree.getroot()

image = root.find("img")
mapdata = root.find("map")
ports = root.find("ports")
waits = root.find("waits")
vehicles = root.find("vehicles")
nodes = root.find("nodes")
paths = root.find("paths")


# declare lists
port_list = []
wait_list = []
node_list = []
path_list = []
vehicle_list = []

# read image data
img_path = image.find("img_path").text
img_name = image.find("name").text
img = {'path': img_path, 'name': img_name}


# read map size, scale and capa
map_width = int(mapdata.find("width").text)
map_scale = float(mapdata.find("scale").text)
map_capa = int(mapdata.find("capa").text)
map_data = {'width': map_width, 'scale': map_scale, 'capacity': map_capa}


# read_ports
xml_port_list = ports.findall("port")
for x in xml_port_list:
    name = x.find("name").text
    num = int(x.find("num").text)
    x_input = float(x.find("x").text) * map_scale
    y_input = float(x.find("y").text) * map_scale
    a = node.Port(num, x_input, y_input, name)
    a.TYPE = x.find("type").text
    a.FREQ = int(x.find("freq").text)
    a.V_TYPE = x.find("v_type").text
    if a.TYPE == "load":
        unload = x.find("unload")
        unload_list = unload.findall("item")
        for y in unload_list:
            a.UNLOAD_LIST.append(int(y.text))
    port_list.append(a)
    node_list.append(a)


# read_waits
xml_wait_list = waits.findall("wait")
for x in xml_wait_list:
    name = x.find("name").text
    num = int(x.find("num").text)
    x_input = float(x.find("x").text) * map_scale
    y_input = float(x.find("y").text) * map_scale
    a = node.WaitPoint(num, x_input, y_input, name)
    if x.find("charge").text == "Y":
        a.CHARGE = True
    wait_list.append(a)
    node_list.append(a)


# read nodes
xml_node_list = nodes.findall("node")
for x in xml_node_list:
    a = node.Node(int(x.find("num").text), int(x.find("x").text) * map_scale, int(x.find("y").text) * map_scale)
    if x.find("isCross").text == "Y":
        a.isCross = True
    node_list.append(a)
node_list = sorted(node_list)

path_linked_list = [[] for _ in range(len(node_list)+1)]

# read paths
xml_path_list = paths.findall("path")
# 노드 사이의 연결 관계를 linked list로 표현
for x in xml_path_list:
    from_node, to_node = int(x.find("start").text), int(x.find("end").text)
    path_list.append((from_node, to_node))

    # cost 구하기
    # 시간으로 구하고 싶어서 노드 사이의 거리를 40으로 나눠준 값을 일단 쓰겠습니다.
    # 세로로 연결된 노드라면
    if node_list[from_node-1].X == node_list[to_node-1].X:
        cost = (abs(node_list[from_node-1].Y - node_list[to_node-1].Y)) / 40
    # 가로로 연결된 노드라면
    else:
        cost = (abs(node_list[from_node-1].X - node_list[to_node-1].X)) / 40
    path_linked_list[from_node].append((to_node, cost))
    path_linked_list[to_node].append((from_node, cost))

# read vehicles
xml_vehicle_list = vehicles.findall("vehicle")
for x in xml_vehicle_list:
    a = vehicle.Vehicle(x.find("name").text)
    a.NUM = int(x.find("num").text)
    a.TYPE = x.find("type").text
    a.WIDTH = int(x.find("width").text)
    a.HEIGHT = int(x.find("height").text)
    a.DIAGONAL = int(x.find("diagonal").text)
    a.ROTATE_SPEED = float(x.find("rotate_speed").text)
    a.ACCEL = float(x.find("accel").text) * 1000                # m/sec^2 -> mm/sec^2
    a.MAX_SPEED = float(x.find("max_speed").text) * 100 / 6     # m/min -> mm/sec
    a.LU_TYPE = x.find("lu_type").text
    a.LOAD_SPEED = int(x.find("load_speed").text)
    a.CHARGE_SPEED = float(x.find("charge_speed").text) / 60    # %/min -> %/sec
    a.DISCHARGE_WAIT = float(x.find("discharge_wait").text) / 60    # %/min -> %/sec
    a.DISCHARGE_WORK = float(x.find("discharge_work").text) / 60    # %/min -> %/sec
    a.node = int(x.find("start_node").text)
    a.ROTATE_TH = a.ROTATE_SPEED
    start_node = [node for node in node_list if node.NUM == a.node][0]
    a.x = start_node.X
    a.y = start_node.Y
    a.velocity = 0
    a.angle = int(x.find("start_angle").text)
    a.battery = 100
    vehicle_list.append(a)
vehicle_list = sorted(vehicle_list)

def read_layout():
    return img, map_data

def read_component():
    return port_list, wait_list, node_list, path_list, vehicle_list, path_linked_list
