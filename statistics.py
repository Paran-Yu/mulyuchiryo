from db import DB
import numpy as np
import matplotlib.pyplot as plt

db = DB()
db.db_init()

def vehicle_charge():
    v1 = [100, 80, 60, 40, 20]
    v2 = [50, 70, 90, 70, 50]

    dt = 1
    t = np.arrange(0, len(v1), dt)

    fig, ax = plt.subplots()
    ax.plot(t, v1, t, v2)

vehicle_charge()