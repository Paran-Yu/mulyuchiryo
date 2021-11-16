import sqlite3


class DB:
    def __init__(self):
        try:
            self.conn = sqlite3.connect("simul_data.db")
        except:
            print("DB Connection failed")
            exit(1)

        self.scene_num = -1

        self.db_init()

    def db_init(self):
        cur = self.conn.cursor()

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
        cur = self.conn.cursor()
        cur.execute("DROP table scene")
        cur.execute("DROP table vehicle")
        cur.execute("DROP table command")

    def put_scene_num(self, num):
        cur = self.conn.cursor()
        cur.execute(f'INSERT INTO scene VALUES ({num})')
        print("new scene: ", num)
        self.conn.commit()

    def put_command(self):
        pass

    def put_vehicle_status(self):
        pass

    def set_scene_num(self, num):
        self.scene_num = num

    def get_scene_num(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM scene ORDER BY ROWID DESC LIMIT 1")
        result = cur.fetchall()
        print(result)
        if len(result) == 0:
            return -1
        else:
            return result[0]

    def get_vehicle_work(self):
        pass

    def get_vehicle_charge(self):
        pass

    def get_total_work(self):
        pass

    def get_node_freq(self):
        pass

    def create_new_scene(self):
        last_num = self.get_scene_num()
        print(last_num)
        if last_num == -1:
            self.put_scene_num(1)
            self.set_scene_num(1)
        else:
            self.put_scene_num(last_num[0] + 1)
            self.set_scene_num(last_num[0] + 1)

#db = DB()
#db.create_new_scene()