## ADDED Requirements

### Requirement: 회원가입
시스템은 이메일+비밀번호로 신규 계정을 생성하고 JWT를 즉시 발급해야 한다. 이메일은 UNIQUE, 비밀번호는 bcrypt 해시 저장. 이메일 인증 없이 즉시 활성화.

#### Scenario: 정상 가입
- **WHEN** POST /auth/signup { email: "user@example.com", password: "12345678" } 요청
- **THEN** 201 Created + { token: "eyJ...", user: { id, email, team_id: null } } 반환

#### Scenario: 이메일 중복
- **WHEN** 이미 가입된 이메일로 POST /auth/signup 요청
- **THEN** 409 { error: { code: "EMAIL_TAKEN", message: "이미 가입된 이메일입니다" } }

#### Scenario: 이메일 형식 오류
- **WHEN** 이메일 형식이 아닌 값으로 POST /auth/signup 요청
- **THEN** 400 { error: { code: "VALIDATION_ERROR", message: "올바른 이메일 형식이 아닙니다" } }

#### Scenario: 비밀번호 8자 미만
- **WHEN** 7자 이하 비밀번호로 POST /auth/signup 요청
- **THEN** 400 { error: { code: "VALIDATION_ERROR", message: "8자 이상 입력해주세요" } }

### Requirement: 로그인
시스템은 이메일+비밀번호 검증 후 JWT(24h 유효)를 발급해야 한다. 로그인 성공 시 users.team_id를 포함하여 반환 — NULL이면 팀 선택 화면, 값이 있으면 칸반 화면으로 분기.

#### Scenario: 정상 로그인
- **WHEN** POST /auth/login { email, password } 정상 자격증명 요청
- **THEN** 200 + { token: "eyJ...(exp 24h)", user: { id, email, team_id } } 반환

#### Scenario: 자격증명 오류
- **WHEN** 잘못된 이메일 또는 비밀번호로 POST /auth/login 요청
- **THEN** 401 { error: { code: "INVALID_CREDENTIALS", message: "이메일 또는 비밀번호가 일치하지 않습니다" } } — 이메일 존재 여부 노출 금지

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
