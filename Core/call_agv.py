# 반송할 수 있는 조건이 충족되면 load 포트로 AGV를 부르는 로직입니다.
from .a_star import a_star, heuristic

loadable_copy_list = []
unloadable_copy_list = []


def check_wait_point(start, end, port_number, node_list, vehicle_list, wait_list, path_linked_list, loadable_port_list, unloadable_port_list):
    # 예시 : 9,8 (경로에 있는 대기 장소부터 체크 후) 7~0 (가까운 충전/대기 장소 체크)
    for idx in range(start, end, -1):
        # AGV가 있고 충전 장소를 나오는 조건을 충족해 있다면
        # using은 찜할 때도 쓴다. 다만 status로 인해서 걸러질 것이다.
        if wait_list[idx].using and vehicle_list[wait_list[idx].using-1].status in [0, 10, 81]:
            a_star_path = a_star(wait_list[idx].NUM, port_number, path_linked_list, node_list)
            a_star_path[0] = a_star_path[0] * -1
            vehicle_list[wait_list[idx].using-1].command(a_star_path, 21, node_list, loadable_port_list, unloadable_port_list)
            node_list[port_number-1].status = -2
            break


def call_agv(node_list, wait_list, vehicle_list, path_linked_list,loadable_port_list, unloadable_port_list):
    global loadable_copy_list, unloadable_copy_list
    # 같은 input이라면 두 번 실행할 필요없다.
    if loadable_port_list != loadable_copy_list or unloadable_port_list != unloadable_copy_list:
        loadable_copy_list = loadable_port_list.copy()
        unloadable_copy_list = unloadable_port_list.copy()
        # 반송 조건 체크
        if loadable_port_list and unloadable_port_list:
            for load_port in loadable_port_list:
                for unload_port in unloadable_port_list:
                    # 아래 조건 충족시 반송 시작
                    if unload_port.NUM in load_port.UNLOAD_LIST and load_port.status == 1:

                        # load_port에 따라서 분기
                        # 좌측 상단 3번 포트
                        if 340 <= load_port.NUM <= 363:
                            check_wait_point(9, -1, load_port.NUM, node_list,  vehicle_list, wait_list, path_linked_list, loadable_port_list, unloadable_port_list)
                        # # 좌측 하단 3번 포트
                        elif 392 <= load_port.NUM <= 415:
                            check_wait_point(29, 19, load_port.NUM, node_list, vehicle_list, wait_list, path_linked_list, loadable_port_list, unloadable_port_list)
                        # # 우측 상단 3번 포트
                        elif 364 <= load_port.NUM <= 387:
                            check_wait_point(19, 9, load_port.NUM, node_list,  vehicle_list, wait_list, path_linked_list, loadable_port_list, unloadable_port_list)
                        # # 우측 하단 3번 포트
                        elif 416 <= load_port.NUM <= 439:
                            check_wait_point(39, 29, load_port.NUM, node_list, vehicle_list, wait_list, path_linked_list, loadable_port_list, unloadable_port_list)
                        # # 중앙 상단 1번 포트
                        # elif 388 <= load_port.NUM <= 391:
                            # 숫자가 연속되지 않아서 두 지점을 체크하고
                            # for idx in range(40, 42):
                            #     if wait_list[idx].using and vehicle_list[wait_list[idx].using-1].status in [0, 10, 81]:
                            #         a_star_path = a_star(wait_list[idx].NUM, load_port.NUM, path_linked_list, node_list)
                            #         a_star_path[0] = a_star_path[0] * -1
                            #         vehicle_list[wait_list[idx].using-1].command(a_star_path, 21, node_list, loadable_port_list, unloadable_port_list)
                            #         node_list[load_port.NUM-1].status = -2
                            #         break
                            #  break가 안 걸렸다면 충전/대기 장소도 체크하기
                            # else:
                            # check_wait_point(49, 41, load_port.NUM, node_list, vehicle_list, wait_list, path_linked_list, loadable_port_list, unloadable_port_list)
                        # # 중앙 하단 1번 포트
                        # elif 440 <= load_port.NUM <= 443:
                            # check_wait_point(51, 41, load_port.NUM, node_list, vehicle_list, wait_list, path_linked_list, loadable_port_list, unloadable_port_list)
                            # check_wait_point(49, 41, load_port.NUM, node_list, vehicle_list, wait_list, path_linked_list, loadable_port_list, unloadable_port_list)

                        elif 388 <= load_port.NUM <= 391 or 440 <= load_port.NUM <= 443:
                            for idx in range(49, 41, -1):
                                # AGV가 있고 충전 장소를 나오는 조건을 충족해 있다면
                                # using은 찜할 때도 쓴다. 다만 status로 인해서 걸러질 것이다.
                                if wait_list[idx].using and vehicle_list[wait_list[idx].using-1].status in [0, 10, 81]:
                                    # 왼쪽으로 빠져서
                                    a_star_path = a_star(wait_list[idx].NUM, 202, path_linked_list, node_list)
                                    a_star_path += a_star(202, load_port.NUM, path_linked_list, node_list)
                                    a_star_path[0] = a_star_path[0] * -1
                                    vehicle_list[wait_list[idx].using-1].command(a_star_path, 21, node_list, loadable_port_list, unloadable_port_list)
                                    node_list[load_port.NUM-1].status = -2
                                    break