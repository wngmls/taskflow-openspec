## Why

스토리보드 v2 와이어프레임을 전수 검토한 결과, 이전 UI 동기화(ui-wireframe-sync)에서 다루지 않은 7가지 UI 컴포넌트가 누락되어 있다. 주로 에러 상태 표시, 모바일 반응형, 폴링 실패 처리, 카드 상세 모달 레이아웃이 와이어프레임과 일치하지 않는다.

## What Changes

- **에러 UI 스타일**: 로그인/회원가입의 validation 에러를 전체 너비 빨간 박스 + 필드 빨간 border로 표시
- **빈 칸반 Empty State**: TODO 컬럼에만 `+ 첫 태스크 만들기` CTA 강조, DOING/DONE은 `드래그로 이동` 텍스트
- **카드 상세 모달**: 좌우 분리 레이아웃(메타 정보 좌측, 액션 우측), 빨간 삭제 버튼 박스
- **폴링 실패 UI**: 연결 끊김 배너, 재시도 카운터(Exponential backoff), 타임라인 구분선
- **모바일 칸반**: 컬럼 탭 인디케이터, FAB(+) 버튼, 카드 길게 누르기 → 상태 변경 메뉴
- **모바일 채팅**: `← 채팅` 뒤로가기 헤더, visualViewport 키보드 대응, pull-to-refresh
- **채팅 1000자 초과 스타일**: 좌측 빨간 볼드 카운터, textarea 빨간 border, 전송 버튼 비활성

## Capabilities

### New Capabilities

<!-- 신규 기능 없음 -->

### Modified Capabilities

- `authentication`: 로그인/회원가입 에러 UI 스타일
- `kanban-board`: 빈 칸반 empty state, 카드 상세 모달 레이아웃, 모바일 칸반 반응형
- `team-chat`: 폴링 실패 UI, 1000자 초과 스타일, 모바일 채팅 반응형

## Impact

- **Frontend만 영향**: HTML/CSS/JS 변경
- **API 변경 없음**
- **DB 변경 없음**
