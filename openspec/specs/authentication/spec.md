## ADDED Requirements

### Requirement: 회원가입
시스템은 이메일+비밀번호로 신규 계정을 생성하고 JWT를 즉시 발급해야 한다. 이메일은 UNIQUE, 비밀번호는 bcrypt 해시 저장. 이메일 인증 없이 즉시 활성화. **에러 표시는 전체 너비 빨간 박스(`border border-red-300 bg-red-50 text-red-700`)로, 해당 필드에는 빨간 border를 추가한다.**

#### Scenario: 정상 가입
- **WHEN** POST /auth/signup { email: "user@example.com", password: "12345678" } 요청
- **THEN** 201 Created + { token: "eyJ...", user: { id, email, team_id: null } } 반환

#### Scenario: 이메일 형식 오류 UI
- **WHEN** 유효하지 않은 이메일 입력 후 blur 또는 가입하기 클릭
- **THEN** 이메일 필드에 빨간 border, 필드 아래에 `⚠ 올바른 이메일 형식이 아닙니다` 표시

#### Scenario: 이메일 중복 UI (409)
- **WHEN** POST /auth/signup 응답이 409 EMAIL_TAKEN
- **THEN** 버튼 위(폼 내부)에 전체 너비 빨간 박스로 `✕ 이미 가입된 이메일입니다` 표시

#### Scenario: 비밀번호 8자 미만 UI
- **WHEN** 8자 미만 비밀번호 입력 후 blur 또는 가입하기 클릭
- **THEN** 비밀번호 필드에 빨간 border, 필드 아래에 `⚠ 8자 이상 입력해주세요` 표시

### Requirement: 로그인
시스템은 이메일+비밀번호 검증 후 JWT(24h 유효)를 발급해야 한다. 로그인 성공 시 users.team_id를 포함하여 반환 — NULL이면 팀 선택 화면, 값이 있으면 칸반 화면으로 분기. **에러는 비밀번호 필드와 로그인 버튼 사이에 전체 너비 빨간 박스로 표시한다.**

#### Scenario: 정상 로그인
- **WHEN** POST /auth/login { email, password } 정상 자격증명 요청
- **THEN** 200 + { token: "eyJ...(exp 24h)", user: { id, email, team_id } } 반환

#### Scenario: 자격증명 오류 UI (401)
- **WHEN** POST /auth/login 응답이 401 INVALID_CREDENTIALS
- **THEN** 비밀번호 필드와 로그인 버튼 사이에 전체 너비 빨간 박스로 `✕ 이메일 또는 비밀번호가 일치하지 않습니다` 표시

### Requirement: 로그아웃 (stateless)
시스템은 POST /auth/logout 요청에 HTTP 200만 반환한다. JWT 블랙리스트를 유지하지 않으며, 클라이언트가 localStorage에서 토큰을 삭제한다. (결정 #5)

#### Scenario: 로그아웃 요청
- **WHEN** POST /auth/logout (Authorization: Bearer {jwt}) 요청
- **THEN** 200 {} 반환, 서버 상태 변경 없음

### Requirement: 현재 사용자 조회
시스템은 유효한 JWT로 현재 로그인된 사용자 정보를 반환해야 한다.

#### Scenario: 정상 조회
- **WHEN** GET /auth/me (유효한 JWT) 요청
- **THEN** 200 { id, email, team_id } 반환

#### Scenario: JWT 만료
- **WHEN** 만료된 JWT로 API 요청
- **THEN** 401 { error: { code: "TOKEN_EXPIRED", message: "인증이 만료되었습니다" } }
