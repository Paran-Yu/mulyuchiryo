from xml.etree import ElementTree

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

# read map size, scals and capa
map_width = int(mapdata.find("width").text)
map_scale = int(mapdata.find("scale").text)
map_capa = int(mapdata.find("capa").text)