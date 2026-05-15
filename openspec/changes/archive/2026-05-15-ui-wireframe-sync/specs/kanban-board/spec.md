## MODIFIED Requirements

### Requirement: 태스크 목록 조회 및 필터
시스템은 팀의 태스크 목록을 반환하며, 필터(전체/@me/미할당)와 정렬(최근 생성순)을 지원해야 한다. **UI는 필터 버튼을 헤더 아래 별도 바에 표시하며, 활성 필터는 `bg-gray-900 text-white` 스타일로 강조한다.**

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

## ADDED Requirements

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
