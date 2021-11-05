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
    
    # 시간으로 나타내고 싶어서 40으로 나눠주었다.
    return (abs(x1 - x2) + abs(y1 - y2)) / 40

def a_star(start, goal, path_list, node_list):

    # 노드 개수만큼 아주 큰 수를 넣어주었다.
    path = [1000000] * len(node_list)
    cost = [1000000] * len(node_list)

    final_path = []
    Q = PriorityQueue()
    
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
        # current에서 갈 수 있는 노드마다
        for each_path in path_list[current_node-1]:
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
                    print(current_node, "에서 회전")
                    g += 5
                elif node_list[current_node-1].X != node_list[previous_node-1].X and node_list[current_node-1].X == node_list[next_node-1].X:
                    print(current_node, "에서 회전")
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
    print(final_path)