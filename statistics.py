from db import DB
import numpy as np
import matplotlib.pyplot as plt

db = DB()
db.db_init()


def vehicle_work():
    # wait charge move load unload
    name_list, work_list = db.get_vehicle_work()
    # work_list = [[10,20,30],[20,10,40],[50,30,20],[30,40,10],[10,20,20]]
    # label = ['V1', 'V2', 'V3']
    width = 0.3

    fig, ax = plt.subplots()
    ax.bar(name_list, work_list[0], width, label="Wait")
    ax.bar(name_list, work_list[1], width, label="Charge", bottom=np.array(work_list[0]))
    ax.bar(name_list, work_list[2], width, label="Move", bottom=np.array(work_list[0])+np.array(work_list[1]))
    ax.bar(name_list, work_list[3], width, label="Load", bottom=np.array(work_list[0])+np.array(work_list[1])+np.array(work_list[2]))
    ax.bar(name_list, work_list[4], width, label="Unload", bottom=np.array(work_list[0])+np.array(work_list[1])+np.array(work_list[2])+np.array(work_list[3]))

    ax.set_ylabel('Time[sec]')
    ax.legend()

    plt.show()


def vehicle_charge():
    data = db.get_vehicle_charge()

    dt = 1
    t = np.arange(0, len(data[0][1]), dt)

    # TODO
    # 시간 간격 dt 조정 기능 - UI와 협의

    fig, ax = plt.subplots()
    for x in data:
        ax.plot(t, x[1], label=x[0])

    ax.set_xlabel('Time[sec]')
    ax.set_ylabel('Battery[%]')
    ax.grid(True)
    plt.legend()
    plt.show()

def vehicle_cmd():
    # wait charge move load append
    name_list, work_list = db.get_vehicle_cmd()
    width = 0.3

    fig, ax = plt.subplots()
    ax.bar(name_list, work_list[0], width, label="Wait")
    ax.bar(name_list, work_list[1], width, label="Charge", bottom=np.array(work_list[0]))
    ax.bar(name_list, work_list[2], width, label="Load", bottom=np.array(work_list[0])+np.array(work_list[1]))
    ax.bar(name_list, work_list[3], width, label="Unload", bottom=np.array(work_list[0])+np.array(work_list[1])+np.array(work_list[2]))
    ax.bar(name_list, work_list[4], width, label="Append", bottom=np.array(work_list[0])+np.array(work_list[1])+np.array(work_list[2])+np.array(work_list[3]))

    ax.set_ylabel('Time[sec]')
    ax.legend()

    plt.show()

def work_progress():
    data = db.get_progress()

    dt = 1
    t = np.arange(0, len(data), dt)

    fig, ax = plt.subplots()
    ax.plot(t, data)

    ax.set_xlabel('Time[sec]')
    ax.set_ylabel('Progress[num]')
    ax.grid(True)
    plt.show()


def node_frequency(node_list, path_list):
    data = db.get_node_freq(len(node_list))
    # 노드 갯수만큼 [방문횟수, 방문횟수, ...]
    # map plot 부분 추가

    fig, ax = plt.subplots()
    ax.invert_yaxis()
    for i in range(len(node_list)):
        plt.plot(node_list[i].X, node_list[i].Y, 'o', markersize=data[i])
        plt.text(node_list[i].X, node_list[i].Y, f'{node_list[i].NUM}', 
            horizontalalignment='right',
            verticalalignment='top',
            fontsize=8,
        )
    # path_list에는 x,y 값이 없고 노드 번호만 있다. 직접 계산해줘야한다.
    for path in path_list:
        start = node_list[path[0] - 1]
        end = node_list[path[1] - 1]
        # 수직인지 수평인지 판별 필요
        if start.X == end.X:  # X축 동일 -> 수직
            plt.vlines(x=start.X, ymin=start.Y, ymax=end.Y)
        else:  # Y축 동일 -> 수평
            plt.hlines(y=start.Y, xmin=start.X, xmax=end.X)

    plt.show()