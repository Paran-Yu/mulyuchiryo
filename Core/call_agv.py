# 반송할 수 있는 조건이 충족되면 AGV를 부르는 로직입니다.
from .a_star import a_star, heuristic

loadable_copy_list = []
unloadable_copy_list = []

def call_agv(node_list, wait_list, path_linked_list,loadable_port_list, unloadable_port_list):
    global loadable_copy_list, unloadable_copy_list

    # 같은 input이라면 두 번 실행할 필요없다.
    if loadable_port_list != loadable_copy_list or unloadable_port_list != unloadable_copy_list:
        loadable_copy_list = loadable_port_list
        unloadable_copy_list = unloadable_port_list
        # 반송 조건 체크
        if loadable_port_list and unloadable_port_list:
            for load_port in loadable_port_list:
                for unload_port in unloadable_port_list:
                    # 아래 조건 충족시 반송 시작
                    if unload_port in load_port.UNLOAD_PORT:
                        # load_port에 따라서 분기
                        # 좌측 상단 3번 포트
                        if 340 <= load_port.NUM <= 363:
                            # 9,8 (대기 장소부터) 7~0 (가까운 충전/대기 장소부터)
                            for idx in range(9,-1,-1):
                                # AGV가 있고 충전 장소를 나오는 조건을 충족해 있다면
                                if wait_list[idx].using and wait_list[idx].using.status == 81:
                                    a_star_path = a_star(wait_list[idx].NUM, load_port.NUM, path_linked_list, node_list)
                                    vehicle_list[idx].command(a_star_path, 21)
                                    break
                        # # 좌측 하단 3번 포트
                        # elif 392 <= load_port.NUM <= 415:
                        # # 우측 상단 3번 포트
                        # elif 364 <= load_port.NUM <= 387:
                        # # 우측 하단 3번 포트
                        # elif 416 <= load_port.NUM <= 439:
                        # # 중앙 상단 1번 포트
                        # elif 388 <= load_port.NUM <= 391:
                        # # 중앙 하단 1번 포트
                        # elif 440 <= load_port.NUM <= 443: