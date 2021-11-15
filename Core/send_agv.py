# 짐을 실은 AGV를 unload 포트로 보내는 로직입니다.
from .a_star import a_star, heuristic


def send_agv(node_list, wait_list, vehicle_list, path_linked_list, unloadable_port_list):
    for vehicle in vehicle_list:
        # AGV가 대기 장소에 있다면 (우선권)
        if vehicle.status == 11 and vehicle.node == 587:
            if node_list[289].status != -2:
                # 찜하기
                node_list[289].status = -2
                # 290으로 가는 append 로직
                a_star_path = a_star(587, 290, path_linked_list, node_list)
                vehicle.command(a_star_path, 22 , node_list, loadable_port_list, unloadable_port_list)
                continue
            elif node_list[290].status != -2:
                port.status = -2
                # append
                a_star_path = a_star(587, 291, path_linked_list, node_list)
                vehicle.command(a_star_path, 22 , node_list, loadable_port_list, unloadable_port_list)
                continue

        elif vehicle.status == 11 and vehicle.node == 17:
            if node_list[289].status != -2:
                # 찜하기
                node_list[289].status = -2
                # 290으로 가는 append 로직
                a_star_path = a_star(17, 290, path_linked_list, node_list)
                vehicle.command(a_star_path, 22 , node_list, loadable_port_list, unloadable_port_list)
                continue
            elif node_list[290].status != -2:
                port.status = -2
                # append
                a_star_path = a_star(17, 291, path_linked_list, node_list)
                vehicle.command(a_star_path, 22 , node_list, loadable_port_list, unloadable_port_list)
                continue

        # 짐을 실은 AGV를 1차 목적지로 보내기
        # 짐을 다 싣고 AGV가 있으면

        # vehicle.node
        # node_list 이용, port의 loaded == 1인지 확인
        if vehicle.status == 10 and node_list[vehicle.node-1].loaded == 1:
            unloadable_port_list.remove(node_list[vehicle.node-1])
            # 위치에 따라서 분기
            # 좌측 상단 3번 포트
            if 340 <= vehicle.node <= 363:
                a_star_path = a_star(vehicle.node, 587, path_linked_list, node_list)
                # 나올 때 후진
                a_star_path[0] = a_star_path[0] * -1
                vehicle.command(a_star_path, 25, node_list, loadable_port_list, unloadable_port_list)
            # 좌측 하단 3번 포트
            elif 392 <= vehicle.node <= 415:
                a_star_path = a_star(vehicle.node, 587, path_linked_list, node_list)
                a_star_path[0] = a_star_path[0] * -1
                vehicle.command(a_star_path, 25, node_list, loadable_port_list, unloadable_port_list)
            # 우측 상단 3번 포트
            elif 364 <= vehicle.node <= 387:
                a_star_path = a_star(vehicle.node, 17, path_linked_list, node_list)
                a_star_path[0] = a_star_path[0] * -1
                vehicle.command(a_star_path, 25, node_list, loadable_port_list, unloadable_port_list)
            # 우측 하단 3번 포트
            elif 416 <= vehicle.node <= 439:
                a_star_path = a_star(vehicle.node, 17, path_linked_list, node_list)
                a_star_path[0] = a_star_path[0] * -1
                vehicle.command(a_star_path, 25, node_list, loadable_port_list, unloadable_port_list)
            # 중앙 상단 1번 포트
            elif 388 <= vehicle.node <= 389:
                a_star_path = a_star(vehicle.node, 645, path_linked_list, node_list)
                a_star_path[0] = a_star_path[0] * -1
                vehicle.command(a_star_path, 25, node_list, loadable_port_list, unloadable_port_list)
            elif 390 <= vehicle.node <= 391:
                a_star_path = a_star(vehicle.node, 648, path_linked_list, node_list)
                a_star_path[0] = a_star_path[0] * -1
                vehicle.command(a_star_path, 25, node_list, loadable_port_list, unloadable_port_list)
            # 중앙 하단 1번 포트
            elif 440 <= vehicle.node <= 441:
                a_star_path = a_star(vehicle.node, 779, path_linked_list, node_list)
                a_star_path[0] = a_star_path[0] * -1
                vehicle.command(a_star_path, 25, node_list, loadable_port_list, unloadable_port_list)
            elif 442 <= vehicle.node <= 443:
                a_star_path = a_star(vehicle.node, 782, path_linked_list, node_list)
                a_star_path[0] = a_star_path[0] * -1
                vehicle.command(a_star_path, 25, node_list, loadable_port_list, unloadable_port_list)
                
        # 1차 목적지를 지나기 전 2차 제어하기
        # 좌측 3번 포트
        # 585에 도착하는 순간부터 path[0]이 586
        if vehicle.desti_node == 587 and vehicle.path and vehicle.path[0] == 586:
            for port in unloadable_port_list:
                if port.NUM == 290 and port.status != -2:
                    # 찜하기
                    port.status = -2
                    # 290으로 가는 append 로직
                    a_star_path = a_star(587, 290, path_linked_list, node_list)
                    vehicle.command(a_star_path, 22 , node_list, loadable_port_list, unloadable_port_list)
                    break
                elif port.NUM == 291 and port.status != -2:
                    port.status = -2
                    # append
                    a_star_path = a_star(587, 291, path_linked_list, node_list)
                    vehicle.command(a_star_path, 22 , node_list, loadable_port_list, unloadable_port_list)
                    break
            # unload_port가 차있어서 정지해야 하는 상황
            # append 경로 마지막까지 왔는데 끝이면 11로 된다. (대기 상태)

        # 우측 3번 포트
        # 922에 도착하는 순간부터 path[0]이 73
        if vehicle.desti_node == 17 and vehicle.path and vehicle.path[0] == 73:
            for port in unloadable_port_list:
                if port.NUM == 290 and port.status != -2:
                    # 찜하기
                    port.status = -2
                    # 290으로 가는 append 로직
                    a_star_path = a_star(17, 290, path_linked_list, node_list)
                    vehicle.command(a_star_path, 22 , node_list, loadable_port_list, unloadable_port_list)
                    break
                elif port.NUM == 291 and port.status != -2:
                    # 찜하기
                    port.status = -2
                    # append
                    a_star_path = a_star(17, 291, path_linked_list, node_list)
                    vehicle.command(a_star_path, 22 , node_list, loadable_port_list, unloadable_port_list)
                    break
            # unload_port가 차있어서 정지해야 하는 상황

        # 중앙 하단 1번 포트
        # 못 내릴 수가 없는 구조
        # 244에 도착하는 순간부터 path[0]이 779
        if vehicle.desti_node == 645 and vehicle.path and vehicle.path[0] == 645:
            # 가장 가까운 것부터
            for idx in range(315, 291, -1):
                if port in unloadable_port_list:
                    if port.NUM == idx and port.status != -2:
                        # 찜하기
                        port.status = -2
                        # idx로 가는 append 로직
                        a_star_path = a_star(43, idx, path_linked_list, node_list)
                        vehicle.command(a_star_path, 22 , node_list, loadable_port_list, unloadable_port_list)
                        break

        if vehicle.desti_node == 648 and vehicle.path and vehicle.path[0] == 648:
            # 가장 가까운 것부터
            for idx in range(316, 340):
                if idx in unloadable_port_list:
                    if port.NUM == idx and port.status != -2:
                        # 찜하기
                        port.status = -2
                        # idx로 가는 append 로직
                        a_star_path = a_star(649, idx, path_linked_list, node_list)
                        vehicle.command(a_star_path, 22 , node_list, loadable_port_list, unloadable_port_list)
                        break

        # 중앙 상단 1번 포트
        # 못 내릴 수가 없는 구조
        # 244에 도착하는 순간부터 path[0]이 779
        if vehicle.desti_node == 779 and vehicle.path and vehicle.path[0] == 779:
            # 가장 가까운 것부터
            for idx in range(467, 443, -1):
                if idx in unloadable_port_list:
                    if port.NUM == idx and port.status != -2:
                        # 찜하기
                        port.status = -2
                        # idx로 가는 append 로직
                        a_star_path = a_star(243, idx, path_linked_list, node_list)
                        vehicle.command(a_star_path, 22 , node_list, loadable_port_list, unloadable_port_list)
                        break
            
        # 244에 도착하는 순간부터 path[0]이 782
        if vehicle.desti_node == 782 and vehicle.path and vehicle.path[0] == 782:
            # 가장 가까운 것부터
            for idx in range(468, 492):
                if idx in unloadable_port_list:
                    if port.NUM == idx and port.status != -2:
                        # 찜하기
                        port.status = -2
                        # idx로 가는 append 로직
                        a_star_path = a_star(783, idx, path_linked_list, node_list)
                        vehicle.command(a_star_path, 22 , node_list, loadable_port_list, unloadable_port_list)
                        break