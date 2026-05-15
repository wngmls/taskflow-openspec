## ADDED Requirements

### Requirement: 태스크 목록 조회 및 필터
시스템은 팀의 태스크 목록을 반환하며, 필터(전체/@me/미할당)와 정렬(최근 생성순)을 지원해야 한다. **UI는 필터 버튼을 헤더 아래 별도 바에 표시하며, 활성 필터는 `bg-gray-900 text-white` 스타일로 강조한다. 빈 칸반일 때 TODO 컬럼에만 `+ 첫 태스크 만들기` CTA 버튼을 강조 표시하고, DOING/DONE 컬럼은 `드래그로 이동` 안내 텍스트를 표시한다.**

#### Scenario: 빈 칸반 Empty State — TODO CTA
- **WHEN** 팀에 태스크가 0개인 상태에서 칸반 화면 로드
- **THEN** TODO 컬럼: 📋 아이콘 + `카드 없음` + `+ 첫 태스크 만들기` 클릭 가능 링크 표시
- **THEN** DOING/DONE 컬럼: 📋 아이콘 + `카드 없음` + `드래그로 이동` 텍스트(클릭 불가) 표시

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
시스템은 팀 멤버가 태스크를 생성할 수 있어야 한다. 생성 시 status는 TODO, creator_id는 현재 사용자, assignee_id는 nullable. **UI는 컬럼 헤더 `+` 클릭 시 인라인 입력 폼을 표시하며, 폼에는 제목 입력 필드와 팀 멤버 목록으로 구성된 담당자 드롭다운이 포함된다. 드롭다운의 기본값은 현재 사용자(@me)이며, `GET /teams/{id}/members` 응답으로 동적으로 구성한다.**

#### Scenario: 태스크 생성
- **WHEN** POST /teams/{id}/tasks { title: "DB 마이그레이션", assignee_id: 42 (옵션) } 요청
- **THEN** 201 { id, title, status: "TODO", creator_id, assignee_id, created_at } 반환

#### Scenario: 인라인 입력 UI
- **WHEN** 사용자가 컬럼 헤더 `+` 버튼 클릭
- **THEN** 컬럼 상단에 인라인 입력 폼(제목 + 담당자 드롭다운) 표시, Enter로 저장, Esc로 취소

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

### Requirement: 칸반 화면 레이아웃
칸반 화면은 스토리보드 v2 와이어프레임을 따른다.

#### Scenario: 컬럼 색상 구분
- **WHEN** 칸반 화면 로드
- **THEN** TODO 컬럼은 amber 배경(`bg-amber-50`, 헤더 `text-amber-700`), DOING은 blue(`bg-blue-50`, `text-blue-700`), DONE은 green(`bg-green-50`, `text-green-700`)으로 표시

#### Scenario: 헤더 탭 내비게이션
- **WHEN** 칸반 화면 로드
- **THEN** 헤더 중앙에 칸반/채팅/멤버 탭 버튼 표시, 현재 페이지(칸반)는 teal 채움 버튼(`bg-teal-600 text-white`), 나머지는 비활성 스타일

#### Scenario: 로고 컴포넌트
- **WHEN** 어느 화면이든 로드
- **THEN** 헤더 좌측에 teal 배경 박스 안에 흰색 텍스트 `TaskFlow` 로고 표시

### Requirement: 카드 상세 모달 레이아웃
카드 클릭 시 열리는 모달은 스토리보드 v2 레이아웃을 따른다.

#### Scenario: 모달 레이아웃
- **WHEN** 카드 클릭으로 모달 열림
- **THEN** 모달 상단에 `#ID 제목` 표시, 좌측에 상태(TODO/DOING/DONE 탭 버튼), 담당자, 생성자, 생성시각 메타 정보 표시, 우측에 저장/다른 담당자 지정/삭제 버튼 3개 표시

#### Scenario: 삭제 버튼 스타일
- **WHEN** creator 또는 owner가 모달 열람
- **THEN** 삭제 버튼을 빨간 border 박스 버튼(`border border-red-400 text-red-600`)으로 표시

### Requirement: 모바일 칸반 반응형
모바일(< 768px)에서 칸반은 컬럼 탭 인디케이터와 FAB 버튼을 사용한다.

#### Scenario: 컬럼 탭 인디케이터
- **WHEN** 모바일에서 칸반 화면 로드
- **THEN** 상단에 TODO/DOING/DONE 탭 표시, 활성 탭은 bold + 하단 underline, 탭 클릭 시 해당 컬럼으로 전환

#### Scenario: FAB 버튼
- **WHEN** 모바일에서 칸반 화면
- **THEN** 우하단 고정 `+` 원형 버튼 표시, 클릭 시 현재 활성 컬럼에 인라인 입력 활성화

#### Scenario: 카드 길게 누르기
- **WHEN** 모바일에서 카드를 500ms 이상 길게 누름
- **THEN** TODO/DOING/DONE 상태 선택 바텀시트 메뉴 표시, 선택 시 PATCH /tasks/{id}/status 호출
