## ADDED Requirements

### Requirement: 환경 분리 (로컬/운영)
시스템은 DATABASE_URL 환경변수 하나로 로컬(SQLite)과 운영(Neon PostgreSQL)을 전환해야 한다.

#### Scenario: 로컬 개발 환경
- **WHEN** DATABASE_URL=sqlite:///./taskflow.db 로 FastAPI 실행
- **THEN** SQLite 파일에 연결, uvicorn으로 로컬 서버 정상 동작

#### Scenario: 운영 환경 (Neon)
- **WHEN** DATABASE_URL=postgres://...neon.tech (Vercel 자동 주입) 로 배포
- **THEN** Neon PostgreSQL에 연결, 동일 SQLAlchemy 모델로 동작

### Requirement: Vercel 배포
시스템은 Vercel에 프론트엔드(정적 파일)와 백엔드(FastAPI Serverless Functions)를 함께 배포해야 한다.

#### Scenario: 배포 성공
- **WHEN** git push origin main 후 Vercel 자동 빌드
- **THEN** 5분 이내 배포 완료, taskflow.vercel.app 에서 접근 가능

#### Scenario: API 라우팅
- **WHEN** /api/* 경로로 요청
- **THEN** FastAPI Serverless Function으로 라우팅

#### Scenario: 정적 파일 서빙
- **WHEN** /* 경로로 요청 (API 제외)
- **THEN** static/ 디렉토리의 HTML/JS/CSS 파일 반환
