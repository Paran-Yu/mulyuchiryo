##########################
# main에 정의된 함수는 추후 UI에서 버튼을 클릭함으로써 동작한다
# UI가 완성되지 않았으므로 테스트를 위해 임시로 main에 정의한다
##########################

import sys
import os.path
sys.path.append(os.path.abspath(os.path.dirname('UI/')))

import time
import threading
import mapreader
from simulator import simulator
from Core.a_star import a_star, heuristic
import Core2.astar as astar, Core2.planner as planner
from Core.call_agv import call_agv
from Core.send_agv import send_agv
from Core.back_agv import back_agv
from Core.check_collision import check_collision
from UI import mainPage
import db

# simulate attribute
simulate_speed = 0.1      # 0.5: 2배속, 0.1: 10배속
simulate_time = 0       # 시간 경과[sec]
simulate_cnt = 0        # 반송 완료 건수

# layout component
img = {}
map_data = {}
port_list = []
wait_list = []
node_list = []
path_list = []
path_linked_list = []
vehicle_list = []
loadable_port_list = []
unloadable_port_list = []
solutions = {}

VEHICLE_STATUS = {
    00: "INIT",
    10: "WAITING",
    20: "MOVE",
    30: "LOADING",
    40: "UNLOADING",
    80: "CHARGING",
    81: "CHARGING_WAIT",
    91: "COLLIDED",
    99: "ERROR"
}

# DB connection
simul_db = db.DB()

#########################
# UI용 함수 정의

# map data 읽어오기
def read_map():
    global img, map_data
    global port_list, wait_list, node_list, path_list, vehicle_list, path_linked_list
    img, map_data = mapreader.read_layout()
    port_list, wait_list, node_list, path_list, vehicle_list, path_linked_list = mapreader.read_component()


# UI에서 simulate 버튼을 누르면 simulate 시작
def start_simulate(plot=True):
    global simulate_time, simulate_cnt
    # simulation 초기화
    simulator.simulate_init(node_list, port_list, wait_list, vehicle_list, path_list, plot)
    simulate_time = 0
    simulate_cnt = 0
    # 새로운 scene 생성
    simul_db.create_new_scene()
    # 시뮬레이션 무한 루프 실행
    simulate_loop()

    for v in vehicle_list:
        if v.NUM in solutions:
            v.command(solutions[v.NUM],21,node_list, loadable_port_list, unloadable_port_list)
    
    while plot:
        simulator.plot_update(simulate_speed, node_list, vehicle_list)


# simulate_speed마다 루틴 실행
# TODO: 도중에 simulate_speed가 바뀌면 대응하는 법...
def simulate_loop():
    global simulate_time, simulate_cnt
    global loadable_port_list, unloadable_port_list

    simulate_time += 1

    simulator.simulate_routine(node_list, port_list, wait_list, vehicle_list, loadable_port_list, unloadable_port_list,
                               simulate_cnt)

    call_agv(node_list, wait_list, vehicle_list, path_linked_list, loadable_port_list, unloadable_port_list)
    send_agv(node_list, vehicle_list, path_linked_list, loadable_port_list, unloadable_port_list)
    back_agv(node_list, vehicle_list, path_linked_list, loadable_port_list, unloadable_port_list)
    check_collision(node_list, vehicle_list, path_linked_list)
    
    # simulate_speed마다 루틴 함수를 새로 수행
    threading.Timer(simulate_speed, simulate_loop).start()

# searching
def search_routes():
    env = planner.Environment(vehicle_list,node_list,path_linked_list)
    # Searching
    cbs = planner.CBS(env)
    solution = cbs.search()
    if not solution:
        print("Solution not found" )
        return
    return solution
    

#######################
# Test용 main
if __name__ == "__main__":
    print(__name__)
    app = mainPage.QApplication(mainPage.sys.argv)
    screen = app.desktop()  # 컴퓨터 전체 화면 rect
    win = mainPage.MainPage(screen.screenGeometry())  # 메인 화면 생성
    win.show()  # 화면 띄우기
    app.exec_()  # 루프 실행
    read_map()
    start_simulate()
