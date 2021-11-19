# UI Tools

## How To

### CMD 환경 실행
pip를 이용해서 주요 모듈들을 설치합니다.
```shell
pip install -r requirements.txt
```
UI/main.py 파일을 실행합니다.
```shell
cd $PJT_DIR/UI
python main.py
```
혹은 사용하는 IDE 툴을 이용해 실행할 수도 있습니다. \
<img src="/uploads/da018b2421624cb54b8b704c2aecea65/image.png" Width="50%" height="50%"> \
파이참에서 [File] - [Settings] 메뉴에 들어가 [Project: {PJT NAME}] 탭의 [Python Interpreter] 메뉴에서 모듈을 직접 설치하고 run 하여 실행할 수 있습니다.

### exe를 이용한 실행
pyinstaller를 이용해 프로젝트를 하나의 exe 파일로 압축할 수 있습니다.
```shell
## 옵션 설명
#  --onefile, -F: 하나의 실행파일로 생성
#  --n: exe파일명 지정
#  --noconsole, -w: exe 파일 실행 시 콘솔창 생성을 막아줌
#  --icon=: 실행파일의 아이콘 이미지 지정. ico 확장자만 가능.
pyinstaller -F main.py -w
```

## 소개
물류치료의 `UI Tools`는 동선을 계산하는 핵심 로직인 Core에 명령과 데이터를 전달하고, 실행 결과에 대한 보고서를 사용자가 쉽게 알아볼 수 있도록 표현해주는 GUI 프로그램입니다.

> <img src="/uploads/30610939f8a3ddf161ec2297ca8282f9/image.png">

AGV가 다니는 동선을 마우스를 이용해서 쉽게 그리고, AGV와 주변의 지형, 목적지 포트 및 대기장소를 추가 / 제거하고 구성하여 가상 환경에서 시연할 수 있고, 이에대한 결과치를 가시화하여 사용자가 AGV들의 동선을 쉽게 계산하고 지정할 수 있도록 도와주는 것을 목표로 합니다.

## 주요 기능

### 파일 관리
- 공장 내부도를 불러오고 Width 실측값 입력으로 픽셀당 거리를 계산.
- 직렬화를 이용해 작업한 레이아웃 데이터를 저장하고 불러와서 다음에 다시 이용할 수 있음
- Core 측에서 전달받은 데이터를 엑셀 파일로 저장.

### 드로잉
- 객체: 마우스 클릭을 이용해 포트, 대기장소, 기기 등을 원하는 위치에 추가함.
- 동선: 마우스를 이용해 원하는 위치에 동선을 그리고, 이를 계산된 거리와 비교하여 적절한 값으로 교체함.


### 세부 설정
- 객체 클릭 시 생성되는 창에 세부 데이터를 입력 가능.
- 입력 가능한 내부 데이터([Issue #3](https://lab.ssafy.com/s05-final/S05P31F006/-/issues/3))


### 모듈과 TCP 통신
- Core측에 공장 운영에 필요한 전반 데이터를 전송하고, 시뮬레이터 결과를 전달받음


### 분석
- 전달 받은 시뮬레이션 결과를 정리하여 표현.

## 사용 예시
### [FILE]
- **Open Layout**: 공장 등의 도면 이미지를 불러옴. \
<img src="/uploads/86eb633da43f4e5c05cb2a6cbfbf0976/open_layout.gif" Width="50%">

- **Save, SaveAs**: 현재 작업중인 도면 저장. \
<img src="/uploads/d3c62569a18beb53e38f5d54650fe9b8/saveAs.gif" Width="50%">

- **Load**: 이전에 작업했던 도면 불러오기 \
<img src="/uploads/f9af23dae4d5c19354141f30fd96a6a8/loadPjt.gif" Width="50%">

- **Set Scale**: 공장의 실측 길이와 모니터 픽셀 사이의 길이 비 변경. \
<img src="/uploads/eeb9ad8ee35df59ab0aa934469ae6f7b/Set_Scale.gif" width="49%" height="49%">
<img src="/uploads/c0c88a05101fa0ed913227f4c61188cb/image.png" width="49%" height="49%">

- **Export Data**: 실행 결과 엑셀파일 출력.

- **Close**: 프로그램 종료.

### [Draw]
**Node**: AGV가 목적지로 설정할 수 있는 점. 검은색 표현 \
**Port**: 물건을 선적하거나 양하할 수 있는 노드. 빨간색 표현 \
**Wait Point**: 유휴 상태의 AGV가 머무는 노드, 충전이 되는 Wait Point도 존재. 파란색 표현. \
**Path**: 노드와 노드 사이의 간선. AGV가 이동할 때 기준이 되는 선. 검은색 표현.
**Vehicle**: 실제 물류를 나르는 AGV. 노드들 위에만 그릴 수 있음. 노란색 표현.
- **노드 생성**: 마우스를 클릭한 위치에 메뉴에서 누른 종류의 노드 생성.
- **노드 선택**: 노드 위에서 마우스를 클릭하면 해당 노드 선택.
- **노드 설정**: 노드 선택 후 사이드 바의 내용 변경.
- **노드 삭제**: 노드 선택 후 사이드 바에서 Delete 버튼 클릭.
- **노드 이동**: 노드 위에서 마우스를 누른 채 움직이거나 노드 선택 후 사이드 바의 내용 변경.
- **Unload Port 추가 / 제거**: Port 노드 선택 후 사이드 바의 전체 unload 포트 목록에서 이름 클릭. 선택된 unload 포트 목록에서 이름 클릭 시 제거됨.
- **간선 생성**: Path 메뉴를 누른 뒤 특정 노드에서 클릭하여 다른 노드 위에서 놓으면 연결됨. Shift 버튼 이용 시 일직선 상에 배치됨.
- **간선 삭제**: 노드 선택 후 연결된 Path 목록에서 Path 클릭 시 제거.

### [Simulate]
- **Play**: 시뮬레이션을 시작함.
- **Pause**: 진행중인 시뮬레이션 일시 정지.
- **Stop**: 시뮬레이션 종료.
- **Oper Data**: 운영에 필요한 데이터 설정.
    - 하루 반송량: 공장 운영의 목표치 설정.
    - 시뮬레이션 속도: 시뮬레이션 진행 속도를 설정.
    - 화면 출력: 시뮬레이션 화면 출력 여부 결정.

### [Repot]
- **Util Rate**: AGV들의 가동률을 볼 수 있는 막대 그래프.
- **Charge**: AGV들의 충전률을 볼 수 있는 꺾은선 그래프.
- **CMD Rate**: AGV에 전달된 명령어들의 비율을 볼 수 있는 막대 그래프.
- **Progress**: 작업 진행 정도를 보여주는 그래프.
- **Via Rate**: 노드 별 방문 빈도를 보여주는 그래프.

## 사용 기술 스택
- Python 3.9
- PyQt5
- Pyinstaller
