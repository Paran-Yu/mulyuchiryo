# 짐을 실은 AGV를 unload 포트로 보내는 로직입니다.
from .a_star import a_star, heuristic


def send_agv(node_list, wait_list, vehicle_list, path_linked_list):
    for vehicle in vehicle_list:
        # 짐을 다 실은 AGV가 있으면
        if vehicle.status == ? and vehicle.loaded == 1:
            