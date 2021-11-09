import time
import threading
import mapreader
from simulator import simulator

import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.transforms import Affine2D
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


# 1920x1080, example.xml scale=1로 조정하고 했습니다.
print(img, map_data, vehicle_list)

# 어디에서든 imread해도 값은 똑같은 것 같다.
# img = mpimg.imread('./example.png')
# print('mpimg:',img)
img = plt.imread('./example.png')
# print('plt:',img)
imgplot = plt.imshow(img)

# print(img[739][1455]) # png는 [R, G, B, A]이며 각 값은 [0, 1], jpg는 [R, G, B]이며 각 값은 [0,255]
# img.resize((1080, 1920))


# 노드
# fig = plt.plot([node.X for node in node_list],[node.Y for node in node_list], 'ro')
for node in node_list:
    plt.plot(node.X, node.Y, 'ro')
    plt.text(node.X, node.Y, node.NUM, fontsize=8)
# plt.text([node.X for node in node_list],[node.Y for node in node_list], str([node.NUM for node in node_list][0]))
# 도로
# path_list에는 x,y 값이 없고 노드 번호만 있다. 직접 계산해줘야한다.
for path in path_list:
    # 시작점 start
    start = [node for node in node_list if node.NUM == path[0]][0]
    # 끝점 end
    end = [node for node in node_list if node.NUM == path[1]][0]
    # print(start, end)
    # 수직인지 수평인지 판별 필요
    if start.X == end.X:    # X축 동일 -> 수직
        plt.vlines(x=start.X, ymin=start.Y, ymax=end.Y)
    else:                   # Y축 동일 -> 수평
        plt.hlines(y=start.Y, xmin=start.X, xmax=end.X)

# plt.show()
# plt.plot()
# plt.draw()
# fig = plt.figure()

ax = plt.gca()
plt.pause(1)

# 여기서부터는 병렬처리 쓰레드의 적용을 받아야할 것 같다.


# 기존 Rectangle은 회전시 중심 기준이 아니라서 어려움, https://stackoverflow.com/questions/60413174/rotating-rectangles-around-point-with-matplotlib
class RotatingRectangle(patches.Rectangle):
    def __init__(self, xy, width, height, rel_point_of_rot, **kwargs):
        super().__init__(xy, width, height, **kwargs)
        self.rel_point_of_rot = rel_point_of_rot
        self.xy_center = self.get_xy()
        self.set_angle(self.angle)

    def _apply_rotation(self):
        angle_rad = self.angle * np.pi / 180
        m_trans = np.array([[np.cos(angle_rad), -np.sin(angle_rad)],
                            [np.sin(angle_rad), np.cos(angle_rad)]])
        shift = -m_trans @ self.rel_point_of_rot
        self.set_xy(self.xy_center + shift)

    def set_angle(self, angle):
        self.angle = angle
        self._apply_rotation()

    def set_rel_point_of_rot(self, rel_point_of_rot):
        self.rel_point_of_rot = rel_point_of_rot
        self._apply_rotation()

    def set_xy_center(self, xy):
        self.xy_center = xy
        self._apply_rotation()

vehicle_rects = []
vehicle_texts = []
# 차량
for vehicle in vehicle_list:
    # print(vehicle.x, vehicle.y)
    vehicle_rect = RotatingRectangle(
        [vehicle.x, vehicle.y],
        vehicle.WIDTH,
        vehicle.HEIGHT,
        angle=vehicle.angle,   # anti-clockwise angle
        fill=True,
        edgecolor = 'blue',
        facecolor = 'purple',
        rel_point_of_rot = [vehicle.WIDTH/2, vehicle.HEIGHT/2]
    )
    # print(vehicle_rect.xy)
    ax.add_patch(vehicle_rect)
    vehicle_rects.append(vehicle_rect)
    vehicle_texts.append(plt.text(vehicle.x, vehicle.y, vehicle.NAME))
    pass

# print(vehicle_rects)
plt.pause(1)

while True:

    # 이동 명령
    for vehicle in vehicle_list:
        print(vehicle)
        vehicle.command([26], 20)
        vehicle.move(node_list)
        print(vehicle.path, vehicle.status)
        # break


    # 이동했다 치고 다시 보여주려면
    # # 1) 전에 있던 걸 지우고 새로 그리기(지우는 방법을 모르겠음)
    # for vehicle in vehicle_list:
    #     vehicle.x, vehicle.y = vehicle.y, vehicle.x
    #     # print(vehicle.x, vehicle.y)
    #     vehicle_rect = RotatingRectangle(
    #         [vehicle.x, vehicle.y],
    #         vehicle.WIDTH,
    #         vehicle.HEIGHT,
    #         angle=vehicle.angle,
    #         fill=True,
    #         edgecolor = 'blue',
    #         facecolor = 'purple',
    #         rel_point_of_rot = [vehicle.WIDTH/2, vehicle.HEIGHT/2]
    #     )
    #     ax.add_patch(vehicle_rect)
    #     pass


    # 2) 전에 있던 것 업데이트 해주기
    for i in range(len(vehicle_rects)):
        print(vehicle_rects[i])
        print(vehicle_list[i], vehicle_list[i].getPos())
        vehicle_rects[i].set_xy_center((vehicle_list[i].x, vehicle_list[i].y))
        vehicle_rects[i].set_angle(vehicle_list[i].angle)
        vehicle_texts[i].set_position((vehicle_list[i].x, vehicle_list[i].y))
        print(vehicle_rects[i])

    plt.pause(1)
    # break



# 이미지 크기 자체를 늘려봤지만 19200x10800은 3MB짜리 이미지가 나온다. 19만은 상상도 안 된다.
# https://ponyozzang.tistory.com/600
# from PIL import Image

# img = Image.open('./example.png')
# img_resize = img.resize((19200, 10800), Image.LANCZOS)  # resizes image in-place
# img_resize.save('img_resize.png')
# imgplot = plt.imshow(img)
# plt.show()
