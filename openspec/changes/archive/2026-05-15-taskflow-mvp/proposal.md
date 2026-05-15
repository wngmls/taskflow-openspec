## Why

소규모 팀(3-5인)이 칸반 보드와 실시간 채팅을 한 화면에서 함께 사용할 수 있는 협업 도구가 없어, 팀 업무 진행 추적과 빠른 의사결정이 분리된 도구 사이에서 이루어지고 있다. TaskFlow MVP는 이 두 기능을 단일 화면으로 통합하여 팀 리더·팀원·신규 합류자 모두가 컨텍스트를 1분 안에 파악할 수 있도록 한다.

## What Changes

- **인증 시스템**: 이메일+비밀번호 회원가입/로그인, JWT(24h) 발급, bcrypt 해시
- **팀 관리**: 팀 생성, 초대코드(AAAA-9999 형식) 발급·합류, 멤버 목록 조회 (1인 1팀 모델)
- **칸반 보드**: TODO/DOING/DONE 3컬럼, 카드 추가·드래그 이동(PATCH /status)·삭제, assignee 지정, 필터(@me/미할당/전체)
- **팀 채팅**: 팀 단위 채팅 송수신, 5초 폴링(since= 증분), 메시지 1000자 제한, 발신자+시각 표시
- **배포**: Vercel(FE+BE Serverless) + Vercel Storage Neon(운영 PostgreSQL), 로컬은 SQLite

**범위 외 (Out of Scope)**: 알림(이메일/SMS/푸시), 파일 첨부, 전문 검색, 권한 세분화(admin/member 이상), 다국어, WebSocket, 테스트 자동화

## Capabilities

### New Capabilities

- `authentication`: 회원가입, 로그인, JWT 발급·검증, 로그아웃(stateless), 현재 사용자 조회 (Auth 4개 API)
- `team-management`: 팀 생성, 초대코드 발급·합류, 팀 정보 조회, 멤버 목록, 팀 떠나기 (Team 5개 API)
- `kanban-board`: 태스크 CRUD, 상태 변경(드래그), assignee 지정, 필터·정렬, 권한 검증 (Task 6개 API)
- `team-chat`: 채팅 메시지 송수신, 5초 폴링, 1000자 제한, 메시지 삭제(본인만) (Chat 3개 API)
- `deployment`: 로컬 SQLite ↔ 운영 Neon 환경 분리, Vercel 배포 구성

### Modified Capabilities

<!-- 신규 프로젝트이므로 해당 없음 -->

## Impact

- **Backend**: FastAPI + SQLAlchemy (SQLite/Neon 양쪽 호환), 4테이블(users, teams, tasks, messages), API 18개
- **Frontend**: Vanilla JS + Tailwind CSS, HTML5 Drag & Drop API, fetch + JWT 헤더, 5초 폴링, 반응형(768/1024 breakpoint)
- **DB 스키마 변경점** (스토리보드 v2 결정사항):
  - `users.team_id` 추가 (FK→teams, NULL허용, 1인 1팀)
  - `tasks.assignee_id` 추가 (FK→users, NULL허용)
  - `tasks.created_at` 추가 (정렬용)
  - `PATCH /tasks/{id}/status` 분리 (기존 PUT에서 분리, 결정 #3)
  - `GET /teams/{id}` 추가 (결정 #8)
- **인프라**: Vercel(무료 티어), Vercel Storage Neon(Pooled 자동 주입), DATABASE_URL 환경변수로 전환
