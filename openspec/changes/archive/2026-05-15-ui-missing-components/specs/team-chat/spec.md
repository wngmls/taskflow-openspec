## MODIFIED Requirements

### Requirement: 메시지 전송
시스템은 팀 멤버가 1000자 이내 텍스트 메시지를 전송할 수 있어야 한다. **1000자 초과 시 카운터를 좌측 빨간 볼드(`font-bold text-red-600`)로 표시하고, textarea에 빨간 border를 추가하며, 전송 버튼을 비활성화(회색)한다.**

#### Scenario: 정상 메시지 전송
- **WHEN** POST /teams/{id}/messages { content: "안녕하세요" } 요청
- **THEN** 201 { id, user_id, content, created_at } 반환

#### Scenario: 1000자 초과 UI
- **WHEN** textarea에 1000자 초과 입력
- **THEN** 카운터를 `1,042 / 1,000` 형식으로 좌측 빨간 볼드 표시, `42자 초과` 보조 텍스트, textarea에 빨간 border, 전송 버튼 비활성(회색)

## ADDED Requirements

### Requirement: 폴링 실패 UI
5초 폴링 중 네트워크 오류 발생 시 사용자에게 연결 끊김 상태를 시각적으로 알린다.

#### Scenario: 연결 끊김 배너
- **WHEN** GET /teams/{id}/messages 요청이 네트워크 오류로 실패
- **THEN** 채팅 헤더의 폴링 상태 표시를 `⚠ 연결 끊김 · 재시도 중` 빨간 배경 배너로 교체

#### Scenario: 타임라인 구분선
- **WHEN** 폴링 실패 발생
- **THEN** 메시지 목록에 `--- HH:mm부터 연결 끊김 ---` 구분선 삽입

#### Scenario: 재시도 카운터
- **WHEN** 폴링 실패 후 재시도 중
- **THEN** 메시지 영역 하단에 `🔄 N초 후 재연결 시도 중... (시도 횟수: N/∞)` 표시, Exponential Backoff(5→10→20→40→60s)

#### Scenario: 오프라인 입력창
- **WHEN** 폴링 실패 상태에서 입력창 포커스
- **THEN** placeholder를 `오프라인 — 연결 복구 후 전송됩니다`로 표시

#### Scenario: 연결 복구
- **WHEN** 폴링 재연결 성공
- **THEN** `연결되었습니다` 토스트 표시, since= 파라미터로 누락 메시지 일괄 수신, 구분선 제거

### Requirement: 모바일 채팅 반응형
모바일(< 768px)에서 채팅 화면은 전용 레이아웃을 사용한다.

#### Scenario: 뒤로가기 헤더
- **WHEN** 모바일에서 채팅 화면 로드
- **THEN** 상단 헤더에 `← 채팅` 뒤로가기 버튼 표시, 클릭 시 `history.back()`

#### Scenario: 키보드 대응
- **WHEN** 모바일에서 메시지 입력창 포커스(키보드 올라옴)
- **THEN** `visualViewport` API로 키보드 높이 감지, 메시지 영역 자동 축소하여 최신 메시지 가시성 유지

#### Scenario: Pull-to-refresh
- **WHEN** 모바일에서 채팅 메시지 영역을 아래로 당김
- **THEN** 강제 동기화 실행(since 없이 GET /messages 재요청)
