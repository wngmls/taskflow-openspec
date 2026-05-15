## Context

TaskFlow MVP는 신규 프로젝트로, 기존 코드베이스 없이 처음부터 구축한다. 스토리보드 v2에서 확정된 8가지 결정사항이 설계 기반이 된다. 로컬 개발은 SQLite, 운영은 Vercel + Neon으로 환경이 분리되며, DATABASE_URL 환경변수 하나로 전환된다.

**확정된 설계 결정 (스토리보드 v2)**:
1. 1인 1팀 모델: `users.team_id` (NULL=미가입)
2. 내 태스크 = `assignee_id` (creator_id 아님)
3. `PATCH /tasks/{id}/status` 분리 (드래그 전용)
4. `logout` stateless: 200만 반환, JWT 블랙리스트 없음
5. 권한: 비멤버→403, DELETE는 creator/owner만, 메시지 DELETE는 본인만

## Goals / Non-Goals

**Goals:**
- FastAPI + SQLAlchemy로 API 18개 구현 (로컬 SQLite ↔ Neon 양쪽 호환)
- Vanilla JS + Tailwind로 9개 화면 구현 (반응형, 모바일 768px breakpoint)
- Vercel Serverless Functions로 백엔드 배포
- JWT 인증, bcrypt 해시, CORS, 에러 응답 표준화

**Non-Goals:**
- WebSocket (5초 폴링으로 대체)
- pytest/jest 자동 테스트 (수동 동작 확인만)
- 이메일 알림, 파일 첨부, 전문 검색
- 다국어, 권한 세분화 (admin/member 이상)
- JWT 갱신 토큰 (24h 만료 시 재로그인)

## Decisions

### D1: 백엔드 — FastAPI + SQLAlchemy
FastAPI(async, auto OpenAPI)를 선택. SQLAlchemy를 ORM으로 사용해 SQLite(로컬)와 PostgreSQL(Neon 운영) 양쪽 호환. 라이브러리: `python-jose`(JWT), `bcrypt`(해시), `pydantic`(validation).

**대안 고려**: Django REST Framework → 과도한 보일러플레이트, MVP 범위에 부적합.

### D2: 프론트엔드 — Vanilla JS + Tailwind (CDN)
프레임워크 없이 순수 ES6+. Tailwind는 CDN으로 빌드 과정 생략. HTML5 native Drag & Drop API로 칸반 드래그 구현.

**대안 고려**: React/Vue → 번들러 설정 복잡도가 Day 2 범위 초과.

### D3: 배포 구조 — FastAPI → Vercel Serverless
FastAPI를 `api/` 디렉토리에 놓고 Vercel Serverless Functions로 배포. 프론트는 정적 파일. `vercel.json`으로 라우팅 설정.

```
프로젝트 루트/
├── api/          ← FastAPI (Vercel Serverless)
│   └── main.py
├── static/       ← Vanilla JS + HTML
└── vercel.json   ← 라우팅: /api/* → api/, /* → static/
```

### D4: DB 스키마 — 1인 1팀, assignee_id nullable
`users.team_id` (FK, NULL=미가입)로 1인 1팀 강제. `tasks.assignee_id` nullable로 미할당 카드 지원. 모든 FK는 CASCADE DELETE 미적용 (데이터 보호).

### D5: 채팅 폴링 — since= 증분 방식
`GET /teams/{id}/messages?since=<ISO timestamp>`로 마지막 메시지 이후만 조회. 초기 진입 시 최근 50개. 모바일 포커스 시 5초 → 2초로 단축. Exponential backoff(5→10→20→40→60s) 적용.

### D6: 에러 응답 표준
모든 4xx/5xx는 `{ "error": { "code": "SCREAMING_SNAKE", "message": "한국어" } }` 형태로 통일.

## Risks / Trade-offs

- **SQLite→Neon 마이그레이션**: SQLAlchemy로 호환성 확보하나, SQLite에 없는 PostgreSQL 기능(예: JSONB) 사용 금지 → Mitigation: 기본 타입(TEXT, INTEGER, TIMESTAMP)만 사용
- **Vercel Serverless Cold Start**: FastAPI cold start가 느릴 수 있음 → Mitigation: 함수 크기 최소화, 필요시 Vercel Fluid Compute 고려
- **5초 폴링 부하**: 동시 50명 × 5초 = 10req/s → Mitigation: `since=` 증분으로 응답 크기 최소화, Neon 무료 티어 충분
- **JWT 만료 강제 로그아웃**: 24h 후 작업 중 토큰 만료 → Mitigation: axios interceptor로 즉시 감지·알림, 재로그인 유도

## Migration Plan

1. 로컬 개발: `uvicorn api/main.py --reload` + SQLite 파일
2. Vercel 연결: `vercel link`, Neon 통합 설치 (DATABASE_URL 자동 주입)
3. 첫 배포: `vercel deploy` → Serverless Functions 자동 빌드
4. 롤백: Vercel 대시보드에서 이전 배포로 즉시 전환 가능

## Open Questions

- Tailwind CDN vs. CLI 빌드: CDN으로 시작, 번들 크기 이슈 발생 시 CLI 전환
- SQLAlchemy Core vs ORM: ORM 사용 (코드 간결성), 복잡한 쿼리는 Core 혼용
