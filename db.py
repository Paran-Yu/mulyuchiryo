import sqlite3


class DB:
    def __init__(self):
        try:
            self.db = sqlite3.connect("simul_data.db")
        except:
            print("DB Connection failed")
            exit(1)

    def db_init(self):
        cur = self.db.cursor()

        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='scene'")
        returns = cur.fetchall()
        if len(returns) == 0:
            cur.execute('CREATE TABLE scene(\
            id INTEGER PRIMARY KEY AUTOINCREMENT)')

        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='vehicle'")
        returns = cur.fetchall()
        if len(returns) == 0:
            cur.execute('CREATE TABLE vehicle(\
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
            cur.execute('CREATE TABLE command(\
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


    def db_clear(self):
        cur = self.db.cursor()
        cur.execute("DROP table scene")
        cur.execute("DROP table vehicle")
        cur.execute("DROP table command")

    def get_vehicle_work(self):
        pass

    def get_vehicle_charge(self):
        pass

    def get_total_work(self):
        pass

    def get_node_freq(self):
        pass

