# 충돌 방지 알고리즘
# 안전이 제일

# 일직선에서 충돌하는지 체크
def check_line_collision(agv1, agv2, stop_record):
    # x 좌표가 같은 경우
    if agv1.x == agv2.x:
        # 2m50cm 이내라면 (시뮬 돌려보면서 값 조정 예정)
        if abs(agv1.y-agv2.y) <= 2500:
            # 더 아래쪽에 있는 AGV가 agv1          
            if agv1.y > agv2.y:
                agv1, agv2 = agv2, agv1

            # 더 가까워지는 걸 막는다.

            # 위에 있는 1이 아래쪽을 향한다면 그리고 1이 움직인다면
            # 아래 있는 2가 멈춰있든 아래를 향하든 회전을 하든 1을 멈춘다.
            # 아래 있는 2가 1에게 직진하는 건 사전에 경로 선택할 때 막아야 한다.
            if agv1.angle == 180 and agv1.status == 20:
                if agv2.status == 11:
                    return
                # print("멈춰1-1", agv1.NUM)
                stop_record.append(agv1.NUM)
                agv1.emergency(1)
                return
            
            if agv2.angle == 0 and agv2.status == 20:
                agv2.emergency(1)
                stop_record.append(agv2.NUM)
                # print("멈춰1-2", agv2.NUM)
                return

    # y 좌표가 같은 경우
    elif agv1.y == agv2.y:
        if abs(agv1.x-agv2.x) <= 2500:
            # 더 오른쪽에 있는 AGV가 agv2
            if agv1.x > agv2.x:
                agv1, agv2 = agv2, agv1
            
            # 왼쪽에 있는 1이 오른쪽을 향한다면 그리고 1이 움직인다면
            # 1을 멈춘다.
            if agv1.angle == 90 and agv1.status == 20:
                agv1.emergency(1)
                stop_record.append(agv1.NUM)
                # print("멈춰2-1", agv1.NUM)
                return
            if agv2.angle == 270 and agv2.status == 20:
                if agv1.status == 11:
                    return
                agv2.emergency(1)
                stop_record.append(agv2.NUM)
                # print("멈춰2-2", agv2.NUM)
                return

# 교차로에서 충돌하는지 체크
def check_crossing_collision(agv1, agv2, node_list, port_list, wait_list, path_linked_list, stop_record):
    agv2_path_length = 5 if len(agv2.path) >= 5 else len(agv2.path)
    stop_list = []
    
    if agv1.path and agv2.path:
        # 포트에서 후진해서 나오는 경우
        if node_list[agv1.node-1] in port_list or node_list[agv1.node-1] in wait_list:
            # 직선 경로에 있는 웨이트 포인트는 뺀다.
            if len(path_linked_list[agv1.node]) == 1:
                # 포트에서 나오는 경우는 제외
                if node_list[agv2.node-1] not in port_list and node_list[agv2.node-1] not in wait_list:
                    for idx in range(agv2_path_length):
                        if abs(agv1.path[0]) == agv2.path[idx]:
                            # 안 나오도록
                            # 포트 근처 노드가 촘촘해서 지금 멈추면 아예 나오는 길을 막을 것 같다.
                            # 아예 먼저 지나가도록 하면 어떨까 싶었다.
                            if 0 <= idx <= 2:
                                agv1.emergency(1)
                                stop_record.append(agv1.NUM)
                                print(agv1.NUM," 이 후진하는데 후진 멈출게", agv2.NUM, "넌 지나가")
                                return
                            # 나오도록
                            else:
                                agv2.emergency(1)
                                stop_record.append(agv2.NUM)
                                print(agv2.NUM, "너가 멈춰 ", agv1.NUM, "이 후진하니까")
                                return

        # 일반적인 교차로에서
        # agv1이 오른쪽 주행, agv2가 세로 주행
        if agv1.angle in [90, 270] and agv2.angle in [0, 180]:
            # path[0]만 비교
            # 다음 목적지 노드가 같음
            if agv1.path[0] == agv2.path[0]:
                # 떨어진 거리 비교
                if abs(agv1.x - node_list[agv1.path[0]-1].X) < abs(agv2.y - node_list[agv1.path[0]-1].Y):
                    # 더 멀리 떨어진 agv2를 멈춘다.
                    agv2.emergency(1)
                    stop_record.append(agv2.NUM)
                    print("멈춰2-1", agv2.NUM)
                    return
                else:
                    agv1.emergency(1)
                    stop_record.append(agv1.NUM)
                    print("멈춰2-1", agv1.NUM)
                    return

        # 중앙 load 포트 근처 충돌 방지
        # agv1이 짐 싣고 나오고 agv2가 세로 주행
        if node_list[agv1.node-1] in port_list and agv2.angle in [0, 180]:
            if agv1.path[0] == agv2.path[0] or agv1.path[1] == agv2.path[0]:
                agv2.emergency(1)
                stop_record.append(agv2.NUM)
                print("멈춰3-1", agv2.NUM)
                return

def check_collision(node_list, port_list, wait_list, vehicle_list, path_linked_list):
    stop_record = []

    check_list = []
    for vehicle in vehicle_list:
        # 초기 상태, 대기, 충전소 근처 대기, 
        if vehicle.status in [0, 10, 11, 20]:
            check_list.append(vehicle)
    
    for idx1 in range(len(check_list)):
        for idx2 in range(len(check_list)):
            if idx1 != idx2:
                # 교차로 제어
                if check_list[idx1].x != check_list[idx2].x and check_list[idx1].y != check_list[idx2].y:
                    if check_list[idx1].status == 20 and check_list[idx2].status == 20:
                        check_crossing_collision(check_list[idx1], check_list[idx2], node_list, port_list, wait_list, path_linked_list, stop_record)
                # 직선 제어
                else:
                    check_line_collision(check_list[idx1], check_list[idx2], stop_record)

    # 멈춘 AGV 동작을 재개시키는 로직
    for vehicle in vehicle_list:
        if vehicle.interrupt == 1:
            if vehicle.NUM not in stop_record:
                vehicle.emergency(0)