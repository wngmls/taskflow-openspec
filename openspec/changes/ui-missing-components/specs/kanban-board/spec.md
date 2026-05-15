## MODIFIED Requirements

### Requirement: 태스크 목록 조회 및 필터
시스템은 팀의 태스크 목록을 반환하며, 필터(전체/@me/미할당)와 정렬(최근 생성순)을 지원해야 한다. **빈 칸반일 때 TODO 컬럼에만 `+ 첫 태스크 만들기` CTA 버튼을 강조 표시하고, DOING/DONE 컬럼은 `드래그로 이동` 안내 텍스트를 표시한다.**

#### Scenario: 빈 칸반 Empty State — TODO CTA
- **WHEN** 팀에 태스크가 0개인 상태에서 칸반 화면 로드
- **THEN** TODO 컬럼: 📋 아이콘 + `카드 없음` + `+ 첫 태스크 만들기` 클릭 가능 링크 표시
- **THEN** DOING/DONE 컬럼: 📋 아이콘 + `카드 없음` + `드래그로 이동` 텍스트(클릭 불가) 표시

#### Scenario: 전체 태스크 조회
- **WHEN** GET /teams/{id}/tasks (팀 멤버 JWT) 요청
- **THEN** 200 [{ id, title, status, creator_id, assignee_id, created_at }] 최근 생성순 반환

#### Scenario: 내 태스크 필터
- **WHEN** GET /teams/{id}/tasks?filter=me 요청
- **THEN** 200 WHERE assignee_id = current_user_id 인 태스크만 반환

#### Scenario: 미할당 필터
- **WHEN** GET /teams/{id}/tasks?filter=unassigned 요청
- **THEN** 200 WHERE assignee_id IS NULL 인 태스크만 반환

## ADDED Requirements

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
