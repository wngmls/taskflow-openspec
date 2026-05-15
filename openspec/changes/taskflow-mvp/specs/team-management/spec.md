## ADDED Requirements

### Requirement: 팀 생성
시스템은 로그인한 사용자가 팀을 생성할 수 있어야 한다. 생성 즉시 초대코드(^[A-Z]{4}-[0-9]{4}$)를 자동 발급하고, 생성자를 owner_id로 지정하며, users.team_id를 업데이트한다.

#### Scenario: 정상 팀 생성
- **WHEN** POST /teams { name: "Frontiers" } (유효한 JWT) 요청
- **THEN** 201 { id, name, invite_code: "FRNT-2026", owner_id, created_at } + users.team_id 업데이트

#### Scenario: 팀 이름 유효성 오류
- **WHEN** 빈 문자열 또는 30자 초과 팀 이름으로 POST /teams 요청
- **THEN** 400 { error: { code: "VALIDATION_ERROR", message: "팀 이름은 1-30자여야 합니다" } }

### Requirement: 초대코드로 팀 합류
시스템은 유효한 초대코드를 입력한 사용자를 해당 팀에 합류시킨다. users.team_id를 업데이트하며, 이미 팀 소속인 사용자는 합류 불가(409).

#### Scenario: 정상 합류
- **WHEN** POST /teams/join { invite_code: "FRNT-2026" } (team_id=NULL인 사용자) 요청
- **THEN** 200 { team: { id, name, member_count }, redirect: "/teams/7" } + users.team_id 업데이트

#### Scenario: 초대코드 형식 오류
- **WHEN** 형식이 ^[A-Z]{4}-[0-9]{4}$에 맞지 않는 코드로 요청
- **THEN** 400 { error: { code: "VALIDATION_ERROR", message: "형식이 올바르지 않습니다" } }

#### Scenario: 존재하지 않는 초대코드
- **WHEN** 유효한 형식이지만 존재하지 않는 코드로 요청
- **THEN** 404 { error: { code: "NOT_FOUND", message: "해당 초대코드를 찾을 수 없습니다" } }

#### Scenario: 이미 팀 소속
- **WHEN** 이미 team_id가 있는 사용자가 합류 요청
- **THEN** 409 { error: { code: "ALREADY_IN_TEAM", message: "이미 다른 팀에 소속되어 있습니다" } }

### Requirement: 팀 정보 조회
시스템은 팀 멤버에게 팀 기본 정보를 반환해야 한다. 비멤버 접근 시 403.

#### Scenario: 멤버의 팀 조회
- **WHEN** GET /teams/{id} (해당 팀 멤버의 JWT) 요청
- **THEN** 200 { id, name, invite_code, owner_id, created_at } 반환

#### Scenario: 비멤버 접근
- **WHEN** GET /teams/{other_id} (다른 팀 멤버의 JWT) 요청
- **THEN** 403 { error: { code: "FORBIDDEN", message: "이 팀의 멤버가 아닙니다" } }

### Requirement: 멤버 목록 조회
시스템은 팀 멤버 목록(owner 구분 포함)을 반환해야 한다.

#### Scenario: 멤버 목록 조회
- **WHEN** GET /teams/{id}/members (팀 멤버의 JWT) 요청
- **THEN** 200 [{ id, email, is_owner: bool, joined_at }] 반환

### Requirement: 팀 떠나기
시스템은 멤버가 팀을 떠날 수 있게 한다. users.team_id를 NULL로 업데이트. owner는 팀을 떠날 수 없다(MVP 범위 외).

#### Scenario: 멤버 팀 떠나기
- **WHEN** DELETE /teams/{id}/leave (멤버 JWT) 요청
- **THEN** 200 {} + users.team_id = NULL 업데이트
