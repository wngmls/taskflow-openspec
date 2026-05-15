## Why

사용자가 다크모드/라이트모드를 선택할 수 없어 야간 사용 시 눈의 피로가 가중된다. OS 설정을 따르는 기본값에 더해 수동 토글을 제공해 사용자 경험을 개선한다.

## What Changes

- **다크모드 CSS**: Tailwind `dark:` 유틸리티 클래스로 모든 화면 다크 스타일 적용
- **테마 토글 버튼**: 헤더 우측에 ☀️/🌙 버튼 추가, 클릭 시 라이트/다크 전환
- **설정 저장**: `localStorage`에 `theme` 키로 저장, 페이지 새로고침 후에도 유지
- **OS 기본값**: 저장된 설정 없으면 `prefers-color-scheme` 미디어 쿼리로 OS 설정 따름
- **적용 화면**: login, signup, team, kanban, chat, members 전체 6개 화면

## Capabilities

### New Capabilities

- `theme-toggle`: 다크/라이트 모드 토글 및 저장

### Modified Capabilities

<!-- 기존 기능 동작 변경 없음, UI 스타일만 추가 -->

## Impact

- **Frontend만 영향**: HTML/CSS(Tailwind dark:) 변경, JS 테마 로직 추가
- **API/DB 변경 없음**
- **공통 로직은 `js/theme.js`로 분리** — 모든 페이지에서 `<script src="/js/theme.js">` 로드
