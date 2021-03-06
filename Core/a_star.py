import threading
import time
from queue import PriorityQueue

# Manhattan distance와 Euclidean distance 중 Manhattan distance을 선택함
# 방식은 크게 중요하지 않다고 생각했음. 다만 Euclidean distance는 계산하는데 더 시간이 오래 걸릴 것 같아서
# Manhattan distance를 선택함
def heuristic(start, goal, node_list):
    # 출발점 절대 좌표
    x1 = node_list[start-1].X
    y1 = node_list[start-1].Y
    # 도착점 절대 좌표
    x2 = node_list[goal-1].X
    y2 = node_list[goal-1].Y
    
    # 맵의 특성을 고려하여 직선 경로가 있다면 직선으로 가도록 유도하기 위해서
    # heurisitc 값을 낮춰주었다.
    if x1 == x2 or y1 == y2:
        return 0
    else:
        return abs(x1 - x2) + abs(y1 - y2)


def a_star(start, goal, path_linked_list, node_list):    # 노드 개수만큼 아주 큰 수를 넣어주었다.
    path = [1000000] * len(node_list)
    cost = [1000000] * len(node_list)

    final_path = []
    Q = PriorityQueue()
    
    # 여기에 들어가있는 노드들은 동선 탐색에서 제외한다.
    # exclusion_list = []

    # Q.put((우선 순위, 노드))
    # 우선 순위에 cost를 넣겠다. 그러면 cost가 작은 노드부터 나올 것이다.
    Q.put((0, start, None))
    cost[start-1] = 0
    found = False

    while not Q.empty():
        if found:
            break

        # Q.get() 하면 (우선순위, 노드, 이전 노드) 이렇게 나온다.
        # 노드를 꺼낸다.
        # current_node = Q.get()[1]
        _, current_node, previous_node =Q.get()

        if current_node == goal:
            found = True

        # AGV 분산하기
        # if current_node in exclusion_list:
            # continue

        # current에서 갈 수 있는 노드마다
        for each_path in path_linked_list[current_node]:
            # each_path는 (2, 20.5) 같은 형태
            next_node, next_cost = each_path
            # g = current까지 축적된 cost + 다음 노드로 가는 cost
            g = cost[current_node-1] + next_cost

            # 회전을 하면 cost를 추가시키는 코드
            # 첫 시작점은 회전 체크를 하지 못하고 그 다음 노드부터 회전 체크를 한다.
            # angle과 좌표를 이용하면 첫 시작점도 회전하는지 알 수 있겠지만
            # 여러 상황을 고려해봤을 때 체크를 안 해도 무방하다고 판단했습니다.
            # 대기/충전 장소, 포트에서 나오는 경로가 딱 1개이기 때문에

            # 5초라서 일단 5를 더해주었다.
            if previous_node:
                if node_list[current_node-1].X == node_list[previous_node-1].X and node_list[current_node-1].X != node_list[next_node-1].X:
                    g += 5
                elif node_list[current_node-1].X != node_list[previous_node-1].X and node_list[current_node-1].X == node_list[next_node-1].X:
                    g += 5

            f = g + heuristic(next_node, goal, node_list)
            if f < cost[next_node-1]:
                # 우선순위 큐에 넣을 때는 h(x)가 포함된 값을 넣는다.
                Q.put((f, next_node, current_node))
                path[next_node-1] = current_node
                cost[next_node-1] = g

    final_path.append(goal)
    node = goal

    while node != start:
        nextNode = path[node-1]
        final_path.append(nextNode)
        node = nextNode

    final_path = final_path[::-1]
    final_path = final_path[1:]

    # AGV 분산하기
    # 분산 리스트를 하나 만들어서 여기에 들어있으면
    # for each_node in final_path:
    #     if each_node == 9:
    #         cost_thread = threading.Thread(target=control_cost, args=[each_node])
    #         cost_thread.start()

    return final_path

# def control_cost(each_node):
#     exclusion_list.append(each_node)
#     time.sleep(5)
#     exclusion_list.remove(each_node)