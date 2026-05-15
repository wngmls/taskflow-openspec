## ADDED Requirements

### Requirement: 메시지 목록 조회 (폴링)
시스템은 팀 채팅 메시지를 반환해야 한다. 초기 진입 시 최근 50개, 이후 since= 파라미터로 증분 조회. 새 메시지가 없으면 빈 배열 반환.

#### Scenario: 초기 메시지 조회
- **WHEN** GET /teams/{id}/messages (since 없음, 팀 멤버 JWT) 요청
- **THEN** 200 [{ id, user_id, user_email, content, created_at }] 최근 50개 시간순 반환

#### Scenario: 증분 폴링
- **WHEN** GET /teams/{id}/messages?since=2026-05-13T14:27:00Z 요청
- **THEN** 200 해당 시각 이후 메시지만 반환 (빈 배열이면 [])

#### Scenario: 메시지 누락 없음 보장
- **WHEN** POST 성공(201)한 메시지에 대해 GET 요청
- **THEN** 반드시 응답에 포함됨 (메시지 누락 0건 Metric)

### Requirement: 메시지 전송
시스템은 팀 멤버가 1000자 이내 텍스트 메시지를 전송할 수 있어야 한다. 클라이언트와 서버 양쪽에서 검증.

#### Scenario: 정상 메시지 전송
- **WHEN** POST /teams/{id}/messages { content: "안녕하세요" } (팀 멤버 JWT) 요청
- **THEN** 201 { id, user_id, content, created_at } 반환

#### Scenario: 1000자 초과
- **WHEN** POST /teams/{id}/messages { content: 1001자 텍스트 } 요청
- **THEN** 400 { error: { code: "TOO_LONG", message: "메시지는 1000자 이내로 입력하세요", limit: 1000, actual: 1001 } }

### Requirement: 메시지 삭제 (본인만)
시스템은 본인 메시지만 삭제할 수 있어야 한다. team owner도 타인 메시지 삭제 불가 (결정 #6, 커뮤니티 신뢰 모델).

#### Scenario: 본인 메시지 삭제
- **WHEN** DELETE /messages/{id} (메시지 작성자 JWT) 요청
- **THEN** 200 {} + 메시지 삭제

#### Scenario: 타인 메시지 삭제 시도
- **WHEN** DELETE /messages/{id} (다른 사용자 JWT, owner 포함) 요청
- **THEN** 403 { error: { code: "NOT_OWNER", message: "본인의 메시지만 삭제할 수 있습니다" } }
