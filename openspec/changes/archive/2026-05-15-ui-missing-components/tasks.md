## 1. 에러 UI 스타일 (로그인/회원가입)

- [x] 1.1 signup.html — 이메일 형식 오류: 빨간 border + 필드 아래 인라인 메시지
- [x] 1.2 signup.html — 이메일 중복(409): 전체 너비 빨간 박스 에러 표시
- [x] 1.3 signup.html — 비밀번호 8자 미만: 빨간 border + 인라인 메시지
- [x] 1.4 login.html — 401 오류: 비밀번호 필드~버튼 사이 전체 너비 빨간 박스

## 2. 빈 칸반 Empty State

- [x] 2.1 kanban.html — TODO 컬럼: `+ 첫 태스크 만들기` 클릭 가능 링크 추가
- [x] 2.2 kanban.html — DOING/DONE 컬럼: `드래그로 이동` 안내 텍스트(클릭 불가)

## 3. 카드 상세 모달 레이아웃

- [x] 3.1 kanban.html — 모달 좌우 분리 레이아웃 (메타 좌측, 액션 우측)
- [x] 3.2 kanban.html — 담당자/생성자/생성시각 메타 정보 표 형태 표시
- [x] 3.3 kanban.html — 삭제 버튼을 빨간 border 박스 버튼으로 변경

## 4. 폴링 실패 UI

- [x] 4.1 chat.html — 연결 끊김 배너 (`⚠ 연결 끊김 · 재시도 중`) 구현
- [x] 4.2 chat.html — 메시지 타임라인 구분선 (`--- HH:mm부터 연결 끊김 ---`)
- [x] 4.3 chat.html — 재시도 카운터 표시 + Exponential Backoff (5→10→20→40→60s)
- [x] 4.4 chat.html — 오프라인 입력창 placeholder 변경
- [x] 4.5 chat.html — 연결 복구 시 토스트 + since= 재동기화

## 5. 채팅 1000자 초과 스타일

- [x] 5.1 chat.html — 카운터를 좌측 빨간 볼드 `N,NNN / 1,000` 형식으로 변경
- [x] 5.2 chat.html — 초과 시 textarea 빨간 border + 전송 버튼 회색 비활성

## 6. 모바일 칸반

- [x] 6.1 kanban.html — 상단 컬럼 탭 인디케이터 (TODO/DOING/DONE underline 방식)
- [x] 6.2 kanban.html — FAB(+) 버튼 (우하단 고정, 현재 활성 컬럼 카드 추가)
- [x] 6.3 kanban.html — 카드 길게 누르기 → 상태 변경 바텀시트 메뉴

## 7. 모바일 채팅

- [x] 7.1 chat.html — `← 채팅` 뒤로가기 헤더 (모바일 < 768px)
- [x] 7.2 chat.html — visualViewport API로 키보드 대응 (메시지 영역 자동 축소)
- [x] 7.3 chat.html — Pull-to-refresh로 강제 동기화
