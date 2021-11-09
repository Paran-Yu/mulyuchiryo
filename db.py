import sqlite3

conn = sqlite3.connect("simul_data.db")


def db_init():
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='scene'")
    returns = cur.fetchall()
    if len(returns) == 0:
        conn.execute('CREATE TABLE scene(\
        id INTEGER PRIMARY KEY AUTOINCREMENT)')

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='vehicle'")
    returns = cur.fetchall()
    if len(returns) == 0:
        conn.execute('CREATE TABLE vehicle(\
        id INTEGER PRIMARY KEY AUTOINCREMENT,\
        scene_id INTEGER,\
        time INTEGER,\
        name TEXT,\
        start_node INTEGER,\
        desti_node INTEGER,\
        cur_node INTEGER,\
        x REAL,\
        y REAL,\
        status INTEGER,\
        velocity REAL,\
        angle REAL,\
        battery REAL,\
        loaded INTEGER,\
        FOREIGN KEY(scene_id) REFERENCES scene(id)\
        )')

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='command'")
    returns = cur.fetchall()
    if len(returns) == 0:
        conn.execute('CREATE TABLE command(\
        id INTEGER PRIMARY KEY AUTOINCREMENT,\
        scene_id INTEGER,\
        vehicle_id INTEGER,\
        start_node INTEGER,\
        desti_node INTEGER,\
        path TEXT,\
        type INTEGER,\
        created_at TEXT,\
        is_checked INTEGER,\
        FOREIGN KEY(scene_id) REFERENCES scene(id)\
        FOREIGN KEY(vehicle_id) REFERENCES vehicle(id)\
        )')

    conn.commit()


conn.close()



