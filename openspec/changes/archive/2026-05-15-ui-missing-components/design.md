## Context

스토리보드 v2의 B(로그인), C(팀), D(칸반), E(채팅), F(모바일) 섹션 전체를 검토해 발견한 7가지 미반영 UI 컴포넌트. 기능 동작은 모두 정상이나 시각적 피드백과 모바일 UX가 와이어프레임 기준에 미달한다.

## Goals / Non-Goals

**Goals:**
- 와이어프레임 7개 항목을 HTML/CSS/JS로 구현
- 특히 에러 상태와 폴링 실패처럼 사용자가 즉시 인지해야 하는 피드백 개선

**Non-Goals:**
- WebSocket 실시간 채팅 (Out of Scope 유지)
- 자동화 테스트
- IE 지원

## Decisions

### D1: 에러 스타일 — 전체 너비 박스
와이어프레임은 에러를 필드 아래 인라인 메시지가 아닌 전체 너비 빨간 박스로 표시. 로그인 401은 비밀번호 필드와 버튼 사이에 위치.

### D2: 빈 칸반 CTA — TODO 컬럼만 강조
TODO 컬럼에만 `+ 첫 태스크 만들기` 클릭 가능 링크. DOING/DONE은 `드래그로 이동` 안내 텍스트(클릭 불가).

### D3: 카드 상세 모달 — 좌우 분리 레이아웃
좌측: #ID + 제목(편집 가능), 상태 탭 버튼, 담당자/생성자/생성시각 메타. 우측: 저장, 다른 담당자 지정, 빨간 삭제 버튼(3개 별도 버튼).

### D4: 폴링 실패 — Exponential Backoff UI
- 헤더: `⚠ 연결 끊김 · 재시도 중` 빨간 배너로 교체
- 메시지 타임라인: 실패 시점에 `--- HH:mm부터 연결 끊김 ---` 구분선 삽입
- 하단: `🔄 N초 후 재연결 시도 중... (시도 횟수: N/∞)`
- 입력창 placeholder: `오프라인 — 연결 복구 후 전송됩니다`
- Backoff: 5→10→20→40→60s

### D5: 모바일 칸반 — 탭 인디케이터 + FAB
- 상단 탭: TODO/DOING/DONE underline 방식, 활성 탭 bold + underline
- FAB(+) 버튼: 우하단 고정, 현재 활성 컬럼에 카드 추가
- 길게 누르기(500ms): 상태 변경 바텀시트 메뉴

### D6: 모바일 채팅 — 뒤로가기 + visualViewport
- `← 채팅` 뒤로가기 헤더 (`history.back()`)
- `visualViewport` API로 키보드 높이 감지, 메시지 영역 자동 축소

## Risks / Trade-offs

- [visualViewport 지원] iOS Safari 13+, Chrome 61+ 지원 → MVP 모던 브라우저 가정으로 허용
- [길게 누르기 contextmenu] 브라우저 기본 컨텍스트 메뉴 충돌 → `preventDefault()` 처리
- [Exponential Backoff] 무한 재시도로 불필요한 요청 → 60s 상한으로 제한

## Migration Plan

프론트엔드 파일만 수정. 배포 후 즉시 적용.
