from db import DB
import numpy as np
import matplotlib.pyplot as plt

db = DB()
db.db_init()

def vehicle_charge():
    charge_list = db.get_vehicle_charge()
    # v1 = [100, 80, 60, 40, 20]
    # v2 = [50, 70, 90, 70, 50]

    dt = 1
    t = np.arange(0, len(charge_list[0]['battery']), dt)

    # TODO
    # 시간 간격 dt 조정 기능 - UI와 협의

    fig, ax = plt.subplots()
    for x in charge_list:
        ax.plot(t, charge_list[0]['battery'], label=charge_list[0]['name'])

    ax.set_xlabel('Time[sec]')
    ax.set_ylabel('Battery[%]')
    ax.grid(True)
    plt.legend()
    plt.show()

# vehicle_charge()