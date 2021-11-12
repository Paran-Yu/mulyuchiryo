class AStar():
    def __init__(self, env):
        # Vehicle 정보: 시작위치(현재위치) - 노드 번호
        self.agent_dict = env.agent_dict
        # 노드 번호 -> 좌표값 -> 휴리스틱 계산
        self.admissible_heuristic = env.admissible_heuristic
        # 목적지 도착 여부
        self.is_at_goal = env.is_at_goal
        # 이웃 정보 가져오기
        self.get_neighbors = env.get_neighbors

    #목적지 찾은 후, 경로 return (노드)
    def reconstruct_path(self, came_from, current):
        total_path = [current]
        while current in came_from.keys():
            current = came_from[current]
            total_path.append(current)
        return total_path[::-1]

    def search(self, agent_name):
        """
        low level search 
        """

        initial_state = self.agent_dict[agent_name]["start"]
        step_cost = 1
        
        closed_set = set()          # 갈 수 없는
        open_set = {initial_state}  # 갈 수 있는

        came_from = {}              # 왔던 거리

        g_score = {} 
        g_score[initial_state] = 0  # 현재 노드에서 출발지까지 총 cost

        f_score = {}                # 출발지에서 목적지까지의 총 cost

        # 시작위치와 현재(목적지) 위치의 휴리스틱 계산
        f_score[initial_state] = self.admissible_heuristic(initial_state, agent_name)

        # 갈 수 있는 위치
        while open_set:
            temp_dict = {open_item:f_score.setdefault(open_item, float("inf")) for open_item in open_set}
            current = min(temp_dict, key=temp_dict.get)

            # 목적지 도착 -> 경로 return
            if self.is_at_goal(current, agent_name):
                return self.reconstruct_path(came_from, current)


            open_set -= {current}
            closed_set |= {current}
            
            # 이웃 충돌 제어
            neighbor_list = self.get_neighbors(current)

            for neighbor in neighbor_list:
                if neighbor in closed_set:
                    continue
                
                tentative_g_score = g_score.setdefault(current, float("inf")) + step_cost

                if neighbor not in open_set:
                    open_set |= {neighbor}
                elif tentative_g_score >= g_score.setdefault(neighbor, float("inf")):
                    continue

                came_from[neighbor] = current

                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + self.admissible_heuristic(neighbor, agent_name)
        return False
