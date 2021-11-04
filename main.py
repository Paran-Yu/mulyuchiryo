import mapreader
from simulator import simulator

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

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

img, map_data = mapreader.read_layout()
port_list, wait_list, node_list, path_list, vehicle_list = mapreader.read_component()

# simulate 시작하면 simulator 함수 시작하도록
simulator.simulate(simulate_speed, port_list, wait_list, vehicle_list)

# 1920x1080, example.xml scale=1로 조정하고 했습니다.
print(img, map_data)

# 어디에서든 imread해도 값은 똑같은 것 같다.
# img = mpimg.imread('./example.png')
# print('mpimg:',img)
img = plt.imread('./example.png')
print('plt:',img)
# print(img[739][1455]) # png는 [R, G, B, A]이며 각 값은 [0, 1], jpg는 [R, G, B]이며 각 값은 [0,255]
# img.resize((1080, 1920))

# for node in node_list:
#     print(node.X, node.Y)
imgplot = plt.imshow(img)
plt.plot([node.X for node in node_list],[node.Y for node in node_list], 'ro')
plt.show()

# 위에 뜬 창을 없애야만 아래가 실행된다. 업데이트 하는 방법을 찾아보기
# img[739][1455] = [0,0,0,0]
# imgplot = plt.imshow(img)
# plt.show()


# 이미지 크기 자체를 늘려봤지만 19200x10800은 3MB짜리 이미지가 나온다. 19만은 상상도 안 된다.
# https://ponyozzang.tistory.com/600
# from PIL import Image

# img = Image.open('./example.png')
# img_resize = img.resize((19200, 10800), Image.LANCZOS)  # resizes image in-place
# img_resize.save('img_resize.png')
# imgplot = plt.imshow(img)
# plt.show()