import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

vehicle_rects = []
vehicle_texts = []
vehicle_arrows = []
vehicle_desti_arrows = []


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


# simulate 초기화
def simulate_init(node_list, port_list, wait_list, vehicle_list, path_list):
    port_init(port_list)
    wait_init(wait_list, vehicle_list)
    plot_init(node_list, path_list, vehicle_list)


# simulate_speed초 마다 한번씩 호출된다.
def simulate_routine(node_list, port_list, wait_list, vehicle_list, loadable_port_list, unloadable_port_list):
    print("routine start")
    port_update(port_list, loadable_port_list, unloadable_port_list)
    vehicle_update(node_list, vehicle_list)


# PORT
# port의 time cnt를 0~FREQ 사이의 랜덤값으로 지정
def port_init(port_list):
    for x in port_list:
        cnt = random.randrange(0, x.FREQ+1)
        x.count = cnt


def port_update(port_list, loadable_port_list, unloadable_port_list):
    for x in port_list:
        # LOAD: 반송물이 사라져야 카운트 시작
        # UNLOAD: 반송물을 받은 후에야 count가 reset 된다.
        if x.status == 0:
            x.count += 1
            if x.count == x.FREQ:
                x.status = 1
                if x.TYPE == "load":
                    loadable_port_list.append(x)
                elif x.TYPE == "unload":
                    unloadable_port_list.append(x)
                x.count = 0


# WAIT POINT
def wait_init(wait_list, vehicle_list):
    for x in vehicle_list:
        used_wait = [wait for wait in wait_list if wait.NUM == x.node][0]
        used_wait.using = True


# VEHICLE
def vehicle_update(node_list, vehicle_list):
    for vehicle in vehicle_list:
        vehicle.vehicle_routine(node_list)
        # TODO: DB에 기록


# PLOT
def plot_init(node_list, path_list, vehicle_list):
    img = plt.imread('./example.png')
    imgplot = plt.imshow(img)
    # 노드
    # fig = plt.plot([node.X for node in node_list],[node.Y for node in node_list], 'ro')
    for node in node_list:
        plt.plot(node.X, node.Y, 'ro')
        plt.text(node.X, node.Y, f'{node.NUM}', fontsize=8)
    # 도로
    # path_list에는 x,y 값이 없고 노드 번호만 있다. 직접 계산해줘야한다.
    for path in path_list:
        start = node_list[path[0] - 1]
        end = node_list[path[1] - 1]
        # 수직인지 수평인지 판별 필요
        if start.X == end.X:  # X축 동일 -> 수직
            plt.vlines(x=start.X, ymin=start.Y, ymax=end.Y)
        else:  # Y축 동일 -> 수평
            plt.hlines(y=start.Y, xmin=start.X, xmax=end.X)

    ax = plt.gca()
    plt.pause(1)

    for vehicle in vehicle_list:
        # print(vehicle.x, vehicle.y)
        vehicle_rect = RotatingRectangle(
            [vehicle.x, vehicle.y],
            vehicle.WIDTH,
            vehicle.HEIGHT,
            angle=vehicle.angle,
            fill=True,
            edgecolor='blue',
            facecolor='purple',
            rel_point_of_rot=[vehicle.WIDTH / 2, vehicle.HEIGHT / 2]
        )
        vehicle_arrow = patches.FancyArrowPatch(
            (vehicle.x, vehicle.y),
            (vehicle.x, vehicle.y - vehicle.HEIGHT),
            mutation_scale=15
        )
        vehicle_desti_arrow = patches.FancyArrowPatch(
            (vehicle.x, vehicle.y),
            (vehicle.x, vehicle.y),
            mutation_scale=5
        )
        ax.add_patch(vehicle_rect)
        ax.add_patch(vehicle_arrow)
        ax.add_patch(vehicle_desti_arrow)
        vehicle_rects.append(vehicle_rect)
        vehicle_texts.append(plt.text(vehicle.x, vehicle.y, vehicle.NAME))
        vehicle_arrows.append(vehicle_arrow)
        vehicle_desti_arrows.append(vehicle_desti_arrow)

    plt.pause(1)


def plot_update(simulate_speed, node_list, vehicle_list):
    def AngleToMfc(degree):
        return (degree+270)%360

    #  전에 있던 것 업데이트 해주기
    for i in range(len(vehicle_rects)):
        print(vehicle_list, vehicle_rects, vehicle_texts, vehicle_arrows, vehicle_desti_arrows)
        vehicle_rects[i].set_xy_center((vehicle_list[i].x, vehicle_list[i].y))
        vehicle_rects[i].set_angle(vehicle_list[i].angle)
        vehicle_texts[i].set_position((vehicle_list[i].x, vehicle_list[i].y))
        vehicle_texts[i].set_text((vehicle_list[i].velocity, vehicle_list[i].angle))
        front_x = vehicle_list[i].x + vehicle_list[i].HEIGHT * np.cos(np.pi/180*AngleToMfc(vehicle_list[i].angle))
        front_y = vehicle_list[i].y + vehicle_list[i].HEIGHT * np.sin(np.pi/180*AngleToMfc(vehicle_list[i].angle))
        vehicle_arrows[i].set_positions((vehicle_list[i].x, vehicle_list[i].y), (front_x, front_y))
        if len(vehicle_list[i].path) == 0:
            vehicle_desti_arrows[i].set_positions((vehicle_list[i].x, vehicle_list[i].y), (vehicle_list[i].x, vehicle_list[i].y))
        else:
            desti_node = node_list[vehicle_list[i].path[-1] -1]
            vehicle_desti_arrows[i].set_positions((vehicle_list[i].x, vehicle_list[i].y), (desti_node.X, desti_node.Y))
    plt.pause(simulate_speed)
