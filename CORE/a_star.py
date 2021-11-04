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
    Q.put((0, start))
    cost[start-1] = 0
    found = False

    while not Q.empty():
        if found:
            break

        # Q.get() 하면 (우선순위, 노드) 이렇게 나온다.
        # 노드를 꺼낸다.
        current = Q.get()[1]
        if current == goal:
            found = True
        # current에서 갈 수 있는 노드마다
        for each_path in path_list[current-1]:
            # each_path는 (2, 20.5) 같은 형태
            next_node, next_cost = each_path
            # g = current까지 축적된 cost + 다음 노드로 가는 cost
            g = cost[current-1] + next_cost
            f = g + heuristic(next_node, goal, node_list)
            if f < cost[next_node-1]:
                Q.put((f, next_node))
                path[next_node-1] = current
                cost[next_node-1] = g

    final_path.append(goal)
    node = goal

    while node != start:
        nextNode = path[node-1]
        final_path.append(nextNode)
        node = nextNode

    final_path = final_path[::-1]
    print(final_path)