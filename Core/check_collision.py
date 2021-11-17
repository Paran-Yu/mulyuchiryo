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
                print("멈춰1-1", agv1.NUM)
                stop_record.append(agv1.NUM)
                agv1.emergency(1)
                return
            
            if agv2.angle == 0 and agv2.status == 20:
                agv2.emergency(1)
                stop_record.append(agv2.NUM)
                print("멈춰1-2", agv2.NUM)
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
                print("멈춰2-1", agv1.NUM)
                return
            if agv2.angle == 270 and agv2.status == 20:
                if agv1.status == 11:
                    return
                agv2.emergency(1)
                stop_record.append(agv2.NUM)
                print("멈춰2-2", agv2.NUM)
                return

# 교차로에서 충돌하는지 체크
def check_crossing_collision(agv1, agv2, node_list, path_linked_list, port_list, stop_record):
    # agv1_path_length = 5 if len(agv1.path) >= 5 else len(agv1.path)
    stop_list = []
    
    if agv1.path:
        # 다음 노드가 교차로? 교차로의 주변 노드 확인  
        if node_list[agv1.path[0]-1].isCross: 
            for node, _ in path_linked_list[agv1.path[0]-1]: # 교차로 노드가 갈 수 있는 길
                if node_list[node-1].X != agv1.x and node_list[node-1].Y != agv2.y:
                    print("현재 노드와 교차로 사이의 주변 노드:",node)
                    stop_list.append(node)
            stop_list.append(agv1.path[0])
            
                # 두 AGV가 동시에 교차로에 진입해서 둘 다 멈추는 걸 방지
                # AGV1이 먼저 이동
                # 이 코드의 수정이 필요해 보임
            if agv1.NUM not in stop_record:
                for stop_node in stop_list:
                    if agv2.path and stop_node == agv2.path[0]:
                        agv2.emergency(1)
                        stop_record.append(agv2.NUM)
                        print("멈춰3-1", agv2.NUM)

        # 포트에서 후진해서 나오는 경우
        # 현재 agv1의 노드가 port일 때
        if agv1.node in port_list:
            for idx in range(5):
                if abs(agv1.node == agv2.path[idx]):
                    if idx > 2:
                        agv1.emergency(1)
                        stop_record.append(agv1.NUM)
                        print("멈춰3-2", agv1.NUM)
                    else:
                        agv2.emergency(1)
                        stop_record.append(agv2.NUM)
                        print("멈춰3-2 너가 멈춰", agv2.NUM)


def check_collision(node_list, vehicle_list, path_linked_list, port_list):
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
                    if vehicle.status  == 20:
                        check_crossing_collision(check_list[idx1], check_list[idx2], node_list, path_linked_list, port_list, stop_record)
                        pass
                # 직선 제어
                else:
                    check_line_collision(check_list[idx1], check_list[idx2], stop_record)

    # 멈춘 AGV 동작을 재개시키는 로직
    for vehicle in vehicle_list:
        if vehicle.interrupt == 1:
            if vehicle.NUM not in stop_record:
                vehicle.emergency(0)