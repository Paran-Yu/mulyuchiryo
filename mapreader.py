from xml.etree import ElementTree
from res import vehicle

tree = ElementTree.parse('example.xml')
root = tree.getroot()

image = root.find("img")
mapdata = root.find("map")
ports = root.find("ports")
waits = root.find("waits")
vehicles = root.find("vehicles")
nodes = root.find("nodes")
paths = root.find("path")

# read image data
img_path = image.find("img_path").text
img_name = image.find("name").text

# read map size, scale and capa
map_width = int(mapdata.find("width").text)
map_scale = int(mapdata.find("scale").text)
map_capa = int(mapdata.find("capa").text)

# read vehicles
vehicle_list = []
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
    # a.node: 초기 node 위치 필요
    a.velocity = 0
    # a.angle: 초기 각 필요
    a.battery = 100

    vehicle_list.append(a)

