# 반송을 완료하고 대기/충전 장소로 돌아오는 로직입니다.
from .a_star import a_star, heuristic


def back_agv(node_list, vehicle_list, path_linked_list, loadable_port_list, unloadable_port_list):
    for vehicle in vehicle_list:
        # 짐을 다 내림
        if vehicle.status == 10 and node_list[vehicle.node-1] in unloadable_port_list:
            unloadable_port_list.remove(node_list[vehicle.node-1])
            # 위치에 따라서 분기
            # 우측 상단 4번 포트
            if 290 <= vehicle.node <= 291:
                # 일단 충돌하지 않도록 빠져나와서
                a_star_path = a_star(vehicle.node, 143, path_linked_list, node_list)
                # 대기/충전 장소 찾고
                for idx in range(534, 542):
                    # 비었다면                
                    if not node_list[idx-1].using:
                        a_star_path += a_star(143, node_list[idx-1].NUM ,path_linked_list, node_list)
                        break
                # 나올 때 후진
                a_star_path[0] = a_star_path[0] * -1
                # 대기하기
                if vehicle.battery >= 70:
                    vehicle.command(a_star_path, 20, node_list, loadable_port_list, unloadable_port_list)
                # 충전하기
                else:
                    vehicle.command(a_star_path, 23, node_list, loadable_port_list, unloadable_port_list)
            # 좌측 상단 2번 포트
            elif 292 <= vehicle.node <= 315:
                a_star_path = a_star(vehicle.node, 630, path_linked_list, node_list)
                a_star_path += a_star(630, 595, path_linked_list, node_list)
                for idx in range(499, 491, -1):
                    if not node_list[idx-1].using:
                        a_star_path += a_star(595, node_list[idx-1].NUM ,path_linked_list, node_list)
                        break
                a_star_path[0] = a_star_path[0] * -1
                if vehicle.battery >= 70:
                    vehicle.command(a_star_path, 20, node_list, loadable_port_list, unloadable_port_list)
                else:
                    vehicle.command(a_star_path, 23, node_list, loadable_port_list, unloadable_port_list)
            # 좌측 하단 2번 포트
            elif 444 <= vehicle.node <= 467:
                for idx in range(519, 511, -1):
                    if not node_list[idx-1].using:
                        a_star_path += a_star(vehicle.node, node_list[idx-1].NUM ,path_linked_list, node_list)
                        break
                a_star_path[0] = a_star_path[0] * -1
                if vehicle.battery >= 70:
                    vehicle.command(a_star_path, 20, node_list, loadable_port_list, unloadable_port_list)
                else:
                    vehicle.command(a_star_path, 23, node_list, loadable_port_list, unloadable_port_list)
            # 우측 상단 2번 포트
            elif 316 <= vehicle.node <= 339:
                a_star_path = a_star(vehicle.node, 720, path_linked_list, node_list)
                for idx in range(509, 501, -1):
                    if not node_list[idx-1].using:
                        a_star_path += a_star(720, node_list[idx-1].NUM ,path_linked_list, node_list)
                        break
                a_star_path[0] = a_star_path[0] * -1
                if vehicle.battery >= 70:
                    vehicle.command(a_star_path, 20, node_list, loadable_port_list, unloadable_port_list)
                else:
                    vehicle.command(a_star_path, 23, node_list, loadable_port_list, unloadable_port_list)
            # 우측 하단 2번 포트
            elif 468 <= vehicle.node <= 491:
                a_star_path = a_star(vehicle.node, 144, path_linked_list, node_list)
                a_star_path += a_star(vehicle.node, 720, path_linked_list, node_list)
                for idx in range(529, 521, -1):
                    if not node_list[idx-1].using:
                        a_star_path += a_star(720, node_list[idx-1].NUM ,path_linked_list, node_list)
                        break
                a_star_path[0] = a_star_path[0] * -1
                if vehicle.battery >= 70:
                    vehicle.command(a_star_path, 20, node_list, loadable_port_list, unloadable_port_list)
                else:
                    vehicle.command(a_star_path, 23, node_list, loadable_port_list, unloadable_port_list)