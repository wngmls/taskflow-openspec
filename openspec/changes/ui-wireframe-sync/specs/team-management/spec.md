## MODIFIED Requirements

### Requirement: 팀 생성
시스템은 로그인한 사용자가 팀을 생성할 수 있어야 한다. 생성 즉시 초대코드(^[A-Z]{4}-[0-9]{4}$)를 자동 발급하고, 생성자를 owner_id로 지정하며, users.team_id를 업데이트한다. **UI는 팀 선택 화면에서 좌측 컬럼에 팀 만들기 영역을 표시한다.**

#### Scenario: 정상 팀 생성
- **WHEN** POST /teams { name: "Frontiers" } (유효한 JWT) 요청
- **THEN** 201 { id, name, invite_code: "FRNT-2026", owner_id, created_at } + users.team_id 업데이트

#### Scenario: 팀 이름 유효성 오류
- **WHEN** 빈 문자열 또는 30자 초과 팀 이름으로 POST /teams 요청
- **THEN** 400 { error: { code: "VALIDATION_ERROR", message: "팀 이름은 1-30자여야 합니다" } }

### Requirement: 초대코드로 팀 합류
시스템은 유효한 초대코드를 입력한 사용자를 해당 팀에 합류시킨다. users.team_id를 업데이트하며, 이미 팀 소속인 사용자는 합류 불가(409). **UI는 팀 선택 화면에서 우측 컬럼에 초대코드 입력 영역을 표시한다. 두 영역은 가로 2컬럼으로 나란히 배치된다.**

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

## ADDED Requirements

### Requirement: 팀 선택 화면 레이아웃
팀 선택 화면은 스토리보드 v2 와이어프레임을 따른다.

#### Scenario: 2컬럼 레이아웃
- **WHEN** 팀 미가입(team_id=NULL) 사용자가 팀 선택 화면 로드
- **THEN** 좌측에 "새 팀 만들기", 우측에 "초대코드로 합류" 영역이 가로 2컬럼(`md:grid-cols-2`)으로 나란히 표시

#### Scenario: 로고 및 헤더
- **WHEN** 팀 선택 화면 로드
- **THEN** 헤더 좌측에 teal 배경 박스 안에 흰색 텍스트 `TaskFlow` 로고 표시, 우측에 로그인된 이메일과 로그아웃 버튼
