# 충돌제어를 위한 최적의 경로 찾기 알고리즘
> Core 폴더 알고리즘 참고 개념 정리

## 1. 최단 경로 찾기

A*: A* 는 **시작점이 정해지고, 목표점이 정해지면 두개의 최단 거리**를 구한다.

### 다익스트라 vs A*

1. 다익스트라

![다익스트라](../docs/다익스트라.gif)

2. A*

![astar](README.assets/astar.gif)

- F(x) = G(x)+H(x)
    - 알고리즘의 핵심 값인 F,G,H
        - F: 출발지점에서 목적지까지의 총 Cost 합
        - G: 현재 노드에서 출발지점까지의 총 Cost
        - H: Heuristic(휴리스틱), 현재노드에서 목적지까지의 추정거리 (핵심 부분)
- F값은 현재 노드가 목적지에 도달하는 데 있어서, 최선의 방법인지 확인할 수 있는 값
    - F값이 없으면 다익스트라 알고리즘처럼 모든 노드에서 목적지까지 가는 방법을 찾는다

## 2. 충돌제어

→ 이웃하는 AGV들과의 충돌을 방지하기 위함

→ 겹치는 경로와 노드를 비교하여 경로를 탐색, 충돌 위험이 있는 경로는 재탐색

- 충돌제어에 참고한 충돌방지 알고리즘 개념
    - A*의 heuristic 탐색 알고리즘의 변형
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

### 참고 논문

1. Multi-agent Pathfinding Based on Improved Cooperative A* in Kiva System(2019)

[https://s3.us-west-2.amazonaws.com/secure.notion-static.com/ff155da1-6bae-4829-bbd3-00de5ea5d36c/ICCAR.2019.8813319.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20211116%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20211116T074019Z&X-Amz-Expires=86400&X-Amz-Signature=6c9fa7cd528d66fcdd782a4c6f6a87a12006ee8446a84a85e7012a73c61691ad&X-Amz-SignedHeaders=host&response-content-disposition=filename %3D"ICCAR.2019.8813319.pdf"](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/ff155da1-6bae-4829-bbd3-00de5ea5d36c/ICCAR.2019.8813319.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20211116%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20211116T074019Z&X-Amz-Expires=86400&X-Amz-Signature=6c9fa7cd528d66fcdd782a4c6f6a87a12006ee8446a84a85e7012a73c61691ad&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22ICCAR.2019.8813319.pdf%22)

2. Multi-vehicle motion planning for social optimal mobility-on-demand

[https://s3.us-west-2.amazonaws.com/secure.notion-static.com/03c6f7f0-9b0d-447d-ba5e-196a1f27f6be/ICRA_2018.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20211116%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20211116T074124Z&X-Amz-Expires=86400&X-Amz-Signature=128951eaa1b29a21a6f0e087cc19f5b244e732ddafe5b9dae6c8c5fead2f3494&X-Amz-SignedHeaders=host&response-content-disposition=filename %3D"ICRA_2018.pdf"](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/03c6f7f0-9b0d-447d-ba5e-196a1f27f6be/ICRA_2018.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20211116%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20211116T074124Z&X-Amz-Expires=86400&X-Amz-Signature=128951eaa1b29a21a6f0e087cc19f5b244e732ddafe5b9dae6c8c5fead2f3494&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22ICRA_2018.pdf%22)

### 참고 개념 and code

1. A* 알고리즘 이해
[https://seokdev.site/210](https://seokdev.site/210)

2. MIT: Multi Agent Path Finding 

[https://github.com/GavinPHR/Multi-Agent-Path-Finding](https://github.com/GavinPHR/Multi-Agent-Path-Finding)

3. MIT: Space-Time A*

[https://github.com/GavinPHR/Space-Time-AStar](https://github.com/GavinPHR/Space-Time-AStar)