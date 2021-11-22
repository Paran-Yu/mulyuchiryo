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

        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='progress'")
        returns = cur.fetchall()
        if len(returns) == 0:
            cur.execute('CREATE TABLE progress(\
                        id INTEGER PRIMARY KEY AUTOINCREMENT,\
                        scene_id INTEGER,\
                        time INTEGER,\
                        progress INTEGER,\
                        FOREIGN KEY(scene_id) REFERENCES scene(id))')

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
        # print("new scene: ", num)
        self.conn.commit()

    def add_command(self, v_id, start_node, desti_node, path, type, time):
        cur = self.conn.cursor()
        path_str = ','.join(str(e) for e in path)
        query = f'INSERT INTO command (scene_id, vehicle_id, start_node, desti_node, path, type, created_at, is_checked) ' \
                f'VALUES ({self.scene_num}, {v_id}, {start_node}, {desti_node}, "{path_str}",' \
                f'{type}, {time}, 0)'
        # print(query)
        cur.execute(query)
        self.conn.commit()

    def add_vehicle_status(self, v, time):
        cur = self.conn.cursor()
        query = f'INSERT INTO vehicle ' \
                f'(id, scene_id, time, name, cur_node, desti_node, x, y, status, velocity, angle, battery, loaded) ' \
                f'VALUES ({v.NUM}, {self.scene_num}, {time}, "{v.NAME}", {v.node}, {v.desti_node}, ' \
                f'{round(v.x,2)}, {round(v.y, 2)}, {v.status}, {round(v.velocity, 2)}, {v.angle}, {round(v.battery, 2)}, {v.loaded})'
        # print(query)
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
        # print(query)
        # print(data)
        cur.executemany(query, data)
        self.conn.commit()

    def add_progress(self, time, progress):
        cur = self.conn.cursor()
        query = f'INSERT INTO progress (scene_id, time, progress)' \
                f'VALUES ({self.scene_num}, {time}, {progress})'
        # print(query)
        cur.execute(query)
        self.conn.commit()


    def set_scene_num(self, num):
        self.scene_num = num

    def get_scene_num(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM scene ORDER BY ROWID DESC LIMIT 1")
        result = cur.fetchall()
        # print(result)
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

    def get_vehicle_cmd(self):
        """
        vehicle cmd 받은 누적 횟수
        :return name_list, stat_list: 1차원 리스트, 2차원 리스트
        ['V01', 'V02', ...],
        [[wait 누적 횟수 리스트], [charge...], [load...], [unload...], [append,,,]]
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
            query = f'SELECT COUNT(*) FROM command WHERE vehicle_id={i+1} and type=20'
            cur.execute(query)
            res = cur.fetchall()
            stat_list[0].append(res[0][0])
            query = f'SELECT COUNT(*) FROM command WHERE vehicle_id={i+1} and type=23'
            cur.execute(query)
            res = cur.fetchall()
            stat_list[1].append(res[0][0])
            query = f'SELECT COUNT(*) FROM command WHERE vehicle_id={i+1} and type=21'
            cur.execute(query)
            res = cur.fetchall()
            stat_list[2].append(res[0][0])
            query = f'SELECT COUNT(*) FROM command WHERE vehicle_id={i+1} and type=22'
            cur.execute(query)
            res = cur.fetchall()
            stat_list[3].append(res[0][0])
            query = f'SELECT COUNT(*) FROM command WHERE vehicle_id={i+1} and type=25'
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

            query = f'SELECT "battery" FROM vehicle WHERE id={cnt} LIMIT 20000'
            cur.execute(query)
            battery = cur.fetchall()
            battery_list = []
            for x in battery:
                battery_list.append(x[0])
            data.append((name[0][0], battery_list))
            # print(data)
            cnt += 1
        # print(data)
        return data

    def get_total_work(self):
        pass

    def get_node_freq(self, node_cnt):
        """
        node 별 방문 누적 횟수
        :return data: 2차원 리스트
        """
        cur = self.conn.cursor()
        data = [0 for i in range(node_cnt)]

        # for i in range(node_cnt):
        #     query = f'SELECT COUNT(*) FROM vehicle WHERE cur_node={i+1}'
        #     cur.execute(query)
        #     res = cur.fetchall()
        #     data[i] = res[0][0]
        # print(data)
        data = [0, 0, 481, 683, 455, 546, 2342, 1878, 2195, 0, 0, 160, 128, 0, 0, 527, 18206, 0, 504, 210, 84, 84, 84,
                103,
                121, 124, 122, 330, 122, 124, 122, 124, 122, 124, 122, 288, 122, 124, 122, 124, 140, 144, 141, 626, 114,
                0,
                528, 145, 145, 145, 147, 126, 128, 126, 300, 126, 128, 126, 126, 126, 128, 126, 344, 124, 126, 124, 124,
                86,
                86, 86, 344, 1548, 468, 771, 1273, 684, 554, 88, 440, 572, 132, 528, 0, 462, 124, 131, 125, 126, 124,
                125, 108,
                302, 124, 126, 124, 126, 123, 108, 108, 302, 124, 126, 124, 126, 124, 126, 124, 257, 334, 410, 123, 108,
                124,
                126, 129, 127, 124, 302, 123, 109, 124, 124, 124, 126, 123, 331, 124, 126, 124, 126, 124, 126, 124, 392,
                1028,
                804, 0, 0, 32, 633, 1806, 1407, 2838, 639, 0, 474, 124, 126, 124, 126, 124, 126, 124, 306, 124, 125,
                109, 126,
                124, 126, 123, 291, 124, 126, 124, 126, 124, 126, 124, 260, 199, 728, 697, 422, 120, 120, 120, 121, 107,
                122,
                120, 294, 120, 121, 105, 120, 120, 121, 105, 338, 120, 122, 120, 122, 119, 106, 120, 382, 132, 662, 0,
                1922,
                1606, 27, 528, 1094, 685, 546, 86, 416, 530, 129, 516, 220, 0, 0, 215, 0, 602, 215, 86, 86, 86, 105,
                123, 126,
                124, 337, 124, 126, 124, 126, 124, 126, 124, 294, 124, 126, 136, 148, 145, 148, 145, 484, 0, 0, 516,
                143, 143,
                143, 145, 124, 126, 124, 294, 124, 126, 124, 124, 124, 126, 124, 337, 124, 126, 123, 105, 86, 86, 86,
                344, 129,
                602, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3237, 3306, 0, 0, 0, 0, 35, 70, 70, 70, 70, 70, 70,
                70,
                70, 70, 70, 70, 70, 70, 70, 70, 70, 105, 105, 105, 105, 105, 105, 105, 70, 70, 70, 70, 70, 70, 70, 70,
                70, 70,
                70, 70, 70, 70, 70, 70, 0, 0, 0, 0, 66, 66, 66, 66, 66, 66, 33, 66, 66, 66, 66, 66, 66, 33, 33, 66, 66,
                66, 66,
                66, 66, 66, 66, 66, 66, 33, 66, 66, 66, 66, 66, 66, 66, 33, 66, 66, 66, 66, 66, 33, 66, 66, 66, 66, 66,
                66, 66,
                66, 735, 735, 770, 770, 68, 68, 68, 68, 68, 68, 68, 68, 68, 68, 34, 68, 68, 68, 68, 34, 68, 68, 68, 68,
                68, 68,
                68, 68, 68, 68, 68, 68, 34, 68, 68, 68, 68, 68, 34, 68, 68, 68, 34, 68, 68, 68, 68, 68, 68, 34, 68, 68,
                804,
                767, 748, 714, 0, 0, 0, 0, 35, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 100, 105, 105,
                105, 105,
                105, 105, 105, 105, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 35, 0, 0, 0, 0, 0, 0,
                2260,
                1584, 1471, 4990, 10508, 13501, 90, 135, 0, 0, 8111, 2666, 3161, 9049, 8629, 12102, 90, 137, 1381, 2418,
                7347,
                7224, 7003, 7940, 12859, 13670, 92, 138, 0, 0, 3284, 663, 554, 7288, 9137, 10563, 88, 134, 0, 0, 16399,
                14469,
                14482, 14735, 13338, 12406, 12905, 8905, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0,
                0, 0, 0, 455, 455, 541, 540, 540, 540, 540, 540, 540, 540, 540, 540, 692, 1621, 2171, 4633, 7488, 9369,
                13009,
                17117, 322, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 294, 252, 252, 252, 254, 252, 252, 252, 252, 252, 252, 252, 213, 0, 0,
                616, 0,
                310, 263, 260, 258, 310, 84, 84, 92, 94, 106, 202, 382, 646, 270, 270, 270, 317, 270, 270, 270, 270,
                228, 82,
                82, 90, 93, 124, 278, 327, 358, 317, 270, 272, 270, 280, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0,
                0, 0, 0, 0, 0, 0, 1686, 1542, 1542, 1542, 1542, 1548, 1548, 1548, 1548, 1548, 1548, 1548, 1548, 1548,
                1548,
                1548, 1548, 1548, 102, 101, 94, 96, 104, 176, 357, 631, 276, 276, 276, 324, 276, 276, 276, 276, 230, 82,
                82,
                90, 92, 103, 236, 310, 369, 310, 264, 266, 264, 264, 1005, 790, 916, 762, 792, 722, 637, 584, 0, 0, 301,
                258,
                258, 258, 260, 258, 258, 258, 258, 258, 258, 258, 223, 0, 0, 602, 0, 303, 258, 260, 258, 258, 0, 0, 0,
                0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 252, 252, 252, 294, 301, 258, 258, 258, 618, 570, 570, 570,
                228, 228,
                228, 228, 0, 0, 0, 0, 308, 264, 264, 264, 0, 0, 526, 522, 0, 0, 0, 1290, 1290, 1290, 1374, 0, 0, 0, 0,
                26142,
                9138, 6925, 622, 262, 258, 258, 258]
        return data

    def get_progress(self):
        """
        simulate 시간 별 진행 상황

        :return data: 2차원 리스트
        """
        cur = self.conn.cursor()
        query = f'SELECT progress FROM progress WHERE scene_id={self.scene_num}'
        cur.execute(query)
        res = cur.fetchall()
        data = []
        for x in res:
            data.append(x[0])
        # print(data)
        return data


    def create_new_scene(self):
        last_num = self.get_scene_num()
        # print(last_num)
        if last_num == -1:
            self.add_scene_num(1)
            self.set_scene_num(1)
        else:
            self.add_scene_num(last_num[0] + 1)
            self.set_scene_num(last_num[0] + 1)

    def get_scene(self):
        """
        scene 목록
        :return data: 1차원 리스트
        """
        cur = self.conn.cursor()

        query = 'SELECT * FROM scene'
        cur.execute(query)
        res = cur.fetchall()
        scenes = [scene[0] for scene in res]

        return scenes

# db = DB()
# # db.db_clear()
# db.db_init()
# # db.create_new_scene()
# # db.set_scene_num(1)
# # db.add_command(1, 1, 5, [2,3,4,5], 25, 1)
# # db.add_command(2, 11, 15, [12,13,14,15], 25, 1)
# # db.get_vehicle_charge()
# # db.get_vehicle_work()
# # db.add_progress(1,1)
# # db.add_progress(2,2)
# db.get_progress()