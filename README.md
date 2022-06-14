# ag-isbnapi-fastapi

- isbn으로 검색하면 해당하는 책정보를 리턴하는 서비스
- 자체 DB가 있고, DB에 없을 경우 외부에서 크롤링 진행

## 프로젝트 상세
- fastapi 이용
- swagge(openap)를 통한 api 문서 자동화
- sqlite를 이용

## 프로젝트 주안점
- 검색을 시도했을 때부터 크롤링을 하기 때문에 약 2~3초의 시간차가 발생한다
- 이 중간에 loading을 띄우는건 쉽지만 관련 API 시퀀스를 어떻게 구성할 것인가? 
  1. socket을 시도하거나
  2. pub/sub 이벤트를 사용하거나 (redis)
  3. HTTP endpoint를 따로 만들거나(HTTP 최대 300초 대기 가능)

## 시도해보려고 하고 있는 기술
- graphql 도입 해보기
