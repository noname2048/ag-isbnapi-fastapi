# ag-isbnapi-fastapi

쿼리로 isbn을 날리면 네이버책 API를 통해 정보를 검색해서
캐싱한뒤, 캐싱을 이용해 리턴하는 API

## 프로젝트 요구사항
__개발환경 요구사항__
* 어느 컴퓨터이던 local에서 실행이 가능했으면 좋겠음
  1. db는 docker로 실행되어 생성되었다가 사라지며, 공용 DB는 나중에 베이킹 해서 인터넷에서 받는걸로.
  2. 명령어 한개를 치면 (많아도 3개까지) 구경온 사람이 이 프로젝트를 실행 가능했으면 좋겠다. (근데 서점 API는 개개인용인데...)
  3. 상수는 한곳에 모아놓아서, (예: db이름) docker와 fastapi가 모두 이 파일에서 참조할 수 있었으면 좋겠다. (아마 env 파일이 될듯)
* ERD 를 넣어놓자(개체-관계 다이어그램)
* 일반적으로 깨끗한 app import가 되었으면 좋겠다.
* 크게 3가지로 분류하자
  1. 1단계 .gitignore, README, CI/CD와 관계된 것들
  2. 프로젝트 환경설정 (poetry, docker와 관계된 것들)
  3. app 그 자체


## 폴더트리정렬
- 내가 작성한 프로젝트의 폴더 트리 이유를 적어 놓으면 나중에 참조하기 편할것 같아서.
```bash
├── .env # 노출되면 안되는 키값
├── .gitignore # 깃 이그노어 파일
├── Dockerfile 
├── README.md # 현재 읽고 있는 파일
├── aladin.py
├── docker-build-image.sh
├── docker-compose.yml
├── jupyter_research
│   ├── aladin.ipynb  # 알라딘 API 사용 연습
│   ├── mongo.ipynb  # mongodb 연습
│   ├── naver.ipynb  # naver API 사용 연습
│   └── thumb.jpg  # API에서 나온 썸네일 (추후 삭제)
├── main.py # 메인앱
├── poetry.lock # poetry 상세 버전 기술 (의존성에 대한 풀이)
├── pyproject.toml # (pip freeze) requirement.txt 와 같은 역할
└── thumbnail # 썸네일 저장 폴더, 썸네일은 제목은 isbn 13 자리로 저장
    ├── 9791158392239.jpg
    └── 9791186179420.jpg
```
## 이 프로젝트를 오랜만에 방문했을때 해야할것
- poetry update
- mongodb connection 확인

## 목적

fastapi 연습, mongodb(key-document NoSQL) 연습

## 배운점

- pylance에 의해 로드된 requests 모듈 import 문에 마우스를 대고 있으면, 신기하게 주석이 나온다 (어떻게 한걸까?)
  - fastapi는 안나온다.
- fastapi는 pydantic을 이용해 type hinting 이나 parse를 도와준다.
  - https://velog.io/@kjh03160/Type-Hinting
  - 대표적으로 body에 request가 담겨져 오는 post의 경우에 사용가능한것으로 보인다.
  - pydantic은 class 중첩으로 사용자가 선언한 클래스를 type hint로 줄 수 있다.
  - 

개발외지식
- 네이버의 경우 10자리 isbn의 경우 작동이 잘 안될 수 도 있다.
  - ex) `k622633024`는 어떤 책의 isbn이다. 검색결과 (display = 0)
  - 사용자가 10자리를 보고 13자리로 변환하는 것은 어려워보인다.
  - 따라서 서점의 API사용이 필요해보인다.
  - 우선 알라딘의 API사용을 해보고, 안되면 크롤링해야 하겠다.
