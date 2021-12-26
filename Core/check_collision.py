# 전형적인 물류공장 (짐을 싣고 내리는 포트가 촘촘하게 있고 반송의 안정성을 위해서 직선 경로 위주)
# 에서 동작하는 충돌방지 알고리즘
# 안전이 제일

# 일직선에서 충돌하는지 체크
def check_line_collision(agv1, agv2, stop_record, node_list):
    # x 좌표가 같은 경우
    if agv1.x == agv2.x:
        # 2m 이내라면 (시뮬 돌려보면서 값 조정)
        if abs(agv1.y-agv2.y) <= 2000:
            # 더 위쪽에 있는 AGV를 agv1로          
            if agv1.y > agv2.y:
                agv1, agv2 = agv2, agv1
            # 더 가까워지는 걸 막는다.
            # 위에 있는 1이 아래쪽을 향한다면 그리고 1이 움직인다면
            # 아래 있는 2가 멈춰있든 아래를 향하든 회전을 하든 1을 멈춘다.
            # 아래 있는 2가 1에게 직진하는 건 사전에 경로 선택할 때 막아야 한다.
            if agv1.angle == 180 and agv1.status == 20:
                # 4번 포트 근처에서 대기 중인 AGV 예외처리
                if agv2.status == 11:
                    return
                stop_record.append(agv1.NUM)
                agv1.emergency(1)
                return
            
            elif agv2.angle == 0 and agv2.status == 20:
                agv2.emergency(1)
                stop_record.append(agv2.NUM)
                return

    # y 좌표가 같은 경우
    elif agv1.y == agv2.y:
        if abs(agv1.x-agv2.x) <= 2000:
            # 더 오른쪽에 있는 AGV가 agv2
            if agv1.x > agv2.x:
                agv1, agv2 = agv2, agv1
            
            if agv1.angle == 90 and agv1.status == 20 and agv2.angle == 270 and agv2.status == 20 and agv1.path[0] == agv2.path[0]:
                # agv1이 더 먼 경우
                if abs(agv1.x - node_list[agv1.path[0]-1].X) >= abs(agv2.x - node_list[agv2.path[0]-1].X):
                    agv1.emergency(1)
                    stop_record.append(agv1.NUM)
                    return
                else:
                    agv2.emergency(1)
                    stop_record.append(agv2.NUM)
                    return
            
            # 왼쪽에 있는 1이 오른쪽을 향한다면 그리고 1이 움직인다면
            # 1을 멈춘다.
            elif agv1.angle == 90 and agv1.status == 20:
                agv1.emergency(1)
                stop_record.append(agv1.NUM)
                return
            elif agv2.angle == 270 and agv2.status == 20:
                if agv1.status == 11:
                    return
                agv2.emergency(1)
                stop_record.append(agv2.NUM)
                return

# 먼저 인자로 적힌 agv만 포트 또는 웨이팅 포트에서 후진해서 나오는 경우
def check_crossing_collision_back(agv1, agv2, stop_record):
    agv2_path_length = 5 if len(agv2.path) >= 5 else len(agv2.path)
    for idx in range(agv2_path_length):
        # 후진해서 나오니까 절대값 사용
        if abs(agv1.path[0]) == agv2.path[idx]:
            # 안 나오도록
            # 포트 근처 노드가 촘촘해서 지금 멈추면 아예 나오는 길을 막을 것 같다.
            # 아예 먼저 지나가도록 하겠다.
            if 0 <= idx <= 2:
                agv1.emergency(1)
                stop_record.append(agv1.NUM)
                return
            # 나오도록
            else:
                agv2.emergency(1)
                stop_record.append(agv2.NUM)
                return

# 일반적인 교차로에서
# agv1이 가로 주행, agv2가 세로 주행
def check_crossing_collision_normal(agv1, agv2, node_list, stop_record):
    # 두 AGV 모두 교차점에서 충분히 멀리 떨어져 있는 경우
    if abs(agv1.x - node_list[agv1.path[0]-1].X) >2000 and abs(agv2.y - node_list[agv1.path[0]-1].Y) < 2000:
        # 대기하러 가거나 충전하러 가는 경우라면 멈춘다.
        # 반송하는 중인 AGV에게 우선권 주기
        if agv1.cmd in [20, 23]:
            agv1.emergency(1)
            stop_record.append(agv1.NUM)
            return
        elif agv2.cmd in [20, 23]:
            agv2.emergency(1)
            stop_record.append(agv2.NUM)
            return
    elif abs(agv1.x - node_list[agv1.path[0]-1].X) < abs(agv2.y - node_list[agv1.path[0]-1].Y):
        # 더 멀리 떨어진 agv2를 멈춘다.
        agv2.emergency(1)
        stop_record.append(agv2.NUM)
        return
    else:
        agv1.emergency(1)
        stop_record.append(agv1.NUM)
        return

# 교차로에서 충돌하는지 체크
def check_crossing_collision(agv1, agv2, node_list, port_list, wait_list, path_linked_list, stop_record):
    stop_list = []
    
    if agv1.path and agv2.path:
        # 포트 또는 웨이팅 포인트에서 후진해서 나오는 경우
        # 연결된 link가 1개인 점을 이용한다.

        # 둘 다 포트 또는 웨이팅 포인트에서 후진해서 나오는 경우 => 제어할 필요 없다
        if len(path_linked_list[agv1.node]) == 1 and len(path_linked_list[agv2.node]) == 1:
            return
        # agv1만 포트 또는 웨이팅 포트에서 후진해서 나오는 경우
        elif len(path_linked_list[agv1.node]) == 1 and len(path_linked_list[agv2.node]) != 1:
            check_crossing_collision_back(agv1, agv2, stop_record)
            return
        # agv2만
        elif len(path_linked_list[agv2.node]) == 1 and len(path_linked_list[agv1.node]) != 1:
            check_crossing_collision_back(agv2, agv1, stop_record)
            return

        # 일반적인 교차로에서
        else:
            # 다음 목적지 노드가 같은 경우
            if agv1.path[0] == agv2.path[0]:
                # agv1이 가로 주행, agv2가 세로 주행
                if agv1.angle in [90, 270] and agv2.angle in [0, 180]:
                    check_crossing_collision_normal(agv1, agv2, node_list, stop_record)
                # agv1이 세로 주행, agv2가 가로 주행
                elif agv1.angle in [0, 180] and agv2.angle in [90, 270]:
                    check_crossing_collision_normal(agv2, agv1, node_list, stop_record)

def check_collision(node_list, port_list, wait_list, vehicle_list, path_linked_list):
    stop_record = []

    check_list = []
    for vehicle in vehicle_list:
        # 초기 상태, 대기, 충전소 근처 대기, 이동 중
        if vehicle.status in [0, 10, 11, 20]:
            check_list.append(vehicle)
    
    for idx1 in range(len(check_list)):
        for idx2 in range(idx1+1, len(check_list)):
            # 교차로 제어
            if check_list[idx1].x != check_list[idx2].x and check_list[idx1].y != check_list[idx2].y:
                if check_list[idx1].status == 20 and check_list[idx2].status == 20:
                    check_crossing_collision(check_list[idx1], check_list[idx2], node_list, port_list, wait_list, path_linked_list, stop_record)
            # 직선 제어
            else:
                check_line_collision(check_list[idx1], check_list[idx2], stop_record, node_list)

    # 멈춘 AGV 동작을 재개시키는 로직
    for vehicle in vehicle_list:
        if vehicle.interrupt == 1:
            if vehicle.NUM not in stop_record:
                vehicle.emergency(0)