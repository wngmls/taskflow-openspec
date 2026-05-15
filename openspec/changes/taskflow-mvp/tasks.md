## 1. 프로젝트 초기 설정

- [x] 1.1 디렉토리 구조 생성 (api/, static/, vercel.json)
- [x] 1.2 Python 의존성 설치 (FastAPI, SQLAlchemy, python-jose, bcrypt, pydantic, uvicorn)
- [x] 1.3 vercel.json 라우팅 설정 (/api/* → Serverless, /* → static/)
- [x] 1.4 .env 파일 및 DATABASE_URL 환경변수 설정
- [x] 1.5 SQLAlchemy DB 연결 설정 (SQLite ↔ Neon 전환)

## 2. DB 스키마 구현

- [x] 2.1 users 테이블 (id, email UNIQUE, password_hash, team_id FK NULL, created_at)
- [x] 2.2 teams 테이블 (id, name 1-30자, invite_code UNIQUE, owner_id FK, created_at)
- [x] 2.3 tasks 테이블 (id, team_id FK, title 1-100자, status TODO/DOING/DONE, creator_id FK, assignee_id FK NULL, created_at)
- [x] 2.4 messages 테이블 (id, team_id FK, user_id FK, content 1-1000자, created_at)
- [x] 2.5 DB 초기화 스크립트 (create_all) 및 로컬 SQLite 파일 생성 확인

## 3. 인증 API (Auth 4개)

- [x] 3.1 POST /auth/signup — bcrypt 해시, EMAIL_TAKEN(409), VALIDATION_ERROR(400), 201+JWT
- [x] 3.2 POST /auth/login — bcrypt 검증, INVALID_CREDENTIALS(401) 이메일 노출 금지, 200+JWT(24h)+team_id
- [x] 3.3 POST /auth/logout — stateless, 200 {} 반환
- [x] 3.4 GET /auth/me — JWT 검증, 200 { id, email, team_id }
- [x] 3.5 JWT 미들웨어 — 만료 시 TOKEN_EXPIRED(401), 모든 /teams/* 보호

## 4. 팀 API (Team 5개)

- [x] 4.1 POST /teams — 팀 생성, invite_code 자동 생성(^[A-Z]{4}-[0-9]{4}$), users.team_id 업데이트, 201
- [x] 4.2 POST /teams/join — 초대코드 검증, ALREADY_IN_TEAM(409), NOT_FOUND(404), users.team_id 업데이트, 200
- [x] 4.3 GET /teams/{id} — 팀 정보, 비멤버 FORBIDDEN(403)
- [x] 4.4 GET /teams/{id}/members — 멤버 목록 (is_owner 구분), 비멤버 403
- [x] 4.5 DELETE /teams/{id}/leave — users.team_id = NULL, 200

## 5. 칸반 API (Task 6개)

- [x] 5.1 GET /teams/{id}/tasks — 전체/필터(me/unassigned), 최근 생성순, 비멤버 403
- [x] 5.2 POST /teams/{id}/tasks — 생성, status=TODO, assignee_id nullable, 201
- [x] 5.3 GET /tasks/{id} — 상세 조회, 비멤버 403
- [x] 5.4 PUT /tasks/{id} — 제목·assignee 수정
- [x] 5.5 PATCH /tasks/{id}/status — 상태 변경(TODO/DOING/DONE), 드래그 전용
- [x] 5.6 DELETE /tasks/{id} — creator OR team owner만, FORBIDDEN(403)

## 6. 채팅 API (Chat 3개)

- [x] 6.1 GET /teams/{id}/messages — since= 증분 폴링, 초기 최근 50개, 빈 배열 가능
- [x] 6.2 POST /teams/{id}/messages — 1000자 제한, TOO_LONG(400), 201
- [x] 6.3 DELETE /messages/{id} — 본인만, NOT_OWNER(403)

## 7. 에러 응답 표준화

- [x] 7.1 에러 핸들러 미들웨어 — 모든 4xx/5xx를 { error: { code, message } } 형태로 통일
- [x] 7.2 CORS 설정 — Vercel 도메인(taskflow.vercel.app) 명시
- [x] 7.3 에러 코드 목록 검증 (EMAIL_TAKEN, INVALID_CREDENTIALS, TOKEN_EXPIRED, FORBIDDEN, NOT_FOUND, TOO_LONG, NOT_OWNER, ALREADY_IN_TEAM, VALIDATION_ERROR)

## 8. 프론트엔드 — 화면 구현

- [x] 8.1 로그인 화면 (login.html) — 이메일/비밀번호 입력, 에러 표시, JWT localStorage 저장
- [x] 8.2 회원가입 화면 (signup.html) — validation, 에러 메시지(400/409), 성공 시 팀 선택으로
- [x] 8.3 팀 선택 화면 (team.html) — 팀 만들기+초대코드 발급, 초대코드 합류, 에러 케이스 3종
- [x] 8.4 칸반 화면 (kanban.html) — 3컬럼(TODO/DOING/DONE), 카드 추가(인라인), 필터, 빈 상태
- [x] 8.5 칸반 드래그 구현 — HTML5 native Drag & Drop, drop 시 PATCH /status 호출
- [x] 8.6 카드 상세 모달 — 제목/상태/assignee 수정, 삭제(확인 다이얼로그), 권한별 버튼 노출
- [x] 8.7 채팅 화면 (chat.html) — 메시지 목록, 5초 폴링(since=), 1000자 카운터, 발신자+시각
- [x] 8.8 멤버 목록 패널 — owner(★) 구분, GET /teams/{id}/members
- [x] 8.9 반응형 UI — md:768px(1컬럼 스와이프), lg:1024px, 햄버거 메뉴

## 9. 프론트엔드 — 공통 처리

- [x] 9.1 JWT 관리 (저장/읽기/삭제) + 401 interceptor → /login redirect
- [x] 9.2 팀 미가입(team_id=NULL) 시 강제 팀 선택 화면 redirect
- [x] 9.3 클라이언트 validation (이메일 형식, 비밀번호 8자, 초대코드 형식, 1000자 카운터)
- [x] 9.4 모바일 채팅 폴링 단축 (포커스 시 5초→2초, visualViewport API)

## 10. 배포

- [x] 10.1 Vercel 프로젝트 연결 (vercel link)
- [x] 10.2 Vercel Storage Neon 통합 설치 (DATABASE_URL 자동 주입 확인)
- [x] 10.3 운영 DB 테이블 생성 (Neon에 create_all 실행)
- [x] 10.4 첫 배포 (vercel deploy --prod) + 5분 내 완료 확인
- [ ] 10.5 전체 흐름 수동 검증 (회원가입→로그인→팀→칸반→채팅→모바일)
