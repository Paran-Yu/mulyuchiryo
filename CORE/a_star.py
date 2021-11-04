from queue import PriorityQueue

# Manhattan distance와 Euclidean distance 중 Manhattan distance을 선택함
# 방식은 크게 중요하지 않다고 생각했음. 다만 Euclidean distance는 계산하는데 더 시간이 오래 걸릴 것 같아서
# Manhattan distance를 선택함
def heuristic(start, goal):
    # 출발점 절대 좌표
    x1 = start.x
    y1 = start.y
    # 도착점 절대 좌표
    x2 = goal.X
    y2 = goal.y
    
    return abs(x1 - x2) + abs(y1 - y2)

def a_star(start):

    # 수정해야 한다.
    path = []
    cost = []

    Q = PriorityQueue()
    # Q.put((우선 순위, 좌표))
    # 우선 순위에 비용을 넣겠다. 그러면 비용이 작은 좌표부터 나올 것이다.
    Q.put((0, start))
    cost[start[0]][start[1]] = 0
    found = False

    while not Q.empty():
        if found:
            break

        # Q.get() 하면 (우선순위, [ , ]) 이렇게 나온다.
        # 좌표를 꺼낸다.
        current = Q.get()[1]
        if current == goal:
            found = True