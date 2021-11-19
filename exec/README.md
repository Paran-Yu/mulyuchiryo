## 1. gitlab 소스 클론 이후 빌드 및 배포할 수 있는 작업 문서

해당사항 없음

## 2. 프로젝트에서 사용하는 외부 서비스 정보 문서

requirements.txt 의 의존성 이외 해당사항 없음

## 3. 데이터베이스 덤프 파일 최신본

해당 프로젝트는 데이터베이스보다는 `layout`파일 및 `xml`파일 기반으로 작동합니다.
- 경로가 상당히 중요하므로, 기작성된 파일들을 레포지토리에 포함시켜서 드립니다.
- `{rootDir}/map.layout`
- `{rootDir}/res/img/map.jpg`

시뮬레이션을 통해 생성되는 데이터베이스는 `{rootDir}/simul_data.db`입니다. 미리 시뮬레이팅된 결과를 통계기능에서 보고 싶은 경우를 위해 현재 폴더(`exec`)에 `simul_data.db`를 첨부합니다. 
- 보시고자 하는 경우 `{rootDir}/simul_data.db`에 덮어쓰기 하시면 됩니다.
- 용량이 70mb 정도로, 통계기능 동작시 하드웨어 사양에 따라 몇 분 소모될 수 있습니다.

## 4. 시연 시나리오 (스크립트 포함)

> 시연 순서에 따른 site 화면별, 실행별(클릭 위치 등) 상세 설명

1. 맵 그리기 시연
2. 그린 지도 `layout` `xml`파일 저장
3. 기존 `xml` 불러오기
4. Simulator 파라미터 설정
5. Simulator Matplot 있는 버전 시연
6. Simulator Matplot 없는 버전 시연
7. 사전녹화한 Simulator 영상
8. 사전 Simulate 데이터로 통계 기능 시연
9. Excel로 내보내기 시연