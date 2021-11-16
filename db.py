import sqlite3
import datetime


class DB:
    def __init__(self):
        try:
            self.conn = sqlite3.connect("simul_data.db", check_same_thread=False)
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
            id INTEGER,\
            scene_id INTEGER,\
            time INTEGER,\
            name TEXT,\
            cur_node INTEGER,\
            desti_node INTEGER,\
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

    def add_scene_num(self, num):
        cur = self.conn.cursor()
        cur.execute(f'INSERT INTO scene VALUES ({num})')
        print("new scene: ", num)
        self.conn.commit()

    def add_command(self, v_id, start_node, desti_node, path, type, time):
        cur = self.conn.cursor()
        path_str = ','.join(str(e) for e in path)
        query = f'INSERT INTO command (scene_id, vehicle_id, start_node, desti_node, path, type, created_at, is_checked) ' \
                f'VALUES ({self.scene_num}, {v_id}, {start_node}, {desti_node}, "{path_str}",' \
                f'{type}, {time}, 0)'
        print(query)
        cur.execute(query)
        self.conn.commit()

    def add_vehicle_status(self, v, time):
        cur = self.conn.cursor()
        query = f'INSERT INTO vehicle ' \
                f'(id, scene_id, time, name, cur_node, desti_node, x, y, status, velocity, angle, battery, loaded) ' \
                f'VALUES ({v.NUM}, {self.scene_num}, {time}, "{v.NAME}", {v.node}, {v.desti_node}, ' \
                f'{round(v.x,2)}, {round(v.y, 2)}, {v.status}, {round(v.velocity, 2)}, {v.angle}, {round(v.battery, 2)}, {v.loaded})'
        print(query)
        cur.execute(query)
        self.conn.commit()

    def add_vehicle_status_all(self, v_list, time):
        cur = self.conn.cursor()
        data = []
        for v in v_list:
            t = (v.NUM, self.scene_num, time, v.NAME, v.node, v.desti_node, round(v.x,2), round(v.y,2),
                              v.status, round(v.velocity, 2), v.angle, round(v.battery, 2), v.loaded)
            data.append(t)
        query = f'INSERT INTO vehicle ' \
                f'VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)'
        print(query)
        print(data)
        cur.executemany(query, data)
        self.conn.commit()

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
        """
        vehicle status의 누적 시간
        :return name_list, stat_list: 1차원 리스트, 2차원 리스트
        ['V01', 'V02', ...],
        [[wait 누적 시간 리스트], [charge...], [move...], [load...], [unload,,,]]
        """
        cur = self.conn.cursor()
        name_list = []
        stat_list = [[], [], [], [], []]

        cnt = 1
        while True:
            query = f'SELECT "name" FROM vehicle WHERE id={cnt} LIMIT 1'
            cur.execute(query)
            name = cur.fetchall()
            if len(name) == 0:
                break
            name_list.append(name[0][0])
            cnt += 1

        for i in range(len(name_list)):
            query = f'SELECT COUNT(*) FROM vehicle WHERE id={i+1} and status=10'
            cur.execute(query)
            res = cur.fetchall()
            stat_list[0].append(res[0][0])
            query = f'SELECT COUNT(*) FROM vehicle WHERE id={i + 1} and status=80 or status=81'
            cur.execute(query)
            res = cur.fetchall()
            stat_list[1].append(res[0][0])
            query = f'SELECT COUNT(*) FROM vehicle WHERE id={i + 1} and status=20'
            cur.execute(query)
            res = cur.fetchall()
            stat_list[2].append(res[0][0])
            query = f'SELECT COUNT(*) FROM vehicle WHERE id={i + 1} and status=30'
            cur.execute(query)
            res = cur.fetchall()
            stat_list[3].append(res[0][0])
            query = f'SELECT COUNT(*) FROM vehicle WHERE id={i + 1} and status=40'
            cur.execute(query)
            res = cur.fetchall()
            stat_list[4].append(res[0][0])
        # print(stat_list)
        return name_list, stat_list


    def get_vehicle_charge(self):
        """
        vehicle의 battery 1초 간격마다 변화를 list로 반환

        :return data: 2차원 리스트
        [[vehicle_name, battery_list], ...]
        """

        cur = self.conn.cursor()
        data = []
        cnt = 1
        while True:
            query = f'SELECT "name" FROM vehicle WHERE id={cnt} LIMIT 1'
            cur.execute(query)
            name = cur.fetchall()
            if len(name) == 0:
                break

            query = f'SELECT "battery" FROM vehicle WHERE id={cnt}'
            cur.execute(query)
            battery = cur.fetchall()
            battery_list = []
            for x in battery:
                battery_list.append(x[0])
            data.append((name[0][0], battery_list))
            # print(data)
            cnt += 1
        print(data)
        return data

    def get_total_work(self):
        pass

    def get_node_freq(self):
        pass

    def create_new_scene(self):
        last_num = self.get_scene_num()
        print(last_num)
        if last_num == -1:
            self.add_scene_num(1)
            self.set_scene_num(1)
        else:
            self.add_scene_num(last_num[0] + 1)
            self.set_scene_num(last_num[0] + 1)

db = DB()
# db.db_clear()
# db.db_init()
# db.create_new_scene()
# db.set_scene_num(1)
# db.add_command(1, 1, 5, [2,3,4,5], 25, 1)
# db.add_command(2, 11, 15, [12,13,14,15], 25, 1)
# db.get_vehicle_charge()
db.get_vehicle_work()