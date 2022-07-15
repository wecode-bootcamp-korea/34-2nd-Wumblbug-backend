# Greeneeds


[greeneeds](https://user-images.githubusercontent.com/65996045/179173662-85daefb2-5956-467e-9633-dec5ace28ea8.gif)


## Introduction
크라우드 펀딩 [텀블벅](https://tumblbug.com/discover) 홈페이지 클론 코딩 프로젝트입니다.

- 기간: 22.07.04 ~ 22.07.15
- 구성: Front-End 4명 / Back-End 2명
- [프론트엔드 깃헙주소](https://github.com/wecode-bootcamp-korea/34-2nd-greeneeds-frontend)
- 협업 툴: Github, Trello, Slack, Notion

</br>

## Project Objective
- Django 프레임 워크를 사용하여 백엔드 서버 구축
- MySQL를 사용하여 DB 구축
- 카카오 로그인 API를 연동하여 회원가입 API 구현
- Django에서 S3로 이미지 업로드하는 기능 구현

</br>

## DB Modeling
![greeneeds Databases](https://user-images.githubusercontent.com/65996045/178923387-db892fc9-ed98-4c26-ab4f-57360aa0f305.png)

</br>

## Technologies
- Python
- Django Web Framewrok
- MySQL
- Git, Github
- AWS(EC2, RDS, S3)

</br>

## Features
**User**
1. 회원가입 (POST)
    - 카카오 로그인 API 연동
    - 카카오 로그인 Unit test
2. 로그인 (POST)
    - 로그인 성공시 JWT Access Token 발급

</br>

**Project**
1. 프로젝트 리스트 조회 (GET)
	- Query Parameter로 좋아요순, 최신순 필터링하여 정보 전달
2. 프로젝트 상세 조회 (GET)
	- Path Parameter로 project_id에 맞춰 상세 정보 전달
3. 프로젝트 포스팅 (POST)
	- S3로 이미지 업로드
	- 업로드된 이미지의 url 반환

</br>

**Like**
1. 좋아요 (POST)
	- 좋아요 추가/삭제

</br>

## API Documentation
- [API Documentation](https://velog.io/@chaduri7913/Greeneeds-API-Documentation)
