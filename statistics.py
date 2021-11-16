from db import DB
import numpy as np
import matplotlib.pyplot as plt

db = DB()
db.db_init()


def vehicle_work():
    # wait charge move load unload
    label, work_list = db.get_vehicle_work()
    # work_list = [[10,20,30],[20,10,40],[50,30,20],[30,40,10],[10,20,20]]
    # label = ['V1', 'V2', 'V3']
    width = 0.3

    fig, ax = plt.subplots()
    ax.bar(label, work_list[0], width, label="Wait")
    ax.bar(label, work_list[1], width, label="Charge", bottom=np.array(work_list[0]))
    ax.bar(label, work_list[2], width, label="Move", bottom=np.array(work_list[0])+np.array(work_list[1]))
    ax.bar(label, work_list[3], width, label="Load", bottom=np.array(work_list[0])+np.array(work_list[1])+np.array(work_list[2]))
    ax.bar(label, work_list[4], width, label="Unload", bottom=np.array(work_list[0])+np.array(work_list[1])+np.array(work_list[2])+np.array(work_list[3]))

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
