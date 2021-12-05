## 1. 알고리즘 개요

AGV(Automated Guided Vehicle)를 이용해서 최단 시간 안에 물건을 싣고 배송하는 걸 목표로 함. 이를 위해서 가장 빠른 경로를 찾는 것이 중요하다. AGV의 이동은 크게 3가지다. <br>

- 대기를 하거나 충전을 하는 장소에 있는 AGV를 Load port로 보내서 짐을 싣기
- Load port에서 짐을 실은 AGV를 짐을 내리는 Unload port로 보내서 짐을 내리기
- 짐을 내린 AGV를 대기를 하거나 충전을 하는 장소로 복귀시키기

멘토님 설명 : 목표 달성을 위해서는 짐을 싣거나 내리러 가는 로직이 가장 중요하고 복귀시킬 때는 조금 늦게 복귀시켜도 된다. <br>

각각의 로직은 call_agv.py, send_agv.py, back_agv.py에서 작성했다. 맵에 따라서 로직을 수정해주어야 한다. <br>

배터리 잔량에 따른 충전 규칙은 다음과 같다. <br>

- 80% ~ 60% : 반송 없을 시, 충전 Job 할당 가능
- 60% > : 충전 Job 만 할당 가능
- 1회 충전 시, 최소 10% or 5분 충전이 필수이며 배터리 잔량이 60%보다 많을 때만 충전 Job 종료할 수 있다. 
- 두시간 충전에 완충, 동작 시 : -1%/min, 대기 시 : -1%/5min

<br>

## 2. 최단 경로 찾기 알고리즘

1. Dijkstra

![다익스트라](README.assets/dijkstra.gif)

2. A*

![astar](README.assets/astar.gif)

- F(x) = G(x)+H(x)
    - G(x): 출발지점에서 현재 노드까지의 총 Cost
    - H(x): Heuristic(휴리스틱), 현재노드에서 목적지까지의 추정거리

<br>

3. 추가적으로 알아본 자료 (카카오맵이 빠르게 길을 찾아주는 방법: CCH를 이용한 개편기)

   https://tech.kakao.com/2021/05/10/kakaomap-cch/

<br>

이번 프로젝트에서는 장애물이 없어서 멀리 돌아가는 경로가 없기 때문에 <br>

A* 알고리즘이 Dijkstra 알고리즘보다 더 빠르게 경로를 탐색할 수 있다고 판단함 <br>

<br>

## 3. 전략

![control](README.assets/control.png)

- AGV가 짐을 내려놓을 포트를 A* 알고리즘으로만 찾으면, 여러 대의 AGV가 한 곳의 포트로 향하고 한 AGV만 짐을 내려놓을 수 있다.
- 추가적으로 경로를 찾고 난 이후에 짐을 내려놓을 수 있는 더 가까운 Unload 포트가 생길 수 있다.

![bandicam 2021-12-06 02-00-28-343.mp4_20211206_020124](README.assets/bandicam 2021-12-06 02-00-28-343.mp4_20211206_020124.gif)

- 이 점을 해결하기 위해서  Unload 포트와 가까운 위치에서 다시 한 번 가장 가까운 Unload 포트를 탐색하고 가장 가까운 Unload 포트로 AGV를 보낸다.

<br>

![bandicam 2021-12-06 02-08-45-922.mp4_20211206_021032](README.assets/bandicam 2021-12-06 02-08-45-922.mp4_20211206_021032.gif)

- 3번 포트에서 짐을 싣고 4번 포트로 짐을 내릴 때 4번 포트는 2개의 포트밖에 없기 때문에 정체가 필연적으로 발생한다. 그래서 4번 포트로 가기 전에 대기 장소를 지정해서 대기 장소로 먼저 가게 했다. 대기 장소에서 Unload 포트가 이용가능한지 판단하고 이용 가능할 때만 짐을 내리게 된다.

- Unload port에 물건을 한 번 내리면 주어진 시간 동안 물건을 내릴 수 없다. AGV들은 대기 장소에서 대기하다가 Unload port에 물건을 내릴 수 있게 되면 Unload 포트로 이동하고 물건을 내린다.

<br>

```python
def control_cost(each_node):
    exclusion_list.append(each_node)
    time.sleep(5)
    exclusion_list.remove(each_node)
```

- 시뮬레이션을 한 번 돌린 후 통계 자료를 통해서 정체가 많이 일어나는 노드를 확인할 수 있는데 A* 알고리즘을 작성할 때 exclusion_list를 만들어 정체를 피하려는 기획을 했습니다. 정체가 많이 일어나는 노드가 한 번 경로에 들어가면 thread를 이용해서 5초 동안 그 노드를 exclusion_list에 넣습니다. 그러면 5초 동안 A*를 이용해서 경로를 탐색할 때는 그 노드를 제외하고 경로를 탐색하게 됩니다.
- 시뮬레이션을 돌려보고 결과를 확인한 후에 이 함수를 이용해서 정체를 줄일 수 있습니다.

