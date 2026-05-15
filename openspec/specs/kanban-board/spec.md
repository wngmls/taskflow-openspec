## ADDED Requirements

### Requirement: 태스크 목록 조회 및 필터
시스템은 팀의 태스크 목록을 반환하며, 필터(전체/@me/미할당)와 정렬(최근 생성순)을 지원해야 한다.

#### Scenario: 전체 태스크 조회
- **WHEN** GET /teams/{id}/tasks (팀 멤버 JWT) 요청
- **THEN** 200 [{ id, title, status, creator_id, assignee_id, created_at }] 최근 생성순 반환

#### Scenario: 내 태스크 필터
- **WHEN** GET /teams/{id}/tasks?filter=me (팀 멤버 JWT) 요청
- **THEN** 200 WHERE assignee_id = current_user_id 인 태스크만 반환 (creator_id 기준 아님, 결정 #4)

#### Scenario: 미할당 필터
- **WHEN** GET /teams/{id}/tasks?filter=unassigned 요청
- **THEN** 200 WHERE assignee_id IS NULL 인 태스크만 반환

### Requirement: 태스크 생성
시스템은 팀 멤버가 태스크를 생성할 수 있어야 한다. 생성 시 status는 TODO, creator_id는 현재 사용자, assignee_id는 nullable.

#### Scenario: 태스크 생성
- **WHEN** POST /teams/{id}/tasks { title: "DB 마이그레이션", assignee_id: 42 (옵션) } 요청
- **THEN** 201 { id, title, status: "TODO", creator_id, assignee_id, created_at } 반환

#### Scenario: 태스크 제목 유효성 오류
- **WHEN** 빈 문자열 또는 100자 초과 제목으로 POST 요청
- **THEN** 400 { error: { code: "VALIDATION_ERROR", message: "태스크 제목은 1-100자여야 합니다" } }

### Requirement: 태스크 상태 변경 (드래그)
시스템은 PATCH /tasks/{id}/status로 태스크 상태를 변경해야 한다. 유효한 상태: TODO, DOING, DONE. (결정 #3 — PUT에서 분리)

#### Scenario: 상태 변경 (드래그)
- **WHEN** PATCH /tasks/{id}/status { status: "DOING" } (팀 멤버 JWT) 요청
- **THEN** 200 { id, status: "DOING" } 반환, 시각 반응 < 50ms (정성 검증)

#### Scenario: 유효하지 않은 상태값
- **WHEN** PATCH /tasks/{id}/status { status: "INVALID" } 요청
- **THEN** 400 { error: { code: "VALIDATION_ERROR", message: "status는 TODO, DOING, DONE 중 하나여야 합니다" } }

### Requirement: 태스크 수정
시스템은 팀 멤버가 태스크 제목과 assignee를 수정할 수 있어야 한다.

#### Scenario: 제목 및 assignee 수정
- **WHEN** PUT /tasks/{id} { title: "새 제목", assignee_id: 43 } (팀 멤버 JWT) 요청
- **THEN** 200 { id, title, assignee_id } 반환

### Requirement: 태스크 삭제
시스템은 creator 또는 team owner만 태스크를 삭제할 수 있어야 한다. 그 외 403.

#### Scenario: creator가 삭제
- **WHEN** DELETE /tasks/{id} (creator JWT) 요청
- **THEN** 200 {} + 태스크 삭제

#### Scenario: team owner가 타인 카드 삭제
- **WHEN** DELETE /tasks/{id} (owner JWT, creator 아님) 요청
- **THEN** 200 {} + 태스크 삭제

#### Scenario: 일반 멤버가 타인 카드 삭제 시도
- **WHEN** DELETE /tasks/{id} (creator도 owner도 아닌 JWT) 요청
- **THEN** 403 { error: { code: "FORBIDDEN", message: "권한이 없습니다" } }

### Requirement: 태스크 상세 조회
시스템은 단일 태스크의 상세 정보를 반환해야 한다.

#### Scenario: 상세 조회
- **WHEN** GET /tasks/{id} (팀 멤버 JWT) 요청
- **THEN** 200 { id, title, status, creator_id, assignee_id, created_at } 반환
