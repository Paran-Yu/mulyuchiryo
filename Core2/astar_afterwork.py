from heapq import heappush, heappop
import numpy as np

'''
    # 고려 1
# Vehicle 종류별로 존재할 것: Vehicle class
# 충돌방지를 위해서는 동선탐색도 class로 만들어야할까?
# Vehicle마다 size가 다름, 이웃 Vehicle과의 충돌방지를 위해서 경계를 각각 계산하기 위함
# class생성? 일단, 함수로 작성
'''

# 행렬의 노름으로 계산: 노름(행렬에 대한 기준 제시, 다른 행렬이나 벡터에 연산을 했을 때 해당 행렬이나 벡터가 미치는 영향력)
# Manhattan distance, 상하좌우 4방향으로 움직이기 때문
def h(start, goal, node_list):
    # 출발점 절대 좌표
    start_pos = [node_list[start-1].X, node_list[start-1].Y]
    # 도착점 절대 좌표
    goal_pos = [node_list[goal-1].X, node_list[goal-1].Y]
    
    # L1 norm
    # 모든 원소에 절댓값을 취한 후, 같은 열의 모든 행의 합을 구한 후 구한 합 중 최댓값을 고른다는 것
    return int(np.linalg.norm(start_pos-goal_pos, 1))  # L1 norm

# 이웃하는 AGV와의 거리를 구하기 위함
def l2(start, goal, node_list):
    # 출발점 절대 좌표
    start_pos = [node_list[start-1].X, node_list[start-1].Y]
    # 도착점 절대 좌표
    goal_pos = [node_list[goal-1].X, node_list[goal-1].Y]

    # L2 norm
    # 행렬 원소의 모든 값들의 제곱 합에 루트를 씌운 것, 즉 좌표계에서 두 점 사이의 거리
    return int(np.linalg.norm(start_pos-goal_pos, 2))  # L2 norm


'''
    고려 2
# 이동할때, 갈수없는 곳에 대한 연산이 필요할까? 
# Check the nearest static obtacles
'''


'''
    Space-Time A*
'''
def search(start, goal, path_list, node_list, dynamic_obstacles, robot_size):
    # Prepare dynamic obstacles
    dynamic_obstacles = dict((k, np.array(list(v))) for k, v in dynamic_obstacles.items())
    # Assume dynamic obstacles are agents with same radius, distance needs to be 2*radius
    def safe_dynamic(grid_pos, time) -> bool:
        nonlocal dynamic_obstacles
        return all(l2(grid_pos, obstacle) > robot_size for obstacle in dynamic_obstacles.setdefault(time, np.array([])))

    # 출발점 절대 좌표
    start_pos = [node_list[start-1].X, node_list[start-1].Y]
    # 도착점 절대 좌표
    goal_pos = [node_list[goal-1].X, node_list[goal-1].Y]
    