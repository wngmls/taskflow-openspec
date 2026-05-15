## MODIFIED Requirements

### Requirement: 회원가입
시스템은 이메일+비밀번호로 신규 계정을 생성하고 JWT를 즉시 발급해야 한다. **에러 표시는 전체 너비 빨간 박스(`border border-red-300 bg-red-50 text-red-700`)로, 해당 필드에는 빨간 border를 추가한다.**

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
시스템은 이메일+비밀번호 검증 후 JWT(24h 유효)를 발급해야 한다. **에러는 비밀번호 필드와 로그인 버튼 사이에 전체 너비 빨간 박스로 표시한다.**

#### Scenario: 정상 로그인
- **WHEN** POST /auth/login { email, password } 정상 자격증명 요청
- **THEN** 200 + { token, user: { id, email, team_id } } 반환

#### Scenario: 자격증명 오류 UI (401)
- **WHEN** POST /auth/login 응답이 401 INVALID_CREDENTIALS
- **THEN** 비밀번호 필드와 로그인 버튼 사이에 전체 너비 빨간 박스로 `✕ 이메일 또는 비밀번호가 일치하지 않습니다` 표시
