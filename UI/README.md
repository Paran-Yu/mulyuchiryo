# UI Tools

## 소개
물류치료의 `UI Tools`는 동선을 계산하는 핵심 로직인 Core에 명령과 데이터를 전달하고, 실행 결과에 대한 보고서를 사용자가 쉽게 알아볼 수 있도록 표현해주는 GUI 프로그램입니다.

> (완성된 이미지)

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



## 사용 기술 스택
- Python 3.9
- PyQt5
- Pyinstaller