<br>

## 4. 충돌제어

AGV들은 이동하면서 충돌을 할 수 있기 때문에 이를 방지하기 위한 알고리즘이 필요합니다. 직선 경로와 교차로에서 일어나는 충돌을 제어할 수 있는 로직을 check_collision.py에 작성했습니다. 멘토님과 이야기하면서 물류 공장의 전형적인 특징에 대해서 알게 되었습니다. 물건을 싣거나 내리는 port는 촘촘하게 몰려있는 경우가 많고 물건을 반송할 때 안정성을 위해서 직선 경로를 주로 이동합니다. 그래서 이 충돌제어 알고리즘은 전형적인 물류 공장 지도에서 동작하는 알고리즘입니다.

### 4-1. 직선 경로 충돌 제어

두 AGV의 x 좌표 혹은 y좌표가 동일하다면 직선 경로 충돌 제어 로직을 실행했습니다. <br>

Vehicle class의 angle (향하는 방향)과 x,y 좌표 (절대 좌표, 지도의 좌측 최상단이 0,0)를 이용해서 AGV가 특정 거리보다 가까워지지 않게 만들어서 충돌을 방지했습니다.

### 4-2. 예시

![bandicam 2021-12-06 00-23-19-451.mp4_20211206_002554](README.assets/bandicam 2021-12-06 00-23-19-451.mp4_20211206_002554.gif)

- 짐을 내려놓고 나오는 AGV 들의 직선 경로 충돌 제어

![bandicam 2021-12-06 01-43-45-250.mp4_20211206_014440](README.assets/bandicam 2021-12-06 01-43-45-250.mp4_20211206_014440.gif)

### 4-3. 교차로 충돌 제어

두 AGV의 x 좌표와 y좌표가 다르다면 교차로에서 만나는지 확인하고 만난다면 교차로 충돌 제어 로직을 실행했습니다. <br>

Vehicle class의 node와 path 그리고 x,y 좌표를 이용했습니다. node에는 가장 최근에 지나온 node 혹은 현재 위치한 node를 저장합니다. path는 앞으로 가게 되는 node들의 NUM이 list에 담겨 있습니다.

### 4-4. 예시

![bandicam 2021-12-06 00-05-24-816.mp4_20211206_000706](README.assets/bandicam 2021-12-06 00-05-24-816.mp4_20211206_000706.gif)

- 파란색 사각형은 AGV를 나타내고 삼각형이 빨간색으로 칠해졌다면 짐을 실은 AGV를 나타냅니다.
- 영상에서 아래로 내려오는 AGV는 짐을 내려놓고 복귀하는 AGV입니다.
- 교차로에서 충돌을 방지하기 위해서 한 AGV를 멈춰야 하는데 두 AGV 모두 교차로까지 거리가 충분히 멀었기 때문에 짐을 실은 AGV가 먼저 지나가도록 로직을 작성했습니다.
- AGV가 한 번 멈춰서 양보를 했다면 그 다음에는 우선적으로 교차로를 먼저 지나가게 해달라는 멘토님의 요구 사항에 따라서 짐을 실은 AGV가 연달아서 오지만 이때는 짐을 실은 AGV가 멈추게 됩니다.
- 위 예시와 다르게 짐을 실은 AGV가 교차로에서 멀리 떨어져있고 복귀하는 AGV가 교차로와 가까이 있다면 짐을 실은 AGV를 멈추었습니다. 복귀하는 AGV를 멈추게 될 경우 교차로에 정차를 할 가능성이 있기 때문입니다. 이 경우 짐을 실은 AGV는 교차로를 지나갈 수 없습니다.

![bandicam 2021-12-06 02-28-42-978.mp4_20211206_023142](README.assets/bandicam 2021-12-06 02-28-42-978.mp4_20211206_023142.gif)

- Load 포트에서 짐을 다 실어서 삼각형이 빨간색으로 바뀌고 목적지를 나타내는 검은색 선도 생겼지만 충돌을 방지하기 위해서 가로로 이동하는 AGV가 지나간 후 움직이는 AGV의 모습입니다.
- 짐을 싣거나 내리는 포트들은 촘촘하게 몰려있어서 기존의 교차로 충돌 방지 로직으로는 충돌을 방지할 수 없었고 예외처리를 해주었습니다.
- 짐을 싣거나 내리는 포트를 나타내는 노드는 edge가 1개 밖에 없다는 점을 이용해서 코드를 작성했습니다.

