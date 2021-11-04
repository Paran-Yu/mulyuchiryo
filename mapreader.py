from xml.etree import ElementTree
from res import vehicle, node

tree = ElementTree.parse('example.xml')
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
map_scale = int(mapdata.find("scale").text)
map_capa = int(mapdata.find("capa").text)
map_data = {'width': map_width, 'scale': map_scale, 'capacity': map_capa}


# read_ports
xml_port_list = ports.findall("port")
for x in xml_port_list:
    a = node.Port(x.find("name").text)
    a.NUM = int(x.find("num").text)
    a.X = float(x.find("x").text) * map_scale
    a.Y = float(x.find("y").text) * map_scale
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
    a = node.WaitPoint(x.find("name").text)
    a.NUM = int(x.find("num").text)
    a.X = float(x.find("x").text) * map_scale
    a.Y = float(x.find("y").text) * map_scale
    if x.find("charge").text == "y":
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


# 노드 사이의 연결 관계를 linked list로 표현
# path_list의 index 0은 편의상 사용하지 않고 index 1부터 사용한다.
xml_path_list = paths.findall("path")
path_list = [[] for _ in range(len(node_list)+1)]
for x in xml_path_list:
    from_node, to_node = int(x.find("start").text), int(x.find("end").text)
    path_list[from_node].append(to_node)
    path_list[to_node].append(from_node)

print(path_list)


# read vehicles
xml_vehicle_list = vehicles.findall("vehicle")
for x in xml_vehicle_list:
    a = vehicle.Vehicle(x.find("name").text)
    a.TYPE = x.find("type").text
    a.WIDTH = int(x.find("width").text)
    a.HEIGHT = int(x.find("height").text)
    a.DIAGONAL = int(x.find("diagonal").text)
    a.ROTATE_SPEED = int(x.find("rotate_speed").text)
    a.ACCEL = float(x.find("accel").text)
    a.MAX_SPEED = int(x.find("max_speed").text)
    a.LU_TYPE = x.find("lu_type").text
    a.CHARGE_SPEED = float(x.find("charge_speed").text)
    a.DISCHARGE_WAIT = float(x.find("discharge_wait").text)
    a.DISCHARGE_WORK = float(x.find("discharge_work").text)
    a.node = int(x.find("start_node").text)
    # a.x
    # a.y
    a.velocity = 0
    a.angle = int(x.find("start_angle").text)
    a.battery = 100
    vehicle_list.append(a)

def read_layout():
    return img, map_data

def read_component():
    return port_list, wait_list, node_list, path_list, vehicle_list