### 4-5. 동작 재개 로직

멈춘 AGV를 다시 동작시키기 위한 로직을 설명하겠습니다.

```python
# AGV를 다시 동작하게 하는 명령
vehicle.emergency(0)
# AGV를 멈추는 명령
vehicle.emergency(1)
```

Core에서 vehicle.emergency(1) 명령을 내리면 Vehicle instance의 interrupt 변수가 1로 바뀝니다. 또한 이 명령을 내릴 때 stop_record 라는 이름의 list에 vehicle instance의 NUM을 기록합니다. vehicle instance가 멈춰있는데(vehicle.interrput == 1) Core 로직을 돌면서 AGV를 멈추라는 명령을 받지 않았다면 동작을 재개합니다.

```python
for vehicle in vehicle_list:
    if vehicle.interrupt == 1:
        if vehicle.NUM not in stop_record:
            vehicle.emergency(0)
```

<br>

## 5. 참고 자료

### 5-1. 알고리즘

1. mvpf (Multi Vehicle Path Finding) 
   
    ![mapf](README.assets/mapf.gif)
    
    1. 충돌 기반 검색(CBS) 및 시공간 A*(STA*)을 사용한 MAPF(익명 다중 에이전트 경로 찾기)
    2. 각 AGV들의 시작 위치와 목표 위치를 가진 리스트를 Input으로 사용하여 충돌을 피하며 모든 AGV들의 경로를 찾는 것
2. Space-Time A*
    1. 동적 장애물을 처리하기 위한 추가 시간 차원이 있는 시공간 A*(STA*) 검색 알고리즘
3. cbs (Conflict based Search) - 제일 많이 참고한 내용
    1. 충돌 기반 검색을 기반으로 한 최적의 다중 Vehicle 경로 찾기 알고리즘
    2. A* 알고리즘보다 빠르다.
        1. 충돌 트리(CT)에서 검색이 수행됩니다. CT의 각 노드는 에이전트의 움직임에 대한 일련의 제약 조건을 나타냅니다. 낮은 수준에서 고속 단일 에이전트 검색이 수행되어 높은 수준의 CT 노드에 의해 부과된 제약 조건을 충족한다. 대부분의 경우 CBS는 이러한 2단계 공식을 통해 최적성을 유지하면서 A*보다 적은 수의 상태를 검사할 수 있습니다.

### 5-2. 논문

1. Multi-agent Pathfinding Based on Improved Cooperative A* in Kiva System(2019)

[https://s3.us-west-2.amazonaws.com/secure.notion-static.com/ff155da1-6bae-4829-bbd3-00de5ea5d36c/ICCAR.2019.8813319.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20211116%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20211116T074019Z&X-Amz-Expires=86400&X-Amz-Signature=6c9fa7cd528d66fcdd782a4c6f6a87a12006ee8446a84a85e7012a73c61691ad&X-Amz-SignedHeaders=host&response-content-disposition=filename %3D"ICCAR.2019.8813319.pdf"](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/ff155da1-6bae-4829-bbd3-00de5ea5d36c/ICCAR.2019.8813319.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20211116%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20211116T074019Z&X-Amz-Expires=86400&X-Amz-Signature=6c9fa7cd528d66fcdd782a4c6f6a87a12006ee8446a84a85e7012a73c61691ad&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22ICCAR.2019.8813319.pdf%22)

2. Multi-vehicle motion planning for social optimal mobility-on-demand

[https://s3.us-west-2.amazonaws.com/secure.notion-static.com/03c6f7f0-9b0d-447d-ba5e-196a1f27f6be/ICRA_2018.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20211116%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20211116T074124Z&X-Amz-Expires=86400&X-Amz-Signature=128951eaa1b29a21a6f0e087cc19f5b244e732ddafe5b9dae6c8c5fead2f3494&X-Amz-SignedHeaders=host&response-content-disposition=filename %3D"ICRA_2018.pdf"](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/03c6f7f0-9b0d-447d-ba5e-196a1f27f6be/ICRA_2018.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20211116%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20211116T074124Z&X-Amz-Expires=86400&X-Amz-Signature=128951eaa1b29a21a6f0e087cc19f5b244e732ddafe5b9dae6c8c5fead2f3494&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22ICRA_2018.pdf%22)

### 5-3. 참고 개념

1. A* 알고리즘 이해
[https://seokdev.site/210](https://seokdev.site/210)

2. MIT: Multi Agent Path Finding 

[https://github.com/GavinPHR/Multi-Agent-Path-Finding](https://github.com/GavinPHR/Multi-Agent-Path-Finding)

3. MIT: Space-Time A*

[https://github.com/GavinPHR/Space-Time-AStar](https://github.com/GavinPHR/Space-Time-AStar)